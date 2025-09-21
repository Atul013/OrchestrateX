#!/usr/bin/env python3
"""
Rate Limit Detection and Response Handler for OrchestrateX
Integrates with API Key Rotation Manager to handle OpenRouter API limits
"""

import requests
import json
import time
from typing import Dict, Tuple, Optional, Any
import logging
from datetime import datetime

# Import our rotation manager
from api_key_rotation import rotation_manager, get_api_key, handle_rate_limit, increment_usage

logger = logging.getLogger(__name__)

class RateLimitAwareAPIClient:
    """
    Enhanced API client with automatic rate limit detection and key rotation
    """
    
    def __init__(self):
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        self.default_headers = {
            "Content-Type": "application/json",
            "HTTP-Referer": "https://orchestratex.me",
            "X-Title": "OrchestrateX"
        }
        
    def _is_rate_limit_error(self, response: requests.Response) -> bool:
        """Check if response indicates rate limiting"""
        if response.status_code == 429:
            return True
        
        # Check for rate limit indicators in response body
        try:
            data = response.json()
            error_message = data.get('error', {}).get('message', '').lower()
            if any(keyword in error_message for keyword in [
                'rate limit', 'too many requests', 'quota exceeded', 
                'limit exceeded', 'rate exceeded'
            ]):
                return True
        except:
            pass
        
        return False
    
    def _extract_rate_limit_info(self, response: requests.Response) -> Dict:
        """Extract rate limit information from response headers and body"""
        rate_limit_info = {
            'status_code': response.status_code,
            'headers': {}
        }
        
        # Common rate limit headers
        rate_limit_headers = [
            'x-ratelimit-limit', 'x-ratelimit-remaining', 'x-ratelimit-reset',
            'retry-after', 'x-ratelimit-limit-requests', 'x-ratelimit-remaining-requests'
        ]
        
        for header in rate_limit_headers:
            if header in response.headers:
                rate_limit_info['headers'][header] = response.headers[header]
        
        # Try to extract error details from response body
        try:
            data = response.json()
            if 'error' in data:
                rate_limit_info['error_details'] = data['error']
        except:
            rate_limit_info['error_details'] = {'message': response.text[:200]}
        
        return rate_limit_info
    
    def call_openrouter_api(self, provider: str, model_id: str, prompt: str, max_tokens: int = 2000, 
                           temperature: float = 0.7, max_retries: int = 3) -> Dict:
        """
        Call OpenRouter API with automatic key rotation on rate limits
        
        Args:
            provider: Provider name (e.g., 'GLM45', 'GPTOSS')
            model_id: Model identifier for OpenRouter
            prompt: The prompt to send
            max_tokens: Maximum tokens to generate
            temperature: Temperature for generation
            max_retries: Maximum number of key rotations to attempt
        
        Returns:
            Dict with success status, response data, and metadata
        """
        
        for attempt in range(max_retries + 1):
            # Get current API key for this provider
            api_key = get_api_key(provider)
            if not api_key:
                return {
                    'success': False,
                    'error': f'No API key available for provider {provider}',
                    'provider': provider,
                    'attempt': attempt
                }
            
            # Prepare request
            headers = self.default_headers.copy()
            headers["Authorization"] = f"Bearer {api_key}"
            
            payload = {
                "model": model_id,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": max_tokens,
                "temperature": temperature
            }
            
            start_time = time.time()
            
            try:
                logger.info(f"🔄 Calling {provider} (attempt {attempt + 1}/{max_retries + 1})")
                response = requests.post(self.base_url, headers=headers, json=payload, timeout=30)
                
                # Increment usage counter
                increment_usage(provider)
                
                response_time = time.time() - start_time
                
                # Check for rate limiting
                if self._is_rate_limit_error(response):
                    rate_limit_info = self._extract_rate_limit_info(response)
                    logger.warning(f"⚠️ Rate limit detected for {provider}: {rate_limit_info}")
                    
                    # Handle rate limit and try rotation
                    rotation_success = handle_rate_limit(provider, rate_limit_info)
                    
                    if not rotation_success and attempt == max_retries:
                        return {
                            'success': False,
                            'error': f'All API keys for {provider} are rate limited',
                            'rate_limit_info': rate_limit_info,
                            'provider': provider,
                            'attempts': attempt + 1
                        }
                    
                    # If we have more attempts or rotation was successful, continue to next iteration
                    if rotation_success or attempt < max_retries:
                        wait_time = min(2 ** attempt, 10)  # Exponential backoff, max 10 seconds
                        logger.info(f"🕐 Waiting {wait_time}s before retry...")
                        time.sleep(wait_time)
                        continue
                
                # Check for other HTTP errors
                if not response.ok:
                    error_data = {
                        'status_code': response.status_code,
                        'response_text': response.text[:500]
                    }
                    
                    try:
                        error_json = response.json()
                        error_data['error_details'] = error_json
                    except:
                        pass
                    
                    return {
                        'success': False,
                        'error': f'HTTP error {response.status_code}',
                        'error_data': error_data,
                        'provider': provider,
                        'attempt': attempt + 1
                    }
                
                # Success! Parse response
                try:
                    result = response.json()
                    
                    # Extract the generated text
                    if 'choices' in result and len(result['choices']) > 0:
                        generated_text = result['choices'][0]['message']['content']
                        
                        # Calculate tokens and cost (rough estimates)
                        input_tokens = len(prompt.split()) * 1.3  # Rough estimate
                        output_tokens = len(generated_text.split()) * 1.3
                        
                        return {
                            'success': True,
                            'response': generated_text,
                            'metadata': {
                                'provider': provider,
                                'model_id': model_id,
                                'input_tokens': int(input_tokens),
                                'output_tokens': int(output_tokens),
                                'total_tokens': int(input_tokens + output_tokens),
                                'response_time_ms': int(response_time * 1000),
                                'attempt': attempt + 1,
                                'timestamp': datetime.now().isoformat()
                            },
                            'raw_response': result
                        }
                    else:
                        return {
                            'success': False,
                            'error': 'No choices in API response',
                            'raw_response': result,
                            'provider': provider,
                            'attempt': attempt + 1
                        }
                        
                except json.JSONDecodeError as e:
                    return {
                        'success': False,
                        'error': f'Failed to parse JSON response: {e}',
                        'response_text': response.text[:500],
                        'provider': provider,
                        'attempt': attempt + 1
                    }
                    
            except requests.exceptions.Timeout:
                logger.warning(f"⏰ Timeout for {provider} attempt {attempt + 1}")
                if attempt == max_retries:
                    return {
                        'success': False,
                        'error': 'Request timeout after all retries',
                        'provider': provider,
                        'attempts': attempt + 1
                    }
                
                # Wait before retry
                time.sleep(min(2 ** attempt, 10))
                continue
                
            except requests.exceptions.RequestException as e:
                logger.error(f"❌ Request error for {provider}: {e}")
                if attempt == max_retries:
                    return {
                        'success': False,
                        'error': f'Request error: {str(e)}',
                        'provider': provider,
                        'attempts': attempt + 1
                    }
                
                # Wait before retry
                time.sleep(min(2 ** attempt, 10))
                continue
        
        # Should not reach here, but just in case
        return {
            'success': False,
            'error': 'Unexpected error: exceeded maximum retries',
            'provider': provider,
            'attempts': max_retries + 1
        }

