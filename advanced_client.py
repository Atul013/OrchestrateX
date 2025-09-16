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
    
    def __init__(self, env_file_path: str = "orche.env"):
        self.api_keys = {}
        self.env_file_path = env_file_path
        self._load_keys()
    
    def _load_keys(self):
        """Load API keys from orche.env file and environment variables"""
        # First load from orche.env file
        self._load_from_env_file()
        
        # Then load from environment variables (they override file values)
        self._load_from_environment()
        
        if not self.api_keys:
            logger.warning("⚠️ No API keys found in orche.env or environment variables")
            logger.info("💡 Make sure orche.env exists with valid API keys")
    
    def _load_from_env_file(self):
        """Load API keys from orche.env file"""
        if not os.path.exists(self.env_file_path):
            logger.warning(f"⚠️ Environment file {self.env_file_path} not found")
            return
            
        try:
            with open(self.env_file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if '=' in line and not line.startswith('#') and line:
                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip()
                        
                        # Map provider keys to model names
                        if key == 'PROVIDER_GLM45_API_KEY' and value:
                            self.api_keys['GLM4.5'] = value
                        elif key == 'PROVIDER_GPTOSS_API_KEY' and value:
                            self.api_keys['GPT-OSS'] = value
                        elif key == 'PROVIDER_LLAMA3_API_KEY' and value:
                            self.api_keys['Llama 4 Maverick'] = value
                        elif key == 'PROVIDER_KIMI_API_KEY' and value:
                            self.api_keys['MoonshotAI Kimi'] = value
                        elif key == 'PROVIDER_QWEN3_API_KEY' and value:
                            self.api_keys['Qwen3'] = value
                        elif key == 'PROVIDER_FALCON_API_KEY' and value:
                            self.api_keys['TNG DeepSeek'] = value
                            
            logger.info(f"[OK] Loaded API keys for {len(self.api_keys)} models from {self.env_file_path}")
            for model in self.api_keys.keys():
                logger.info(f"  [MODEL] {model}")
                
        except Exception as e:
            logger.error(f"[ERROR] Error reading {self.env_file_path}: {e}")
    
    def _load_from_environment(self):
        """Load API keys from environment variables (overrides file values)"""
        env_mappings = {
            'PROVIDER_GLM45_API_KEY': 'GLM4.5',
            'PROVIDER_GPTOSS_API_KEY': 'GPT-OSS', 
            'PROVIDER_LLAMA3_API_KEY': 'Llama 4 Maverick',
            'PROVIDER_KIMI_API_KEY': 'MoonshotAI Kimi',
            'PROVIDER_QWEN3_API_KEY': 'Qwen3',
            'PROVIDER_FALCON_API_KEY': 'TNG DeepSeek',
            'OPENROUTER_API_KEY': 'openrouter'  # Generic fallback key
        }
        
        env_override_count = 0
        for env_key, model_name in env_mappings.items():
            value = os.getenv(env_key)
            if value:
                self.api_keys[model_name] = value
                env_override_count += 1
                
        if env_override_count > 0:
            logger.info(f"✅ Environment variables override {env_override_count} API keys")
    
    def get_key(self, service: str) -> Optional[str]:
        """Get API key for a service/model"""
        # Direct service lookup
        if service in self.api_keys:
            return self.api_keys[service]
        
        # Model name mapping for backwards compatibility
        model_mappings = {
            "openrouter": "GPT-OSS",  # Use any available key as fallback
            "model_selector": None,   # No key needed for local model selector
        }
        
        mapped_service = model_mappings.get(service, service)
        if mapped_service and mapped_service in self.api_keys:
            return self.api_keys[mapped_service]
        
        # Return any available OpenRouter key as fallback
        if service == "openrouter" and self.api_keys:
            return next(iter(self.api_keys.values()))
            
        return None
    
    def get_model_key(self, model_name: str) -> Optional[str]:
        """Get API key for specific model"""
        return self.api_keys.get(model_name)
    
    def has_key(self, service: str) -> bool:
        """Check if API key exists for a service"""
        return self.get_key(service) is not None
    
    def has_model_key(self, model_name: str) -> bool:
        """Check if API key exists for a model"""
        return model_name in self.api_keys
    
    def list_available_models(self) -> List[str]:
        """List models with available API keys"""
        return list(self.api_keys.keys())

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
        
        # OpenRouter model mappings - using exact IDs from orche.env
        self.model_mappings = {
            "TNG DeepSeek": "tngtech/deepseek-r1t2-chimera:free",  # PROVIDER_FALCON_MODEL
            "GLM4.5": "z-ai/glm-4.5-air:free",  # PROVIDER_GLM45_MODEL
            "GPT-OSS": "openai/gpt-oss-120b:free",  # PROVIDER_GPTOSS_MODEL
            "MoonshotAI Kimi": "moonshotai/kimi-k2:free",  # PROVIDER_KIMI_MODEL
            "Llama 4 Maverick": "meta-llama/llama-4-maverick:free",  # PROVIDER_LLAMA3_MODEL
            "Qwen3": "qwen/qwen3-coder:free"  # PROVIDER_QWEN3_MODEL
        }
        
        # Model cost estimates (per 1K tokens) - All models are free tier
        self.model_costs = {
            "TNG DeepSeek": 0.0,  # Free tier
            "GLM4.5": 0.0,        # Free tier
            "GPT-OSS": 0.0,       # Free tier
            "MoonshotAI Kimi": 0.0, # Free tier
            "Llama 4 Maverick": 0.0, # Free tier
            "Qwen3": 0.0          # Free tier
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
        # Get model-specific API key
        api_key = self.key_manager.get_model_key(model_name)
        if not api_key:
            # Fallback to any available key
            api_key = self.key_manager.get_key("openrouter")
        
        if not api_key:
            logger.warning(f"⚠️ No API key available for {model_name} - simulating response")
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
                # Add unique focus areas for each model to reduce redundancy
                focus_areas = {
                    "TNG DeepSeek": "technical accuracy and logical reasoning",
                    "GLM4.5": "clarity and structure", 
                    "GPT-OSS": "completeness and missing information",
                    "MoonshotAI Kimi": "creativity and alternative perspectives",
                    "Llama 4 Maverick": "practical applicability and real-world relevance",
                    "Qwen3": "precision and factual correctness"
                }
                
                focus = focus_areas.get(model_name, "overall quality")
                
                # Customize critique prompts for shorter, focused responses
                if model_name == "TNG DeepSeek":
                    critique_prompt = f"""Analyze ONLY technical accuracy and logical flow: {original_response}

Provide a 15-word critique focusing on: logical gaps, technical errors, or reasoning flaws. Be specific and concise."""
                elif model_name == "Qwen3":
                    critique_prompt = f"""Check ONLY factual precision and data accuracy: {original_response}

Provide a 15-word critique focusing on: factual errors, data precision, or citation needs. Avoid technical logic points."""
                else:
                    critique_prompt = f"""Critique {focus}: {original_response}

Give a 3-5 word critique about {focus}. Format: "Missing [specific thing]" or "Lacks [specific element]" or "Needs [specific improvement]"."""
                
                final_prompt = critique_prompt
                response_type = "critique"
            else:
                final_prompt = prompt
                response_type = "primary"
            
            logger.info(f"🤖 Calling {model_name} ({response_type}) via OpenRouter...")
            
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://orchestratex.app",
                "X-Title": "OrchestrateX Advanced Client"
            }
            
            # Model-specific configuration for response length
            if model_name == "TNG DeepSeek" and is_critique:
                max_tokens = 100  # Very short technical critiques
            elif model_name == "Qwen3" and is_critique:
                max_tokens = 80   # Very short factual critiques  
            elif model_name in ["TNG DeepSeek", "Qwen3"]:
                max_tokens = 1500  # Shorter primary responses
            else:
                max_tokens = 4000  # Standard length for other models
            
            payload = {
                "model": openrouter_model,
                "messages": [
                    {
                        "role": "user",
                        "content": final_prompt
                    }
                ],
                "max_tokens": max_tokens,
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
                    
                    # Clean up special tokens from GPT-OSS output
                    if "GPT-OSS" in model_name:
                        tokens_to_remove = ["<|start|>", "<|assistant|>", "<|channel|>", "<|final|>", "<|message|>", "<|end|>", "assistant", "final", "channel"]
                        for token in tokens_to_remove:
                            response_text = response_text.replace(token, "")
                        response_text = response_text.strip()
                    
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
    
    async def refine_response_with_critique(self, 
                                          original_prompt: str,
                                          primary_model: str,
                                          original_response: str,
                                          chosen_critique: str,
                                          critique_model: str) -> ModelResponse:
        """
        Refine the primary model's response based on selected critique
        
        Args:
            original_prompt: The original user prompt
            primary_model: Name of the primary model to refine response
            original_response: Original response that needs refinement
            chosen_critique: The critique text from user's chosen model
            critique_model: Name of the model that provided the critique
            
        Returns:
            ModelResponse with refined response from primary model
        """
        logger.info(f"🔄 Refining {primary_model} response based on {critique_model}'s critique")
        
        # Create refinement prompt
        refinement_prompt = f"""ORIGINAL PROMPT: {original_prompt}

YOUR ORIGINAL RESPONSE: {original_response}

FEEDBACK FROM {critique_model}: {chosen_critique}

Please improve your original response by addressing the feedback above. Keep the same style and approach, but incorporate the suggestions to make it better. Provide only the improved response without any meta-commentary."""
        
        # Call the primary model again with refinement prompt
        refined_response = await self._call_openrouter_api(
            model_name=primary_model,
            prompt=refinement_prompt,
            is_critique=False,
            temperature=0.7
        )
        
        # Update response type to indicate it's refined
        refined_response.response_type = "refined"
        refined_response.metadata = refined_response.metadata or {}
        refined_response.metadata.update({
            "original_response_length": len(original_response),
            "critique_source": critique_model,
            "critique_text": chosen_critique,
            "is_refinement": True
        })
        
        logger.info(f"✨ Response refined: {len(refined_response.response_text)} chars")
        return refined_response

    async def orchestrate_with_user_refinement(self, 
                                             prompt: str,
                                             user_choice_callback = None) -> Dict[str, Any]:
        """
        Complete orchestration workflow with user-controlled refinement
        
        Args:
            prompt: Input prompt
            user_choice_callback: Optional callback function to get user's critique choice
                                 Should return tuple (chosen_critique_index, should_refine)
        
        Returns:
            Dictionary with complete workflow results including potential refinement
        """
        logger.info(f"🎭 Starting complete orchestration with refinement for: '{prompt[:50]}...'")
        
        # Step 1: Get initial orchestration with critiques
        initial_result = await self.orchestrate_with_critiques(prompt)
        
        if not initial_result.success or not initial_result.primary_response.success:
            logger.error("❌ Initial orchestration failed, cannot proceed with refinement")
            return {
                "stage": "initial_failed",
                "initial_result": initial_result,
                "refined_response": None,
                "user_choice": None
            }
        
        # Step 2: Present critiques to user (if callback provided)
        successful_critiques = [c for c in initial_result.critique_responses if c.success]
        
        if not successful_critiques:
            logger.warning("⚠️ No successful critiques available for refinement")
            return {
                "stage": "no_critiques",
                "initial_result": initial_result,
                "refined_response": None,
                "user_choice": None
            }
        
        user_choice = None
        refined_response = None
        
        # Step 3: Get user choice (if callback provided)
        if user_choice_callback:
            try:
                user_choice = user_choice_callback(successful_critiques)
                
                if user_choice and len(user_choice) == 2:
                    chosen_index, should_refine = user_choice
                    
                    if should_refine and 0 <= chosen_index < len(successful_critiques):
                        chosen_critique = successful_critiques[chosen_index]
                        
                        # Step 4: Refine response based on chosen critique
                        refined_response = await self.refine_response_with_critique(
                            original_prompt=prompt,
                            primary_model=initial_result.selected_model,
                            original_response=initial_result.primary_response.response_text,
                            chosen_critique=chosen_critique.response_text,
                            critique_model=chosen_critique.model_name
                        )
                        
                        logger.info(f"✅ Refinement completed using {chosen_critique.model_name}'s feedback")
                    
            except Exception as e:
                logger.error(f"❌ Error in user choice callback: {e}")
        
        return {
            "stage": "complete",
            "initial_result": initial_result,
            "refined_response": refined_response,
            "user_choice": user_choice,
            "available_critiques": successful_critiques
        }

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

def interactive_critique_selector(critiques: List[ModelResponse]) -> Tuple[int, bool]:
    """
    Interactive function to let user choose which critique to use for refinement
    
    Args:
        critiques: List of successful critique responses
        
    Returns:
        Tuple of (chosen_index, should_refine)
    """
    print("\n" + "="*60)
    print("🎯 PRIMARY RESPONSE COMPLETED! Now review critiques:")
    print("="*60)
    
    for i, critique in enumerate(critiques):
        print(f"\n📝 Critique {i+1} from {critique.model_name}:")
        print(f"   {critique.response_text[:200]}...")
        print(f"   [Confidence: {critique.confidence_score:.2f}, Latency: {critique.latency_ms}ms]")
    
    print("\n" + "="*60)
    print("🔄 REFINEMENT OPTIONS:")
    print("="*60)
    print("0. Skip refinement (use original response)")
    for i, critique in enumerate(critiques):
        print(f"{i+1}. Refine using {critique.model_name}'s feedback")
    
    while True:
        try:
            choice = input(f"\nChoose an option (0-{len(critiques)}): ").strip()
            choice_num = int(choice)
            
            if choice_num == 0:
                print("✅ Keeping original response without refinement")
                return (0, False)
            elif 1 <= choice_num <= len(critiques):
                chosen_critique = critiques[choice_num - 1]
                print(f"✅ Will refine using {chosen_critique.model_name}'s feedback")
                return (choice_num - 1, True)
            else:
                print(f"❌ Please enter a number between 0 and {len(critiques)}")
                
        except ValueError:
            print("❌ Please enter a valid number")
        except KeyboardInterrupt:
            print("\n❌ User cancelled, keeping original response")
            return (0, False)

def format_complete_result(workflow_result: Dict[str, Any]) -> str:
    """Format the complete workflow result for display"""
    stage = workflow_result["stage"]
    initial = workflow_result["initial_result"]
    refined = workflow_result["refined_response"]
    
    output = []
    output.append("🎭 COMPLETE ORCHESTRATION RESULT")
    output.append("="*50)
    
    # Primary response
    output.append(f"\n🤖 PRIMARY MODEL: {initial.selected_model}")
    output.append(f"Original Response: {initial.primary_response.response_text[:300]}...")
    
    # Critiques summary
    successful_critiques = [c for c in initial.critique_responses if c.success]
    output.append(f"\n📝 CRITIQUES: {len(successful_critiques)} models provided feedback")
    
    # Refinement result
    if refined and refined.success:
        output.append(f"\n✨ REFINED RESPONSE (improved by {refined.metadata.get('critique_source', 'unknown')}):")
        output.append(f"{refined.response_text}")
        output.append(f"\nImprovement: {len(refined.response_text)} chars vs {refined.metadata.get('original_response_length', 0)} chars original")
    else:
        output.append(f"\n📋 FINAL RESPONSE: Using original (no refinement applied)")
    
    # Summary
    total_cost = initial.total_cost_usd + (refined.cost_usd if refined else 0)
    total_time = initial.total_latency_ms + (refined.latency_ms if refined else 0)
    output.append(f"\n💰 Total Cost: ${total_cost:.4f}")
    output.append(f"⏱️ Total Time: {total_time}ms")
    output.append(f"🎯 Stage: {stage}")
    
    return "\n".join(output)

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
            print(f"Response: {result.primary_response.response_text}")
        
        print(f"\n📝 Critiques from {len(result.critique_responses)} other models:")
        for critique in result.critique_responses:
            status = "✅" if critique.success else "❌"
            print(f"{status} {critique.model_name}: {critique.response_text if critique.success else critique.error_message}")
        
        # Show UI-formatted result
        ui_data = format_for_ui(result)
        print(f"\n📊 Summary: {ui_data['summary']}")
        
        # Print stats
        orchestrator.print_stats()
        
        return result

async def example_with_refinement():
    """Example demonstrating the complete workflow with user-controlled refinement"""
    
    async with MultiModelOrchestrator() as orchestrator:
        
        # Test prompt that could benefit from refinement
        prompt = "Explain machine learning algorithms in simple terms for beginners"
        
        print(f"🎭 Starting complete orchestration workflow...")
        print(f"📝 Prompt: {prompt}")
        
        # Run complete workflow with interactive refinement
        workflow_result = await orchestrator.orchestrate_with_user_refinement(
            prompt=prompt,
            user_choice_callback=interactive_critique_selector
        )
        
        # Display complete result
        print(format_complete_result(workflow_result))
        
        # Print stats
        orchestrator.print_stats()
        
        return workflow_result

async def example_programmatic_refinement():
    """Example of programmatic refinement without user interaction"""
    
    async with MultiModelOrchestrator() as orchestrator:
        
        prompt = "Write a function to validate email addresses"
        
        # Automatic critique selection (e.g., always choose the first successful critique)
        def auto_selector(critiques):
            if critiques:
                print(f"🤖 Auto-selecting {critiques[0].model_name}'s critique for refinement")
                return (0, True)  # Choose first critique, do refine
            return (0, False)
        
        workflow_result = await orchestrator.orchestrate_with_user_refinement(
            prompt=prompt,
            user_choice_callback=auto_selector
        )
        
        print(format_complete_result(workflow_result))
        return workflow_result

if __name__ == "__main__":
    # Run example with interactive refinement
    print("🎯 Example 1: Interactive Refinement")
    asyncio.run(example_with_refinement())
    
    print("\n" + "="*70 + "\n")
    
    # Run example with programmatic refinement
    print("🤖 Example 2: Programmatic Refinement")
    asyncio.run(example_programmatic_refinement())
