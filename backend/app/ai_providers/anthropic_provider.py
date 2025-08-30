"""
Anthropic (Claude) Provider Implementation
"""

import time
from typing import Dict, Any
from anthropic import AsyncAnthropic
from . import BaseAIProvider, AIProviderResponse, AIProviderError

class AnthropicProvider(BaseAIProvider):
    """Anthropic Claude API provider implementation"""
    
    def __init__(self, api_key: str, model_name: str = "claude-3-5-sonnet-20241022"):
        super().__init__(api_key, model_name)
        self.client = AsyncAnthropic(api_key=api_key)
        self.cost_per_input_token = 0.015 / 1000  # $0.015 per 1K tokens
        self.cost_per_output_token = 0.075 / 1000  # $0.075 per 1K tokens
    
    async def generate_response(self, prompt: str, **kwargs) -> AIProviderResponse:
        """Generate response using Anthropic Claude API"""
        start_time = time.time()
        
        try:
            # Prepare the message
            messages = [{"role": "user", "content": prompt}]
            
            # Add system prompt if provided
            system_prompt = kwargs.get("system_prompt", "You are a helpful AI assistant.")
            
            # Make API call
            response = await self.client.messages.create(
                model=self.model_name,
                max_tokens=kwargs.get("max_tokens", 2000),
                temperature=kwargs.get("temperature", 0.7),
                system=system_prompt,
                messages=messages
            )
            
            # Calculate metrics
            response_time_ms = int((time.time() - start_time) * 1000)
            
            # Extract response data
            message = response.content[0].text
            input_tokens = response.usage.input_tokens
            output_tokens = response.usage.output_tokens
            total_tokens = input_tokens + output_tokens
            
            # Calculate cost
            cost = (input_tokens * self.cost_per_input_token + 
                   output_tokens * self.cost_per_output_token)
            
            return AIProviderResponse(
                provider="anthropic",
                model_name=self.model_name,
                response_text=message,
                tokens_used=total_tokens,
                response_time_ms=response_time_ms,
                cost_usd=cost,
                confidence_score=0.85,  # Claude doesn't provide confidence, use default
                metadata={
                    "input_tokens": input_tokens,
                    "output_tokens": output_tokens,
                    "stop_reason": response.stop_reason
                }
            )
            
        except Exception as e:
            raise AIProviderError(
                provider="anthropic",
                error_msg=str(e),
                status_code=getattr(e, 'status_code', None)
            )
    
    async def health_check(self) -> bool:
        """Check if Anthropic API is accessible"""
        try:
            await self.client.messages.create(
                model=self.model_name,
                max_tokens=1,
                messages=[{"role": "user", "content": "Hi"}]
            )
            return True
        except Exception:
            return False
    
    async def close(self):
        """Close Anthropic client"""
        await self.client.close()
