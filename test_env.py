#!/usr/bin/env python3
"""
Simple script to test what environment variables are available
"""
import os

def check_env_vars():
    """Check if API key environment variables are set"""
    providers = ['GLM45', 'GPTOSS', 'LLAMA3', 'KIMI', 'QWEN3', 'FALCON']
    
    print("Environment Variables Check:")
    print("=" * 40)
    
    for provider in providers:
        api_key_var = f'PROVIDER_{provider}_API_KEY'
        model_var = f'PROVIDER_{provider}_MODEL'
        
        api_key = os.environ.get(api_key_var)
        model = os.environ.get(model_var)
        
        print(f"{provider}:")
        print(f"  API Key: {'✅ Set' if api_key else '❌ Not found'}")
        print(f"  Model: {'✅ Set' if model else '❌ Not found'}")
        if api_key:
            print(f"  Key preview: {api_key[:10]}...")
        print()

if __name__ == "__main__":
    check_env_vars()