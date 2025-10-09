#!/usr/bin/env python3
"""
API Key Rotation Manager for OrchestrateX
Handles automatic rotation of API keys when rate limits are reached
"""

import os
import time
import json
import logging
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import threading
from collections import defaultdict

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class APIKeyRotationManager:
    """
    Manages API key rotation for multiple providers with rate limit detection
    """
    
    def __init__(self, env_file: str = "orche.env"):
        self.env_file = env_file
        self.api_keys: Dict[str, Dict] = {}
        self.key_usage: Dict[str, Dict] = defaultdict(lambda: {
            'requests': 0, 
            'last_reset': datetime.now(),
            'rate_limited': False,
            'current_key_index': 0
        })
        self.rotation_history: List[Dict] = []
        self.lock = threading.Lock()
        
        # Rate limit recovery time (how long to wait before retrying a rate-limited key)
        self.rate_limit_recovery_time = timedelta(minutes=15)
        
        self._load_api_keys()
        logger.info(f"🔑 API Key Rotation Manager initialized with {len(self.api_keys)} providers")

    def _load_from_environment(self):
        """Load API keys from environment variables"""
        providers_found = 0
        
        # List of known providers
        providers = ['GLM45', 'GPTOSS', 'LLAMA3', 'KIMI', 'QWEN3', 'FALCON']
        
        for provider in providers:
            api_key = os.environ.get(f'PROVIDER_{provider}_API_KEY')
            model = os.environ.get(f'PROVIDER_{provider}_MODEL')
            
            if api_key:
                self.api_keys[provider] = {
                    'primary_key': api_key,
                    'backup_keys': [],
                    'model_id': model,
                    'all_keys': [api_key]
                }
                providers_found += 1
                logger.info(f"✅ Loaded {provider} from environment")
        
        return providers_found > 0
    
    def _load_api_keys(self):
        """Load API keys from environment variables or file"""
        # First try to load from environment variables (for Cloud Run)
        env_keys = self._load_from_environment()
        if env_keys:
            logger.info(f"🔑 Loaded {len(env_keys)} providers from environment variables")
            return

        # Fallback to file (for local development)
        if not os.path.exists(self.env_file):
            logger.error(f"❌ Environment file {self.env_file} not found and no env vars")
            return

        with open(self.env_file, 'r') as f:
            lines = f.readlines()
        
        current_provider = None
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith('#') or line.startswith('—'):
                continue
            
            if '=' in line:
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip()
                
                # Detect provider from key pattern
                if key.startswith('PROVIDER_') and key.endswith('_API_KEY'):
                    provider_name = key.replace('PROVIDER_', '').replace('_API_KEY', '')
                    current_provider = provider_name
                    
                    if current_provider not in self.api_keys:
                        self.api_keys[current_provider] = {
                            'primary_key': value,
                            'backup_keys': [],
                            'model_id': None,
                            'all_keys': [value]
                        }
                    else:
                        self.api_keys[current_provider]['primary_key'] = value
                        if value not in self.api_keys[current_provider]['all_keys']:
                            self.api_keys[current_provider]['all_keys'].insert(0, value)
                
                elif key.startswith('PROVIDER_') and key.endswith('_BACKUP_KEYS'):
                    provider_name = key.replace('PROVIDER_', '').replace('_BACKUP_KEYS', '')
                    if provider_name in self.api_keys and value:
                        backup_keys = [k.strip() for k in value.split(',')]
                        self.api_keys[provider_name]['backup_keys'] = backup_keys
                        # Add backup keys to all_keys if not already present
                        for backup_key in backup_keys:
                            if backup_key not in self.api_keys[provider_name]['all_keys']:
                                self.api_keys[provider_name]['all_keys'].append(backup_key)
                
                elif key.startswith('PROVIDER_') and key.endswith('_MODEL'):
                    provider_name = key.replace('PROVIDER_', '').replace('_MODEL', '')
                    if provider_name in self.api_keys:
                        self.api_keys[provider_name]['model_id'] = value
        
        # Initialize usage tracking for all providers
        for provider in self.api_keys.keys():
            self.key_usage[provider] = {
                'requests': 0,
                'last_reset': datetime.now(),
                'rate_limited': False,
                'current_key_index': 0,
                'key_status': {i: {'rate_limited': False, 'last_limited': None} 
                             for i in range(len(self.api_keys[provider]['all_keys']))}
            }
        
        logger.info(f"✅ Loaded API keys for providers: {list(self.api_keys.keys())}")
    
    def get_current_api_key(self, provider: str) -> Optional[str]:
        """Get the current active API key for a provider"""
        with self.lock:
            if provider not in self.api_keys:
                logger.error(f"❌ Provider {provider} not found")
                return None
            
            provider_config = self.api_keys[provider]
            usage_info = self.key_usage[provider]
            current_index = usage_info['current_key_index']
            
            # Check if current key is rate limited and if recovery time has passed
            key_status = usage_info['key_status'][current_index]
            if key_status['rate_limited'] and key_status['last_limited']:
                if datetime.now() - key_status['last_limited'] > self.rate_limit_recovery_time:
                    # Recovery time passed, reset rate limit status
                    key_status['rate_limited'] = False
                    key_status['last_limited'] = None
                    logger.info(f"🔄 Provider {provider} key {current_index} recovered from rate limit")
            
            # If current key is still rate limited, try to rotate
            if key_status['rate_limited']:
                self._rotate_to_next_available_key(provider)
                current_index = usage_info['current_key_index']
            
            current_key = provider_config['all_keys'][current_index]
            logger.debug(f"🔑 Using key index {current_index} for provider {provider}")
            return current_key
    
    def _rotate_to_next_available_key(self, provider: str) -> bool:
        """Rotate to the next available (non-rate-limited) key"""
        provider_config = self.api_keys[provider]
        usage_info = self.key_usage[provider]
        total_keys = len(provider_config['all_keys'])
        
        # Try all keys to find a non-rate-limited one
        for i in range(total_keys):
            next_index = (usage_info['current_key_index'] + i + 1) % total_keys
            key_status = usage_info['key_status'][next_index]
            
            # Check if this key is available (not rate limited or recovered)
            if not key_status['rate_limited'] or (
                key_status['last_limited'] and 
                datetime.now() - key_status['last_limited'] > self.rate_limit_recovery_time
            ):
                # Found an available key
                old_index = usage_info['current_key_index']
                usage_info['current_key_index'] = next_index
                
                # Reset rate limit status if recovery time passed
                if key_status['rate_limited']:
                    key_status['rate_limited'] = False
                    key_status['last_limited'] = None
                
                # Log rotation
                rotation_event = {
                    'timestamp': datetime.now().isoformat(),
                    'provider': provider,
                    'from_key_index': old_index,
                    'to_key_index': next_index,
                    'reason': 'rate_limit_avoidance'
                }
                self.rotation_history.append(rotation_event)
                
                logger.warning(f"🔄 Rotated {provider} from key {old_index} to key {next_index}")
                return True
        
        # All keys are rate limited
        logger.error(f"❌ All API keys for provider {provider} are rate limited!")
        return False
    
    def handle_rate_limit_error(self, provider: str, error_response: dict = None) -> bool:
        """
        Handle rate limit error by marking current key as rate limited and rotating
        Returns True if rotation was successful, False if all keys are rate limited
        """
        with self.lock:
            if provider not in self.api_keys:
                logger.error(f"❌ Provider {provider} not found")
                return False
            
            usage_info = self.key_usage[provider]
            current_index = usage_info['current_key_index']
            
            # Mark current key as rate limited
            usage_info['key_status'][current_index]['rate_limited'] = True
            usage_info['key_status'][current_index]['last_limited'] = datetime.now()
            
            logger.warning(f"⚠️ Rate limit detected for {provider} key {current_index}")
            
            # Log the rate limit event
            rate_limit_event = {
                'timestamp': datetime.now().isoformat(),
                'provider': provider,
                'key_index': current_index,
                'error_response': error_response,
                'action': 'marked_rate_limited'
            }
            self.rotation_history.append(rate_limit_event)
            
            # Try to rotate to next available key
            return self._rotate_to_next_available_key(provider)
    
    def increment_request_count(self, provider: str):
        """Increment request count for monitoring purposes"""
        with self.lock:
            if provider in self.key_usage:
                self.key_usage[provider]['requests'] += 1
    
    def get_provider_status(self, provider: str) -> Dict:
        """Get detailed status information for a provider"""
        if provider not in self.api_keys:
            return {'error': f'Provider {provider} not found'}
        
        with self.lock:
            provider_config = self.api_keys[provider]
            usage_info = self.key_usage[provider]
            
            status = {
                'provider': provider,
                'model_id': provider_config['model_id'],
                'total_keys': len(provider_config['all_keys']),
                'current_key_index': usage_info['current_key_index'],
                'total_requests': usage_info['requests'],
                'last_reset': usage_info['last_reset'].isoformat(),
                'keys_status': []
            }
            
            for i, key in enumerate(provider_config['all_keys']):
                key_status = usage_info['key_status'][i]
                status['keys_status'].append({
                    'index': i,
                    'key_preview': f"{key[:15]}...{key[-10:]}",
                    'is_current': i == usage_info['current_key_index'],
                    'rate_limited': key_status['rate_limited'],
                    'last_limited': key_status['last_limited'].isoformat() if key_status['last_limited'] else None
                })
            
            return status
    
    def get_all_provider_status(self) -> Dict:
        """Get status for all providers"""
        return {provider: self.get_provider_status(provider) for provider in self.api_keys.keys()}
    
    def get_rotation_history(self, limit: int = 50) -> List[Dict]:
        """Get recent rotation history"""
        return self.rotation_history[-limit:]
    
    def reset_provider_limits(self, provider: str):
        """Manually reset rate limits for a provider (admin function)"""
        with self.lock:
            if provider in self.key_usage:
                usage_info = self.key_usage[provider]
                for key_status in usage_info['key_status'].values():
                    key_status['rate_limited'] = False
                    key_status['last_limited'] = None
                usage_info['current_key_index'] = 0
                logger.info(f"🔄 Manually reset rate limits for provider {provider}")
    
    def export_status_report(self) -> Dict:
        """Export comprehensive status report"""
        return {
            'timestamp': datetime.now().isoformat(),
            'total_providers': len(self.api_keys),
            'providers_status': self.get_all_provider_status(),
            'recent_rotations': self.get_rotation_history(20),
            'system_info': {
                'rate_limit_recovery_time_minutes': self.rate_limit_recovery_time.total_seconds() / 60,
                'rotation_manager_version': '1.0.0'
            }
        }