# Global client instance
api_client = RateLimitAwareAPIClient()

# Convenience function for easy import
def call_model_with_rotation(provider: str, model_id: str, prompt: str, **kwargs) -> Dict:
    """
    Convenience function to call a model with automatic key rotation
    """
    return api_client.call_openrouter_api(provider, model_id, prompt, **kwargs)

if __name__ == "__main__":
    # Test the rate limit aware client
    print("🔄 Testing Rate Limit Aware API Client")
    print("=" * 50)
    
    # Test with a simple prompt
    test_prompt = "Hello! Please respond with a brief greeting."
    
    # Test each provider
    test_providers = [
        ('GLM45', 'z-ai/glm-4.5-air:free'),
        ('GPTOSS', 'openai/gpt-oss-20b:free'),
        ('LLAMA3', 'meta-llama/llama-4-maverick:free')
    ]
    
    for provider, model_id in test_providers:
        print(f"\n🧪 Testing {provider}...")
        result = call_model_with_rotation(provider, model_id, test_prompt, max_tokens=100)
        
        if result['success']:
            print(f"✅ {provider}: {result['response'][:100]}...")
            print(f"   Tokens: {result['metadata']['total_tokens']}, Time: {result['metadata']['response_time_ms']}ms")
        else:
            print(f"❌ {provider}: {result['error']}")