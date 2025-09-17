"""
OpenRouter Provider for OrchestrateX
Integrates with OpenRouter.ai for multiple AI models
"""

import asyncio
import httpx
from typing import Dict, Any, Optional
from datetime import datetime
import logging

from . import AIProviderResponse, AIProviderError, BaseAIProvider

class OpenRouterProvider(BaseAIProvider):
    """OpenRouter provider for multiple AI models"""
    
    # Model configurations for our 6 models
    MODEL_CONFIGS = {
        "TNG DeepSeek": {
            "id": "deepseek/deepseek-r1",
            "max_tokens": 4000,
            "cost_per_1k_tokens": 0.002
        },
        "GLM4.5": {
            "id": "zhipuai/glm-4-plus",
            "max_tokens": 4000,
            "cost_per_1k_tokens": 0.003
        },
        "GPT-OSS": {
            "id": "openai/gpt-4o-mini",
            "max_tokens": 4000,
            "cost_per_1k_tokens": 0.001
        },
        "MoonshotAI Kimi": {
            "id": "moonshot/moonshot-v1-32k",
            "max_tokens": 4000,
            "cost_per_1k_tokens": 0.002
        },
        "Llama 4 Maverick": {
            "id": "meta-llama/llama-3.2-90b-vision-instruct",
            "max_tokens": 4000,
            "cost_per_1k_tokens": 0.0015
        },
        "Qwen3": {
            "id": "qwen/qwen-2.5-coder-32b-instruct",
            "max_tokens": 4000,
            "cost_per_1k_tokens": 0.002
        }
    }
    
    def __init__(self, api_key: str):
        """Initialize OpenRouter provider"""
        super().__init__("OpenRouter")
        self.api_key = api_key
        self.base_url = "https://openrouter.ai/api/v1"
        self.client = httpx.AsyncClient(
            timeout=30.0,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://orchestratex.app",
                "X-Title": "OrchestrateX"
            }
        )
    
    async def generate_response(self, 
                              model_name: str, 
                              prompt: str, 
                              **kwargs) -> AIProviderResponse:
        """Generate response using OpenRouter API"""
        
        if model_name not in self.MODEL_CONFIGS:
            raise AIProviderError(
                self.provider_name, 
                f"Unsupported model: {model_name}"
            )
        
        model_config = self.MODEL_CONFIGS[model_name]
        
        try:
            start_time = datetime.utcnow()
            
            # Prepare request payload
            payload = {
                "model": model_config["id"],
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "max_tokens": model_config["max_tokens"],
                "temperature": kwargs.get("temperature", 0.7),
                "top_p": kwargs.get("top_p", 0.9)
            }
            
            # Make API call
            response = await self.client.post(
                f"{self.base_url}/chat/completions",
                json=payload
            )
            
            end_time = datetime.utcnow()
            response_time_ms = int((end_time - start_time).total_seconds() * 1000)
            
            if response.status_code != 200:
                raise AIProviderError(
                    self.provider_name,
                    f"API error: {response.text}",
                    response.status_code
                )
            
            data = response.json()
            
            # Extract response
            if not data.get("choices") or not data["choices"][0].get("message"):
                raise AIProviderError(
                    self.provider_name,
                    "Invalid response format from API"
                )
            
            response_text = data["choices"][0]["message"]["content"]
            tokens_used = data.get("usage", {}).get("total_tokens", 0)
            
            # Calculate cost
            cost_usd = (tokens_used / 1000) * model_config["cost_per_1k_tokens"]
            
            return AIProviderResponse(
                provider=self.provider_name,
                model_name=model_name,
                response_text=response_text,
                tokens_used=tokens_used,
                response_time_ms=response_time_ms,
                cost_usd=cost_usd,
                metadata={
                    "model_id": model_config["id"],
                    "finish_reason": data["choices"][0].get("finish_reason"),
                    "prompt_tokens": data.get("usage", {}).get("prompt_tokens", 0),
                    "completion_tokens": data.get("usage", {}).get("completion_tokens", 0)
                }
            )
            
        except httpx.TimeoutException:
            raise AIProviderError(
                self.provider_name,
                f"Timeout calling {model_name}"
            )
        except Exception as e:
            if isinstance(e, AIProviderError):
                raise
            raise AIProviderError(
                self.provider_name,
                f"Unexpected error: {str(e)}"
            )
    
    async def test_connection(self) -> bool:
        """Test connection to OpenRouter API"""
        try:
            response = await self.client.get(f"{self.base_url}/models")
            return response.status_code == 200
        except:
            return False
    
    def get_available_models(self) -> List[str]: # pyright: ignore[reportUndefinedVariable]
        """Get list of available models"""
        return list(self.MODEL_CONFIGS.keys())
    
    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()
