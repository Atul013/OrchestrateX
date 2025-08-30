"""
Enhanced AI Provider Manager for OrchestrateX
Manages all AI providers and integrates with our model selector
"""

import os
import asyncio
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime

from . import AIProviderResponse, AIProviderError
from .openrouter_provider import OpenRouterProvider

class EnhancedProviderManager:
    """
    Enhanced provider manager that integrates with our ML model selector
    """
    
    def __init__(self):
        self.providers: Dict[str, Any] = {}
        self.initialized = False
        self.api_keys = self._load_api_keys()
    
    def _load_api_keys(self) -> Dict[str, str]:
        """Load API keys from environment variables"""
        return {
            "openrouter": os.getenv("OPENROUTER_API_KEY", ""),
            "openai": os.getenv("OPENAI_API_KEY", ""),
            "anthropic": os.getenv("ANTHROPIC_API_KEY", ""),
        }
    
    async def initialize(self):
        """Initialize all providers"""
        try:
            # Initialize OpenRouter provider if API key is available
            if self.api_keys.get("openrouter"):
                self.providers["openrouter"] = OpenRouterProvider(
                    self.api_keys["openrouter"]
                )
                logging.info("✅ OpenRouter provider initialized")
            else:
                logging.warning("⚠️ OpenRouter API key not found")
            
            # Test connections
            await self._test_all_providers()
            
            self.initialized = True
            logging.info("🚀 Provider manager initialized")
            
        except Exception as e:
            logging.error(f"❌ Failed to initialize provider manager: {e}")
            raise
    
    async def _test_all_providers(self):
        """Test all provider connections"""
        for provider_name, provider in self.providers.items():
            try:
                if hasattr(provider, 'test_connection'):
                    is_connected = await provider.test_connection()
                    if is_connected:
                        logging.info(f"✅ {provider_name} connection test passed")
                    else:
                        logging.warning(f"⚠️ {provider_name} connection test failed")
            except Exception as e:
                logging.error(f"❌ {provider_name} connection test error: {e}")
    
    async def generate_response(self, 
                              model_name: str, 
                              prompt: str, 
                              **kwargs) -> AIProviderResponse:
        """
        Generate response using the specified model
        Routes to appropriate provider based on model name
        """
        
        if not self.initialized:
            await self.initialize()
        
        try:
            # Route to OpenRouter for our 6 models
            if model_name in ["TNG DeepSeek", "GLM4.5", "GPT-OSS", 
                             "MoonshotAI Kimi", "Llama 4 Maverick", "Qwen3"]:
                
                if "openrouter" not in self.providers:
                    # Fallback: simulate response if no provider available
                    return await self._simulate_response(model_name, prompt)
                
                return await self.providers["openrouter"].generate_response(
                    model_name, prompt, **kwargs
                )
            
            else:
                raise AIProviderError("ProviderManager", f"Unknown model: {model_name}")
                
        except Exception as e:
            logging.error(f"❌ Failed to generate response with {model_name}: {e}")
            # Return simulated response as fallback
            return await self._simulate_response(model_name, prompt)
    
    async def _simulate_response(self, model_name: str, prompt: str) -> AIProviderResponse:
        """
        Simulate AI response for testing/fallback
        """
        
        # Simulate processing time
        await asyncio.sleep(0.5)
        
        # Generate simulated response based on model characteristics
        response_templates = {
            "TNG DeepSeek": "🧠 [DeepSeek] Advanced reasoning for: {prompt}",
            "GLM4.5": "🤖 [GLM4.5] Comprehensive analysis of: {prompt}",
            "GPT-OSS": "💡 [GPT-OSS] Detailed explanation of: {prompt}",
            "MoonshotAI Kimi": "🌙 [Kimi] Creative solution for: {prompt}",
            "Llama 4 Maverick": "🦙 [Llama] Thoughtful approach to: {prompt}",
            "Qwen3": "⚡ [Qwen3] Technical solution for: {prompt}"
        }
        
        template = response_templates.get(model_name, "🤖 [AI] Response to: {prompt}")
        response_text = template.format(prompt=prompt[:100] + "..." if len(prompt) > 100 else prompt)
        
        # Add realistic details based on prompt
        if "code" in prompt.lower() or "programming" in prompt.lower():
            response_text += "\n\n```python\n# Example implementation\ndef solution():\n    return 'Generated code'\n```"
        elif "explain" in prompt.lower():
            response_text += "\n\nThis involves several key concepts:\n1. Understanding the context\n2. Analyzing requirements\n3. Providing clear explanations"
        
        return AIProviderResponse(
            provider="Simulator",
            model_name=model_name,
            response_text=response_text,
            tokens_used=len(response_text.split()) * 1.3,  # Rough token estimate
            response_time_ms=500,
            cost_usd=0.001,  # Simulated cost
            confidence_score=0.85,
            metadata={
                "simulated": True,
                "reason": "API provider not available"
            }
        )
    
    async def get_model_capabilities(self, model_name: str) -> Dict[str, Any]:
        """Get capabilities and metadata for a specific model"""
        
        capabilities = {
            "TNG DeepSeek": {
                "specialties": ["reasoning", "analysis", "problem_solving"],
                "max_tokens": 4000,
                "languages": ["english", "chinese"],
                "strengths": ["logical reasoning", "mathematical problems"],
                "cost_tier": "medium"
            },
            "GLM4.5": {
                "specialties": ["general", "conversation", "analysis"],
                "max_tokens": 4000,
                "languages": ["english", "chinese"],
                "strengths": ["comprehensive answers", "multi-turn chat"],
                "cost_tier": "medium"
            },
            "GPT-OSS": {
                "specialties": ["general", "creative", "coding"],
                "max_tokens": 4000,
                "languages": ["english", "multilingual"],
                "strengths": ["versatility", "code generation"],
                "cost_tier": "low"
            },
            "MoonshotAI Kimi": {
                "specialties": ["creative", "writing", "analysis"],
                "max_tokens": 32000,
                "languages": ["english", "chinese"],
                "strengths": ["long context", "creative writing"],
                "cost_tier": "medium"
            },
            "Llama 4 Maverick": {
                "specialties": ["coding", "reasoning", "general"],
                "max_tokens": 4000,
                "languages": ["english", "multilingual"],
                "strengths": ["open source", "reliable performance"],
                "cost_tier": "low"
            },
            "Qwen3": {
                "specialties": ["coding", "technical", "analysis"],
                "max_tokens": 4000,
                "languages": ["english", "chinese"],
                "strengths": ["code generation", "technical accuracy"],
                "cost_tier": "medium"
            }
        }
        
        return capabilities.get(model_name, {})
    
    def get_available_models(self) -> List[str]:
        """Get list of all available models"""
        return ["TNG DeepSeek", "GLM4.5", "GPT-OSS", "MoonshotAI Kimi", "Llama 4 Maverick", "Qwen3"]
    
    async def batch_generate(self, 
                            requests: List[Dict[str, Any]]) -> List[AIProviderResponse]:
        """Generate multiple responses in parallel"""
        
        tasks = []
        for req in requests:
            task = self.generate_response(
                req["model_name"],
                req["prompt"],
                **req.get("kwargs", {})
            )
            tasks.append(task)
        
        return await asyncio.gather(*tasks, return_exceptions=True)
    
    async def close_all(self):
        """Close all providers"""
        for provider in self.providers.values():
            try:
                await provider.close()
            except Exception as e:
                logging.error(f"Error closing provider: {e}")

# Global provider manager instance
enhanced_provider_manager = EnhancedProviderManager()
