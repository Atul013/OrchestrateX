#!/usr/bin/env python3
"""
Advanced OrchestrateX Multi-Model Client

This client implements the complete multi-model orchestration workflow:
1. Secure API key management
2. Model selection via ML API
3. Primary response from best model
4. Concurrent critique responses from other models
5. Comprehensive error handling and retries
6. UI-ready response formatting

Usage:
    from advanced_client import MultiModelOrchestrator
    
    orchestrator = MultiModelOrchestrator()
    result = await orchestrator.orchestrate_with_critiques("Your prompt here")
"""

import asyncio
import aiohttp
import os
import logging
import time
import json
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from datetime import datetime
import backoff
from concurrent.futures import ThreadPoolExecutor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
    handlers=[
        logging.FileHandler('orchestratex_advanced.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class ModelResponse:
    """Structured response from an AI model"""
    model_name: str
    response_text: str
    response_type: str  # "primary" or "critique"
    tokens_used: int
    latency_ms: int
    cost_usd: float
    confidence_score: float
    success: bool
    error_message: Optional[str] = None
    timestamp: str = None
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow().isoformat()
        if self.metadata is None:
            self.metadata = {}

@dataclass
class OrchestrationResult:
    """Complete orchestration result with primary response and critiques"""
    original_prompt: str
    selected_model: str
    model_confidence_scores: Dict[str, float]
    primary_response: ModelResponse
    critique_responses: List[ModelResponse]
    total_latency_ms: int
    total_cost_usd: float
    success: bool
    error_summary: Optional[str] = None
    timestamp: str = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for UI integration"""
        return {
            "prompt": self.original_prompt,
            "selected_model": self.selected_model,
            "confidence_scores": self.model_confidence_scores,
            "primary_response": asdict(self.primary_response),
            "critiques": [asdict(resp) for resp in self.critique_responses],
            "summary": {
                "total_latency_ms": self.total_latency_ms,
                "total_cost_usd": self.total_cost_usd,
                "success": self.success,
                "models_used": len(self.critique_responses) + 1,
                "timestamp": self.timestamp
            },
            "error": self.error_summary
        }

class SecureAPIKeyManager:
    """Secure management of API keys"""
    
    def __init__(self):
        self.api_keys = {}
        self._load_keys()
    
    def _load_keys(self):
        """Load API keys from environment variables"""
        key_mappings = {
            "openrouter": "OPENROUTER_API_KEY",
            "model_selector": "MODEL_SELECTOR_API_KEY",
            "backup_openai": "OPENAI_API_KEY",
            "backup_anthropic": "ANTHROPIC_API_KEY"
        }
        
        for service, env_var in key_mappings.items():
            key = os.getenv(env_var)
            if key:
                self.api_keys[service] = key
                logger.info(f"✅ Loaded API key for {service}")
            else:
                logger.warning(f"⚠️ No API key found for {service} (env var: {env_var})")
    
    def get_key(self, service: str) -> Optional[str]:
        """Get API key for a service"""
        return self.api_keys.get(service)
    
    def has_key(self, service: str) -> bool:
        """Check if API key exists for a service"""
        return service in self.api_keys and bool(self.api_keys[service])

class MultiModelOrchestrator:
    """
    Advanced multi-model orchestration client with concurrent critiques
    """
    
    def __init__(self, 
                 model_selector_url: str = "http://localhost:5000",
                 max_retries: int = 3,
                 timeout: int = 30,
                 max_concurrent: int = 6):
        """
        Initialize the advanced orchestrator
        
        Args:
            model_selector_url: URL of the model selector API
            max_retries: Maximum retry attempts for failed requests
            timeout: Request timeout in seconds
            max_concurrent: Maximum concurrent API calls
        """
        self.model_selector_url = model_selector_url
        self.max_retries = max_retries
        self.timeout = timeout
        self.max_concurrent = max_concurrent
        
        # Initialize secure key manager
        self.key_manager = SecureAPIKeyManager()
        
        # OpenRouter model mappings
        self.model_mappings = {
            "TNG DeepSeek": "deepseek/deepseek-r1",
            "GLM4.5": "zhipuai/glm-4-plus",
            "GPT-OSS": "openai/gpt-4o-mini",
            "MoonshotAI Kimi": "moonshot/moonshot-v1-32k",
            "Llama 4 Maverick": "meta-llama/llama-3.2-90b-vision-instruct",
            "Qwen3": "qwen/qwen-2.5-coder-32b-instruct"
        }
        
        # Model cost estimates (per 1K tokens)
        self.model_costs = {
            "TNG DeepSeek": 0.002,
            "GLM4.5": 0.003,
            "GPT-OSS": 0.001,
            "MoonshotAI Kimi": 0.002,
            "Llama 4 Maverick": 0.0015,
            "Qwen3": 0.002
        }
        
        self.session = None
        self.stats = {
            "total_orchestrations": 0,
            "successful_orchestrations": 0,
            "failed_orchestrations": 0,
            "total_api_calls": 0,
            "total_cost": 0.0,
            "model_usage": {}
        }
    
    async def __aenter__(self):
        """Async context manager entry"""
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=self.timeout),
            connector=aiohttp.TCPConnector(limit=50, limit_per_host=10)
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()
    
    @backoff.on_exception(
        backoff.expo,
        (aiohttp.ClientError, asyncio.TimeoutError),
        max_tries=3,
        max_time=60
    )
    async def _call_model_selector_api(self, prompt: str) -> Tuple[str, Dict[str, float]]:
        """
        Call model selector API with retry logic
        
        Args:
            prompt: Input prompt to analyze
            
        Returns:
            Tuple of (best_model, confidence_scores)
        """
        try:
            logger.info(f"🎯 Calling model selector for prompt: '{prompt[:50]}...'")
            
            async with self.session.post(
                f"{self.model_selector_url}/predict",
                json={"prompt": prompt},
                headers={"Content-Type": "application/json"}
            ) as response:
                
                if response.status == 200:
                    data = await response.json()
                    best_model = data["best_model"]
                    confidence_scores = data["confidence_scores"]
                    
                    logger.info(f"✅ Model selector result: {best_model} (confidence: {data['prediction_confidence']:.3f})")
                    return best_model, confidence_scores
                else:
                    error_text = await response.text()
                    logger.error(f"❌ Model selector API error {response.status}: {error_text}")
                    raise aiohttp.ClientError(f"Model selector API error: {error_text}")
                    
        except Exception as e:
            logger.error(f"❌ Model selector API call failed: {e}")
            # Fallback to default model
            logger.warning("🔄 Using fallback model selection")
            return "GPT-OSS", {"GPT-OSS": 0.7, "TNG DeepSeek": 0.3}
    
    @backoff.on_exception(
        backoff.expo,
        (aiohttp.ClientError, asyncio.TimeoutError),
        max_tries=3,
        max_time=120
    )
    async def _call_openrouter_api(self, 
                                  model_name: str, 
                                  prompt: str,
                                  is_critique: bool = False,
                                  original_response: str = None,
                                  temperature: float = 0.7) -> ModelResponse:
        """
        Call OpenRouter API for a specific model with retry logic
        
        Args:
            model_name: Name of the AI model
            prompt: Input prompt or critique prompt
            is_critique: Whether this is a critique request
            original_response: Original response to critique (if applicable)
            temperature: Model temperature setting
            
        Returns:
            ModelResponse with result
        """
        if not self.key_manager.has_key("openrouter"):
            logger.warning(f"⚠️ No OpenRouter API key - simulating {model_name} response")
            return await self._simulate_model_response(model_name, prompt, is_critique)
        
        if model_name not in self.model_mappings:
            logger.error(f"❌ Unknown model: {model_name}")
            return ModelResponse(
                model_name=model_name,
                response_text="",
                response_type="critique" if is_critique else "primary",
                tokens_used=0,
                latency_ms=0,
                cost_usd=0.0,
                confidence_score=0.0,
                success=False,
                error_message=f"Unknown model: {model_name}"
            )
        
        start_time = time.time()
        
        try:
            openrouter_model = self.model_mappings[model_name]
            
            # Prepare the prompt
            if is_critique and original_response:
                critique_prompt = f"""Please analyze and critique the following response to the original prompt:

Original Prompt: {prompt}

Response to Critique: {original_response}

Please provide:
1. What this response does well
2. Areas for improvement
3. Any missing information or perspectives
4. An improved version of the response

Your critique:"""
                final_prompt = critique_prompt
                response_type = "critique"
            else:
                final_prompt = prompt
                response_type = "primary"
            
            logger.info(f"🤖 Calling {model_name} ({response_type}) via OpenRouter...")
            
            headers = {
                "Authorization": f"Bearer {self.key_manager.get_key('openrouter')}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://orchestratex.app",
                "X-Title": "OrchestrateX Advanced Client"
            }
            
            payload = {
                "model": openrouter_model,
                "messages": [
                    {
                        "role": "user",
                        "content": final_prompt
                    }
                ],
                "max_tokens": 4000,
                "temperature": temperature,
                "top_p": 0.9
            }
            
            async with self.session.post(
                "https://openrouter.ai/api/v1/chat/completions",
                json=payload,
                headers=headers
            ) as response:
                
                end_time = time.time()
                latency_ms = int((end_time - start_time) * 1000)
                
                if response.status == 200:
                    data = await response.json()
                    
                    if not data.get("choices") or not data["choices"][0].get("message"):
                        raise aiohttp.ClientError("Invalid response format from OpenRouter")
                    
                    response_text = data["choices"][0]["message"]["content"]
                    usage = data.get("usage", {})
                    tokens_used = usage.get("total_tokens", 0)
                    
                    # Calculate cost
                    cost_usd = (tokens_used / 1000) * self.model_costs.get(model_name, 0.002)
                    
                    # Log success
                    logger.info(f"✅ {model_name} ({response_type}): {len(response_text)} chars, {tokens_used} tokens, ${cost_usd:.4f}, {latency_ms}ms")
                    
                    self.stats["total_api_calls"] += 1
                    self.stats["total_cost"] += cost_usd
                    self.stats["model_usage"][model_name] = self.stats["model_usage"].get(model_name, 0) + 1
                    
                    return ModelResponse(
                        model_name=model_name,
                        response_text=response_text,
                        response_type=response_type,
                        tokens_used=tokens_used,
                        latency_ms=latency_ms,
                        cost_usd=cost_usd,
                        confidence_score=1.0,  # Full confidence for successful response
                        success=True,
                        metadata={
                            "openrouter_model": openrouter_model,
                            "finish_reason": data["choices"][0].get("finish_reason"),
                            "prompt_tokens": usage.get("prompt_tokens", 0),
                            "completion_tokens": usage.get("completion_tokens", 0),
                            "temperature": temperature
                        }
                    )
                    
                else:
                    error_text = await response.text()
                    logger.error(f"❌ OpenRouter API error {response.status} for {model_name}: {error_text}")
                    raise aiohttp.ClientError(f"OpenRouter API error: {error_text}")
                    
        except Exception as e:
            end_time = time.time()
            latency_ms = int((end_time - start_time) * 1000)
            
            logger.error(f"❌ Failed to call {model_name}: {e}")
            return ModelResponse(
                model_name=model_name,
                response_text="",
                response_type=response_type if 'response_type' in locals() else "unknown",
                tokens_used=0,
                latency_ms=latency_ms,
                cost_usd=0.0,
                confidence_score=0.0,
                success=False,
                error_message=str(e)
            )
    
    async def _simulate_model_response(self, 
                                     model_name: str, 
                                     prompt: str,
                                     is_critique: bool = False) -> ModelResponse:
        """Simulate AI model response for testing without API keys"""
        
        await asyncio.sleep(0.5)  # Simulate API latency
        
        if is_critique:
            response_templates = {
                "TNG DeepSeek": f"[DeepSeek Critique] This response demonstrates solid reasoning but could benefit from deeper analysis of edge cases in: {prompt[:50]}...",
                "GLM4.5": f"[GLM4.5 Critique] The response is comprehensive but might be improved with more structured formatting for: {prompt[:50]}...",
                "GPT-OSS": f"[GPT-OSS Critique] Good explanation overall, however consider adding practical examples for: {prompt[:50]}...",
                "MoonshotAI Kimi": f"[Kimi Critique] Creative approach, but could be enhanced with more technical precision for: {prompt[:50]}...",
                "Llama 4 Maverick": f"[Llama Critique] Thoughtful response, though additional context would strengthen the argument in: {prompt[:50]}...",
                "Qwen3": f"[Qwen3 Critique] Technical accuracy is good, but user experience considerations could be added for: {prompt[:50]}..."
            }
            response_type = "critique"
        else:
            response_templates = {
                "TNG DeepSeek": f"[DeepSeek Primary] Advanced reasoning and comprehensive analysis for: {prompt[:50]}...",
                "GLM4.5": f"[GLM4.5 Primary] Detailed and well-structured response to: {prompt[:50]}...",
                "GPT-OSS": f"[GPT-OSS Primary] Versatile and practical solution for: {prompt[:50]}...",
                "MoonshotAI Kimi": f"[Kimi Primary] Creative and innovative approach to: {prompt[:50]}...",
                "Llama 4 Maverick": f"[Llama Primary] Reliable and thorough analysis of: {prompt[:50]}...",
                "Qwen3": f"[Qwen3 Primary] Technical and precise implementation for: {prompt[:50]}..."
            }
            response_type = "primary"
        
        template = response_templates.get(model_name, f"[{model_name} {response_type.title()}] Response to: {prompt[:50]}...")
        response_text = template
        
        # Add contextual content
        if "code" in prompt.lower():
            response_text += "\n\n```python\n# Simulated code example\ndef example_solution():\n    return 'Simulated implementation'\n```"
        elif "explain" in prompt.lower():
            response_text += "\n\nKey points:\n1. Fundamental concepts\n2. Practical applications\n3. Best practices"
        
        tokens_used = len(response_text.split()) * 1.3
        
        return ModelResponse(
            model_name=model_name,
            response_text=response_text,
            response_type=response_type,
            tokens_used=int(tokens_used),
            latency_ms=500 + (100 if is_critique else 0),  # Slightly longer for critiques
            cost_usd=0.001,
            confidence_score=0.85,
            success=True,
            metadata={"simulated": True, "reason": "No API key available"}
        )
    
    async def orchestrate_with_critiques(self, prompt: str) -> OrchestrationResult:
        """
        Complete orchestration workflow with primary response and concurrent critiques
        
        Args:
            prompt: Input prompt to process
            
        Returns:
            OrchestrationResult with primary response and critiques
        """
        start_time = time.time()
        self.stats["total_orchestrations"] += 1
        
        try:
            logger.info(f"🎭 Starting advanced orchestration for: '{prompt[:50]}...'")
            
            # Step 1: Get model selection
            selected_model, confidence_scores = await self._call_model_selector_api(prompt)
            
            # Step 2: Get primary response from selected model
            primary_response = await self._call_openrouter_api(
                selected_model, 
                prompt, 
                is_critique=False
            )
            
            if not primary_response.success:
                logger.warning(f"⚠️ Primary model {selected_model} failed, trying fallback...")
                # Try fallback model
                fallback_models = ["GPT-OSS", "Llama 4 Maverick", "TNG DeepSeek"]
                for fallback in fallback_models:
                    if fallback != selected_model:
                        primary_response = await self._call_openrouter_api(
                            fallback, 
                            prompt, 
                            is_critique=False
                        )
                        if primary_response.success:
                            logger.info(f"✅ Fallback successful with {fallback}")
                            selected_model = fallback
                            break
            
            # Step 3: Get concurrent critiques from other models
            other_models = [model for model in self.model_mappings.keys() if model != selected_model]
            
            logger.info(f"🔄 Getting critiques from {len(other_models)} other models...")
            
            # Create semaphore for concurrency control
            semaphore = asyncio.Semaphore(self.max_concurrent)
            
            async def get_critique_with_semaphore(model):
                async with semaphore:
                    return await self._call_openrouter_api(
                        model,
                        prompt,
                        is_critique=True,
                        original_response=primary_response.response_text if primary_response.success else None,
                        temperature=0.8  # Slightly higher temperature for critiques
                    )
            
            # Execute critique requests concurrently
            critique_tasks = [get_critique_with_semaphore(model) for model in other_models]
            critique_responses = await asyncio.gather(*critique_tasks, return_exceptions=True)
            
            # Handle exceptions in critique responses
            processed_critiques = []
            for i, response in enumerate(critique_responses):
                if isinstance(response, Exception):
                    logger.error(f"❌ Critique from {other_models[i]} failed: {response}")
                    # Create failed response object
                    failed_response = ModelResponse(
                        model_name=other_models[i],
                        response_text="",
                        response_type="critique",
                        tokens_used=0,
                        latency_ms=0,
                        cost_usd=0.0,
                        confidence_score=0.0,
                        success=False,
                        error_message=str(response)
                    )
                    processed_critiques.append(failed_response)
                else:
                    processed_critiques.append(response)
            
            # Calculate totals
            end_time = time.time()
            total_latency_ms = int((end_time - start_time) * 1000)
            total_cost = primary_response.cost_usd + sum(c.cost_usd for c in processed_critiques)
            
            # Determine overall success
            successful_critiques = sum(1 for c in processed_critiques if c.success)
            overall_success = primary_response.success and successful_critiques > 0
            
            if overall_success:
                self.stats["successful_orchestrations"] += 1
            else:
                self.stats["failed_orchestrations"] += 1
            
            logger.info(f"✅ Orchestration completed: Primary={primary_response.success}, Critiques={successful_critiques}/{len(processed_critiques)}")
            
            # Add confidence scores to critiques
            for critique in processed_critiques:
                if critique.success:
                    critique.confidence_score = confidence_scores.get(critique.model_name, 0.5)
            
            return OrchestrationResult(
                original_prompt=prompt,
                selected_model=selected_model,
                model_confidence_scores=confidence_scores,
                primary_response=primary_response,
                critique_responses=processed_critiques,
                total_latency_ms=total_latency_ms,
                total_cost_usd=total_cost,
                success=overall_success,
                error_summary=None if overall_success else "Some API calls failed"
            )
            
        except Exception as e:
            end_time = time.time()
            total_latency_ms = int((end_time - start_time) * 1000)
            
            logger.error(f"❌ Orchestration failed completely: {e}")
            self.stats["failed_orchestrations"] += 1
            
            return OrchestrationResult(
                original_prompt=prompt,
                selected_model="unknown",
                model_confidence_scores={},
                primary_response=ModelResponse(
                    model_name="error",
                    response_text="",
                    response_type="primary",
                    tokens_used=0,
                    latency_ms=0,
                    cost_usd=0.0,
                    confidence_score=0.0,
                    success=False,
                    error_message=str(e)
                ),
                critique_responses=[],
                total_latency_ms=total_latency_ms,
                total_cost_usd=0.0,
                success=False,
                error_summary=str(e)
            )
    
    def print_stats(self):
        """Print orchestrator statistics"""
        print("\n📊 Advanced Orchestrator Statistics")
        print("=" * 45)
        print(f"Total Orchestrations: {self.stats['total_orchestrations']}")
        print(f"Successful: {self.stats['successful_orchestrations']}")
        print(f"Failed: {self.stats['failed_orchestrations']}")
        
        if self.stats['total_orchestrations'] > 0:
            success_rate = (self.stats['successful_orchestrations'] / self.stats['total_orchestrations']) * 100
            print(f"Success Rate: {success_rate:.1f}%")
        
        print(f"Total API Calls: {self.stats['total_api_calls']}")
        print(f"Total Cost: ${self.stats['total_cost']:.4f}")
        
        if self.stats['model_usage']:
            print("\nModel Usage:")
            for model, count in sorted(self.stats['model_usage'].items()):
                print(f"  {model}: {count}")
    
    def save_result(self, result: OrchestrationResult, filename: str = None):
        """Save orchestration result to JSON file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"orchestration_result_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(result.to_dict(), f, indent=2, ensure_ascii=False)
        
        logger.info(f"💾 Result saved to {filename}")

# UI Integration Helper Functions
def format_for_ui(result: OrchestrationResult) -> Dict[str, Any]:
    """Format orchestration result for UI display"""
    return {
        "primary": {
            "model": result.primary_response.model_name,
            "response": result.primary_response.response_text,
            "confidence": result.model_confidence_scores.get(result.primary_response.model_name, 0.0),
            "latency": result.primary_response.latency_ms,
            "cost": result.primary_response.cost_usd,
            "success": result.primary_response.success
        },
        "critiques": [
            {
                "model": critique.model_name,
                "response": critique.response_text,
                "confidence": critique.confidence_score,
                "latency": critique.latency_ms,
                "cost": critique.cost_usd,
                "success": critique.success
            }
            for critique in result.critique_responses
        ],
        "summary": {
            "prompt": result.original_prompt,
            "total_models": len(result.critique_responses) + 1,
            "successful_models": sum(1 for c in result.critique_responses if c.success) + (1 if result.primary_response.success else 0),
            "total_cost": result.total_cost_usd,
            "total_time": result.total_latency_ms,
            "timestamp": result.timestamp
        }
    }

# Example usage and testing
async def example_usage():
    """Example of how to use the advanced orchestrator"""
    
    async with MultiModelOrchestrator() as orchestrator:
        
        # Test prompt
        prompt = "Write a Python function to implement a binary search algorithm with error handling"
        
        # Get complete orchestration with critiques
        result = await orchestrator.orchestrate_with_critiques(prompt)
        
        # Print results
        print(f"\n🎯 Primary Response from {result.selected_model}:")
        print(f"Success: {result.primary_response.success}")
        if result.primary_response.success:
            print(f"Response: {result.primary_response.response_text[:200]}...")
        
        print(f"\n📝 Critiques from {len(result.critique_responses)} other models:")
        for critique in result.critique_responses:
            status = "✅" if critique.success else "❌"
            print(f"{status} {critique.model_name}: {critique.response_text[:100] if critique.success else critique.error_message}...")
        
        # Show UI-formatted result
        ui_data = format_for_ui(result)
        print(f"\n📊 Summary: {ui_data['summary']}")
        
        # Print stats
        orchestrator.print_stats()
        
        return result

if __name__ == "__main__":
    # Run example
    asyncio.run(example_usage())
