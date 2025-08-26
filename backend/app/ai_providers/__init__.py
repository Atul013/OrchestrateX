"""
AI Provider Base Classes and Configuration
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from pydantic import BaseModel
import httpx
import asyncio
from datetime import datetime

class AIProviderResponse(BaseModel):
    """Standard response format from AI providers"""
    provider: str
    model_name: str
    response_text: str
    tokens_used: int
    response_time_ms: int
    cost_usd: float
    confidence_score: Optional[float] = None
    metadata: Dict[str, Any] = {}

class AIProviderError(Exception):
    """Custom exception for AI provider errors"""
    def __init__(self, provider: str, error_msg: str, status_code: Optional[int] = None):
        self.provider = provider
        self.error_msg = error_msg
        self.status_code = status_code
        super().__init__(f"{provider}: {error_msg}")

class BaseAIProvider(ABC):
    """Abstract base class for all AI providers"""
    
    def __init__(self, api_key: str, model_name: str):
        self.api_key = api_key
        self.model_name = model_name
        self.client = httpx.AsyncClient(timeout=30.0)
    
    @abstractmethod
    async def generate_response(self, prompt: str, **kwargs) -> AIProviderResponse:
        """Generate response from the AI model"""
        pass
    
    @abstractmethod
    async def health_check(self) -> bool:
        """Check if the provider is available"""
        pass
    
    async def close(self):
        """Clean up resources"""
        await self.client.aclose()

class AIProviderManager:
    """Manages all AI providers and their configurations"""
    
    def __init__(self):
        self.providers: Dict[str, BaseAIProvider] = {}
        self.api_keys: Dict[str, str] = {
            # Default empty keys - should be set via environment variables
            "openai": "",
            "anthropic": "",
            "xai": "",
            "alibaba": "",
            "meta": "",
            "mistral": ""
        }
    
    def set_api_key(self, provider: str, api_key: str):
        """Set API key for a provider"""
        self.api_keys[provider] = api_key
    
    def get_provider(self, model_name: str) -> Optional[BaseAIProvider]:
        """Get provider instance for a model"""
        return self.providers.get(model_name)
    
    async def initialize_providers(self):
        """Initialize all available providers"""
        from .openai_provider import OpenAIProvider
        from .anthropic_provider import AnthropicProvider
        from .xai_provider import XAIProvider
        
        # Initialize providers with API keys
        if self.api_keys["openai"]:
            self.providers["gpt4"] = OpenAIProvider(
                api_key=self.api_keys["openai"],
                model_name="gpt-4-turbo"
            )
        
        if self.api_keys["anthropic"]:
            self.providers["claude"] = AnthropicProvider(
                api_key=self.api_keys["anthropic"],
                model_name="claude-3-5-sonnet-20241022"
            )
        
        if self.api_keys["xai"]:
            self.providers["grok"] = XAIProvider(
                api_key=self.api_keys["xai"],
                model_name="grok-1"
            )
    
    async def check_all_providers_health(self) -> Dict[str, bool]:
        """Check health of all providers"""
        results = {}
        for model_name, provider in self.providers.items():
            try:
                results[model_name] = await provider.health_check()
            except Exception:
                results[model_name] = False
        return results
    
    async def close_all(self):
        """Close all provider connections"""
        for provider in self.providers.values():
            await provider.close()

# Global provider manager instance
provider_manager = AIProviderManager()
