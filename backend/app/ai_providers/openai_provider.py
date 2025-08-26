"""
OpenAI Provider Implementation
"""

import time
from typing import Dict, Any
from openai import AsyncOpenAI
from . import BaseAIProvider, AIProviderResponse, AIProviderError

class OpenAIProvider(BaseAIProvider):
    """OpenAI API provider implementation"""
    
    def __init__(self, api_key: str, model_name: str = "gpt-4-turbo"):
        super().__init__(api_key, model_name)
        self.client = AsyncOpenAI(api_key=api_key)
        self.cost_per_input_token = 0.01 / 1000  # $0.01 per 1K tokens
        self.cost_per_output_token = 0.03 / 1000  # $0.03 per 1K tokens
    
    async def generate_response(self, prompt: str, **kwargs) -> AIProviderResponse:
        """Generate response using OpenAI API"""
        start_time = time.time()
        
        try:
            # Prepare the request
            messages = [{"role": "user", "content": prompt}]
            
            # Add system message if provided
            if "system_prompt" in kwargs:
                messages.insert(0, {"role": "system", "content": kwargs["system_prompt"]})
            
            # Make API call
            response = await self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                max_tokens=kwargs.get("max_tokens", 2000),
                temperature=kwargs.get("temperature", 0.7),
                top_p=kwargs.get("top_p", 1.0)
            )
            
            # Calculate metrics
            response_time_ms = int((time.time() - start_time) * 1000)
            
            # Extract response data
            message = response.choices[0].message.content
            input_tokens = response.usage.prompt_tokens
            output_tokens = response.usage.completion_tokens
            total_tokens = response.usage.total_tokens
            
            # Calculate cost
            cost = (input_tokens * self.cost_per_input_token + 
                   output_tokens * self.cost_per_output_token)
            
            return AIProviderResponse(
                provider="openai",
                model_name=self.model_name,
                response_text=message,
                tokens_used=total_tokens,
                response_time_ms=response_time_ms,
                cost_usd=cost,
                confidence_score=0.9,  # OpenAI doesn't provide confidence, use default
                metadata={
                    "input_tokens": input_tokens,
                    "output_tokens": output_tokens,
                    "finish_reason": response.choices[0].finish_reason
                }
            )
            
        except Exception as e:
            raise AIProviderError(
                provider="openai",
                error_msg=str(e),
                status_code=getattr(e, 'status_code', None)
            )
    
    async def health_check(self) -> bool:
        """Check if OpenAI API is accessible"""
        try:
            await self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=1
            )
            return True
        except Exception:
            return False
    
    async def close(self):
        """Close OpenAI client"""
        await self.client.close()