# Global instance
rotation_manager = APIKeyRotationManager()

# Convenience functions for easy import
def get_api_key(provider: str) -> Optional[str]:
    """Get current API key for provider"""
    return rotation_manager.get_current_api_key(provider)

def handle_rate_limit(provider: str, error_response: dict = None) -> bool:
    """Handle rate limit error"""
    return rotation_manager.handle_rate_limit_error(provider, error_response)

def increment_usage(provider: str):
    """Increment request count"""
    rotation_manager.increment_request_count(provider)

def get_status(provider: str = None) -> Dict:
    """Get status for provider or all providers"""
    if provider:
        return rotation_manager.get_provider_status(provider)
    else:
        return rotation_manager.get_all_provider_status()

if __name__ == "__main__":
    # Test the rotation manager
    print("🔑 API Key Rotation Manager Test")
    print("=" * 50)
    
    # Print status for all providers
    status = rotation_manager.export_status_report()
    print(json.dumps(status, indent=2))
    
    # Test getting keys
    for provider in ['GLM45', 'GPTOSS', 'LLAMA3', 'KIMI', 'QWEN3', 'FALCON']:
        key = get_api_key(provider)
        if key:
            print(f"✅ {provider}: {key[:15]}...{key[-10:]}")
        else:
            print(f"❌ {provider}: No key found")