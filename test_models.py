#!/usr/bin/env python3
import requests
from env_loader import load_env_file

def test_deepseek():
    loaded = load_env_file('orche.env')
    api_key = loaded['PROVIDER_FALCON_API_KEY']
    
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    
    payload = {
        'model': 'deepseek/deepseek-chat',
        'messages': [{'role': 'user', 'content': 'Brief critique: Hello world'}],
        'max_tokens': 50
    }
    
    try:
        response = requests.post('https://openrouter.ai/api/v1/chat/completions', 
                               json=payload, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            content = data['choices'][0]['message']['content']
            print(f'DeepSeek response: "{content}"')
            print(f'Length: {len(content)} chars')
            print(f'Empty: {len(content.strip()) == 0}')
        else:
            print(f'Error {response.status_code}: {response.text}')
    except Exception as e:
        print(f'Exception: {e}')

if __name__ == '__main__':
    test_deepseek()