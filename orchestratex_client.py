#!/usr/bin/env python3
"""
OrchestrateX Client Script

A comprehensive Python client that:
1. Sends prompts to model selector REST API
2. Routes to predicted AI model via OpenRouter
3. Handles fallbacks and error recovery
4. Processes prompts in batch
5. Logs all interactions with detailed metrics

Usage:
    python orchestratex_client.py --prompt "Your question here"
    python orchestratex_client.py --batch prompts.txt
    python orchestratex_client.py --interactive
"""

import asyncio
import aiohttp
import argparse
import json
import logging
import time
import os
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('orchestratex_client.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class ModelResponse:
    """Response from AI model"""
    model_name: str
    response_text: str
    tokens_used: int
    response_time_ms: int
    cost_usd: float
    success: bool
    error_message: Optional[str] = None
    provider: str = "unknown"
    metadata: Dict[str, Any] = None

@dataclass
class OrchestrationResult:
    """Complete orchestration result"""
    original_prompt: str
    selected_model: str
    confidence_scores: Dict[str, float]
    final_response: ModelResponse
    fallback_attempts: List[str]
    total_time_ms: int
    total_cost_usd: float
    success: bool

class OrchestrateXClient:
    """
    Comprehensive client for OrchestrateX system
    """
    
    def __init__(self, 
                 model_selector_url: str = "http://localhost:5000",
                 openrouter_api_key: str = None,
                 timeout: int = 30):
        """
        Initialize the OrchestrateX client
        
        Args:
            model_selector_url: URL of the model selector API
            openrouter_api_key: OpenRouter API key for AI model access
            timeout: Request timeout in seconds
        """
        self.model_selector_url = model_selector_url
        self.openrouter_api_key = openrouter_api_key or os.getenv("OPENROUTER_API_KEY")
        self.timeout = timeout
        
        # OpenRouter model mappings
        self.model_mappings = {
            "TNG DeepSeek": "deepseek/deepseek-r1",
            "GLM4.5": "zhipuai/glm-4-plus", 
            "GPT-OSS": "openai/gpt-4o-mini",
            "MoonshotAI Kimi": "moonshot/moonshot-v1-32k",
            "Llama 4 Maverick": "meta-llama/llama-3.2-90b-vision-instruct",
            "Qwen3": "qwen/qwen-2.5-coder-32b-instruct"
        }
        
        # Model fallback order (from most reliable to least)
        self.fallback_order = [
            "GPT-OSS",
            "Llama 4 Maverick", 
            "TNG DeepSeek",
            "GLM4.5",
            "Qwen3",
            "MoonshotAI Kimi"
        ]
        
        self.session = None
        self.stats = {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "total_cost": 0.0,
            "total_time_ms": 0,
            "model_usage": {}
        }
    
    async def __aenter__(self):
        """Async context manager entry"""
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=self.timeout)
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()
    
    async def get_model_prediction(self, prompt: str) -> Tuple[str, Dict[str, float]]:
        """
        Get model prediction from the model selector API
        
        Args:
            prompt: Input prompt to analyze
            
        Returns:
            Tuple of (best_model, confidence_scores)
        """
        try:
            logger.info(f"🎯 Getting model prediction for prompt: '{prompt[:50]}...'")
            
            async with self.session.post(
                f"{self.model_selector_url}/predict",
                json={"prompt": prompt},
                headers={"Content-Type": "application/json"}
            ) as response:
                
                if response.status == 200:
                    data = await response.json()
                    best_model = data["best_model"]
                    confidence_scores = data["confidence_scores"]
                    
                    logger.info(f"✅ Model selection: {best_model} (confidence: {data['prediction_confidence']:.3f})")
                    return best_model, confidence_scores
                else:
                    error_text = await response.text()
                    logger.error(f"❌ Model selector API error {response.status}: {error_text}")
                    raise Exception(f"Model selector API error: {error_text}")
                    
        except Exception as e:
            logger.error(f"❌ Failed to get model prediction: {e}")
            # Fallback to default model
            return "GPT-OSS", {"GPT-OSS": 0.5}
    
    async def call_ai_model(self, 
                           model_name: str, 
                           prompt: str,
                           temperature: float = 0.7) -> ModelResponse:
        """
        Call AI model via OpenRouter API
        
        Args:
            model_name: Name of the AI model
            prompt: Input prompt
            temperature: Model temperature setting
            
        Returns:
            ModelResponse with result
        """
        if not self.openrouter_api_key:
            logger.warning("⚠️ No OpenRouter API key - using simulation")
            return await self._simulate_model_response(model_name, prompt)
        
        if model_name not in self.model_mappings:
            logger.error(f"❌ Unknown model: {model_name}")
            return ModelResponse(
                model_name=model_name,
                response_text="",
                tokens_used=0,
                response_time_ms=0,
                cost_usd=0.0,
                success=False,
                error_message=f"Unknown model: {model_name}"
            )
        
        try:
            start_time = time.time()
            openrouter_model = self.model_mappings[model_name]
            
            logger.info(f"🤖 Calling {model_name} via OpenRouter...")
            
            headers = {
                "Authorization": f"Bearer {self.openrouter_api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://orchestratex.app",
                "X-Title": "OrchestrateX Client"
            }
            
            payload = {
                "model": openrouter_model,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
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
                response_time_ms = int((end_time - start_time) * 1000)
                
                if response.status == 200:
                    data = await response.json()
                    
                    if not data.get("choices") or not data["choices"][0].get("message"):
                        raise Exception("Invalid response format from OpenRouter")
                    
                    response_text = data["choices"][0]["message"]["content"]
                    usage = data.get("usage", {})
                    tokens_used = usage.get("total_tokens", 0)
                    
                    # Estimate cost (rough approximation)
                    cost_usd = (tokens_used / 1000) * 0.002  # $0.002 per 1K tokens average
                    
                    logger.info(f"✅ {model_name} response: {len(response_text)} chars, {tokens_used} tokens, ${cost_usd:.4f}")
                    
                    return ModelResponse(
                        model_name=model_name,
                        response_text=response_text,
                        tokens_used=tokens_used,
                        response_time_ms=response_time_ms,
                        cost_usd=cost_usd,
                        success=True,
                        provider="OpenRouter",
                        metadata={
                            "openrouter_model": openrouter_model,
                            "finish_reason": data["choices"][0].get("finish_reason"),
                            "prompt_tokens": usage.get("prompt_tokens", 0),
                            "completion_tokens": usage.get("completion_tokens", 0)
                        }
                    )
                else:
                    error_text = await response.text()
                    logger.error(f"❌ OpenRouter API error {response.status}: {error_text}")
                    raise Exception(f"OpenRouter API error: {error_text}")
                    
        except Exception as e:
            logger.error(f"❌ Failed to call {model_name}: {e}")
            return ModelResponse(
                model_name=model_name,
                response_text="",
                tokens_used=0,
                response_time_ms=int((time.time() - start_time) * 1000) if 'start_time' in locals() else 0,
                cost_usd=0.0,
                success=False,
                error_message=str(e),
                provider="OpenRouter"
            )
    
    async def _simulate_model_response(self, model_name: str, prompt: str) -> ModelResponse:
        """Simulate AI model response for testing"""
        
        await asyncio.sleep(0.5)  # Simulate API latency
        
        response_templates = {
            "TNG DeepSeek": "🧠 [DeepSeek Simulation] Advanced reasoning response to: {prompt}",
            "GLM4.5": "🤖 [GLM4.5 Simulation] Comprehensive analysis of: {prompt}",
            "GPT-OSS": "💡 [GPT-OSS Simulation] Detailed explanation of: {prompt}",
            "MoonshotAI Kimi": "🌙 [Kimi Simulation] Creative solution for: {prompt}",
            "Llama 4 Maverick": "🦙 [Llama Simulation] Thoughtful approach to: {prompt}",
            "Qwen3": "⚡ [Qwen3 Simulation] Technical solution for: {prompt}"
        }
        
        template = response_templates.get(model_name, "🤖 [AI Simulation] Response to: {prompt}")
        response_text = template.format(prompt=prompt[:100] + "..." if len(prompt) > 100 else prompt)
        
        # Add context-specific content
        if any(keyword in prompt.lower() for keyword in ["code", "programming", "function"]):
            response_text += "\n\n```python\n# Simulated code example\ndef example_function():\n    return 'This is a simulated response'\n```"
        
        tokens_used = len(response_text.split()) * 1.3
        
        return ModelResponse(
            model_name=model_name,
            response_text=response_text,
            tokens_used=int(tokens_used),
            response_time_ms=500,
            cost_usd=0.001,
            success=True,
            provider="Simulator",
            metadata={"simulated": True}
        )
    
    async def orchestrate_prompt(self, prompt: str) -> OrchestrationResult:
        """
        Complete orchestration workflow for a single prompt
        
        Args:
            prompt: Input prompt to process
            
        Returns:
            OrchestrationResult with complete processing details
        """
        start_time = time.time()
        fallback_attempts = []
        total_cost = 0.0
        
        self.stats["total_requests"] += 1
        
        try:
            logger.info(f"🎭 Starting orchestration for: '{prompt[:50]}...'")
            
            # Step 1: Get model prediction
            selected_model, confidence_scores = await self.get_model_prediction(prompt)
            
            # Step 2: Try selected model
            response = await self.call_ai_model(selected_model, prompt)
            total_cost += response.cost_usd
            
            # Step 3: Implement fallback if needed
            if not response.success:
                logger.warning(f"⚠️ Primary model {selected_model} failed, trying fallbacks...")
                fallback_attempts.append(selected_model)
                
                # Try fallback models in order
                for fallback_model in self.fallback_order:
                    if fallback_model != selected_model:
                        logger.info(f"🔄 Trying fallback model: {fallback_model}")
                        fallback_attempts.append(fallback_model)
                        
                        response = await self.call_ai_model(fallback_model, prompt)
                        total_cost += response.cost_usd
                        
                        if response.success:
                            logger.info(f"✅ Fallback successful with {fallback_model}")
                            break
                else:
                    logger.error("❌ All fallback models failed")
            
            end_time = time.time()
            total_time_ms = int((end_time - start_time) * 1000)
            
            # Update stats
            if response.success:
                self.stats["successful_requests"] += 1
            else:
                self.stats["failed_requests"] += 1
            
            self.stats["total_cost"] += total_cost
            self.stats["total_time_ms"] += total_time_ms
            
            model_used = response.model_name if response.success else "failed"
            self.stats["model_usage"][model_used] = self.stats["model_usage"].get(model_used, 0) + 1
            
            return OrchestrationResult(
                original_prompt=prompt,
                selected_model=selected_model,
                confidence_scores=confidence_scores,
                final_response=response,
                fallback_attempts=fallback_attempts,
                total_time_ms=total_time_ms,
                total_cost_usd=total_cost,
                success=response.success
            )
            
        except Exception as e:
            logger.error(f"❌ Orchestration failed: {e}")
            self.stats["failed_requests"] += 1
            
            return OrchestrationResult(
                original_prompt=prompt,
                selected_model="unknown",
                confidence_scores={},
                final_response=ModelResponse(
                    model_name="error",
                    response_text="",
                    tokens_used=0,
                    response_time_ms=0,
                    cost_usd=0.0,
                    success=False,
                    error_message=str(e)
                ),
                fallback_attempts=[],
                total_time_ms=int((time.time() - start_time) * 1000),
                total_cost_usd=0.0,
                success=False
            )
    
    async def process_batch(self, prompts: List[str], max_concurrent: int = 3) -> List[OrchestrationResult]:
        """
        Process multiple prompts in batch with concurrency control
        
        Args:
            prompts: List of prompts to process
            max_concurrent: Maximum concurrent requests
            
        Returns:
            List of OrchestrationResult
        """
        logger.info(f"📊 Processing batch of {len(prompts)} prompts (max concurrent: {max_concurrent})")
        
        semaphore = asyncio.Semaphore(max_concurrent)
        
        async def process_with_semaphore(prompt):
            async with semaphore:
                return await self.orchestrate_prompt(prompt)
        
        tasks = [process_with_semaphore(prompt) for prompt in prompts]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Handle exceptions
        processed_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error(f"❌ Batch item {i} failed: {result}")
                processed_results.append(OrchestrationResult(
                    original_prompt=prompts[i],
                    selected_model="error",
                    confidence_scores={},
                    final_response=ModelResponse(
                        model_name="error",
                        response_text="",
                        tokens_used=0,
                        response_time_ms=0,
                        cost_usd=0.0,
                        success=False,
                        error_message=str(result)
                    ),
                    fallback_attempts=[],
                    total_time_ms=0,
                    total_cost_usd=0.0,
                    success=False
                ))
            else:
                processed_results.append(result)
        
        logger.info(f"✅ Batch processing completed: {sum(1 for r in processed_results if r.success)}/{len(prompts)} successful")
        return processed_results
    
    def print_stats(self):
        """Print client statistics"""
        print("\n📊 OrchestrateX Client Statistics")
        print("=" * 40)
        print(f"Total Requests: {self.stats['total_requests']}")
        print(f"Successful: {self.stats['successful_requests']}")
        print(f"Failed: {self.stats['failed_requests']}")
        print(f"Success Rate: {(self.stats['successful_requests']/max(self.stats['total_requests'], 1)*100):.1f}%")
        print(f"Total Cost: ${self.stats['total_cost']:.4f}")
        print(f"Average Time: {(self.stats['total_time_ms']/max(self.stats['total_requests'], 1)):.0f}ms")
        
        if self.stats['model_usage']:
            print("\nModel Usage:")
            for model, count in self.stats['model_usage'].items():
                print(f"  {model}: {count}")
    
    def save_results(self, results: List[OrchestrationResult], filename: str = None):
        """Save results to JSON file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"orchestratex_results_{timestamp}.json"
        
        data = []
        for result in results:
            data.append({
                "prompt": result.original_prompt,
                "selected_model": result.selected_model,
                "confidence_scores": result.confidence_scores,
                "response": result.final_response.response_text,
                "success": result.success,
                "tokens_used": result.final_response.tokens_used,
                "response_time_ms": result.total_time_ms,
                "cost_usd": result.total_cost_usd,
                "fallback_attempts": result.fallback_attempts,
                "error": result.final_response.error_message
            })
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"💾 Results saved to {filename}")

async def main():
    """Main function for CLI usage"""
    parser = argparse.ArgumentParser(description="OrchestrateX Client")
    parser.add_argument("--prompt", "-p", help="Single prompt to process")
    parser.add_argument("--batch", "-b", help="File containing prompts (one per line)")
    parser.add_argument("--interactive", "-i", action="store_true", help="Interactive mode")
    parser.add_argument("--model-selector-url", default="http://localhost:5000", help="Model selector API URL")
    parser.add_argument("--openrouter-key", help="OpenRouter API key")
    parser.add_argument("--max-concurrent", type=int, default=3, help="Max concurrent requests for batch")
    parser.add_argument("--output", "-o", help="Output file for results")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose logging")
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    async with OrchestrateXClient(
        model_selector_url=args.model_selector_url,
        openrouter_api_key=args.openrouter_key
    ) as client:
        
        results = []
        
        if args.prompt:
            # Single prompt mode
            result = await client.orchestrate_prompt(args.prompt)
            results.append(result)
            
            print(f"\n🎯 Selected Model: {result.selected_model}")
            print(f"💬 Response: {result.final_response.response_text}")
            print(f"⏱️ Time: {result.total_time_ms}ms")
            print(f"💰 Cost: ${result.total_cost_usd:.4f}")
            
        elif args.batch:
            # Batch mode
            if not Path(args.batch).exists():
                print(f"❌ File not found: {args.batch}")
                return
            
            with open(args.batch, 'r', encoding='utf-8') as f:
                prompts = [line.strip() for line in f if line.strip()]
            
            results = await client.process_batch(prompts, args.max_concurrent)
            
            print(f"\n📊 Batch Results ({len(results)} prompts):")
            for i, result in enumerate(results, 1):
                status = "✅" if result.success else "❌"
                print(f"{i}. {status} {result.selected_model} - {result.total_time_ms}ms - ${result.total_cost_usd:.4f}")
        
        elif args.interactive:
            # Interactive mode
            print("🎭 OrchestrateX Interactive Mode")
            print("Type 'quit' to exit, 'stats' for statistics")
            
            while True:
                try:
                    prompt = input("\n💬 Enter prompt: ").strip()
                    
                    if prompt.lower() in ['quit', 'exit']:
                        break
                    elif prompt.lower() == 'stats':
                        client.print_stats()
                        continue
                    elif not prompt:
                        continue
                    
                    result = await client.orchestrate_prompt(prompt)
                    results.append(result)
                    
                    print(f"\n🎯 Model: {result.selected_model}")
                    if result.success:
                        print(f"💬 Response: {result.final_response.response_text}")
                    else:
                        print(f"❌ Error: {result.final_response.error_message}")
                    print(f"⏱️ Time: {result.total_time_ms}ms | 💰 Cost: ${result.total_cost_usd:.4f}")
                    
                except KeyboardInterrupt:
                    break
                except Exception as e:
                    print(f"❌ Error: {e}")
        
        else:
            print("❌ Please specify --prompt, --batch, or --interactive mode")
            parser.print_help()
            return
        
        # Show final stats
        client.print_stats()
        
        # Save results if requested
        if args.output and results:
            client.save_results(results, args.output)

if __name__ == "__main__":
    asyncio.run(main())
