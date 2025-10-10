#!/usr/bin/env python3
"""
Environment Loader for OrchestrateX
Loads environment variables from orche.env file into os.environ
"""

import os
import logging

logger = logging.getLogger(__name__)

def load_env_file(env_file_path: str = "orche.env"):
    """
    Load environment variables from orche.env file into os.environ
    
    Args:
        env_file_path: Path to the environment file
        
    Returns:
        dict: Dictionary of loaded environment variables
    """
    loaded_vars = {}
    
    if not os.path.exists(env_file_path):
        logger.warning(f"⚠️ Environment file {env_file_path} not found")
        return loaded_vars
    
    try:
        with open(env_file_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                
                # Skip empty lines and comments
                if not line or line.startswith('#') or line.startswith('——'):
                    continue
                
                # Parse key=value pairs
                if '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip()
                    
                    if key and value:
                        # Set in os.environ
                        os.environ[key] = value
                        loaded_vars[key] = value
                        logger.debug(f"Loaded {key}")
                else:
                    logger.warning(f"Invalid line {line_num} in {env_file_path}: {line}")
        
        logger.info(f"✅ Loaded {len(loaded_vars)} environment variables from {env_file_path}")
        
        # Log API key availability
        api_key_vars = [k for k in loaded_vars.keys() if 'API_KEY' in k]
        if api_key_vars:
            logger.info(f"🔑 API keys loaded: {len(api_key_vars)}")
            for key in api_key_vars:
                logger.info(f"  - {key}: {value[:10]}..." if len(value) > 10 else f"  - {key}: {value}")
        
        return loaded_vars
        
    except Exception as e:
        logger.error(f"❌ Error loading {env_file_path}: {e}")
        return loaded_vars

def verify_api_keys():
    """
    Verify that required API keys are available in environment
    
    Returns:
        dict: Status of each required API key
    """
    required_keys = [
        'PROVIDER_GLM45_API_KEY',
        'PROVIDER_GPTOSS_API_KEY',
        'PROVIDER_LLAMA3_API_KEY',
        'PROVIDER_KIMI_API_KEY',
        'PROVIDER_QWEN3_API_KEY',
        'PROVIDER_FALCON_API_KEY'
    ]
    
    key_status = {}
    
    for key in required_keys:
        value = os.environ.get(key)
        key_status[key] = {
            'available': value is not None,
            'length': len(value) if value else 0,
            'preview': value[:10] + '...' if value and len(value) > 10 else value
        }
    
    available_count = sum(1 for status in key_status.values() if status['available'])
    
    logger.info(f"📊 API Key Status: {available_count}/{len(required_keys)} available")
    
    for key, status in key_status.items():
        if status['available']:
            logger.info(f"  ✅ {key}: {status['preview']}")
        else:
            logger.warning(f"  ❌ {key}: Missing")
    
    return key_status

def load_orchestratex_environment():
    """
    Main function to load OrchestrateX environment variables
    
    Returns:
        bool: True if environment loaded successfully
    """
    try:
        logger.info("🚀 Loading OrchestrateX environment...")
        
        # Load from orche.env file
        loaded_vars = load_env_file("orche.env")
        
        if not loaded_vars:
            logger.warning("⚠️ No variables loaded from orche.env")
            return False
        
        # Verify API keys
        key_status = verify_api_keys()
        
        # Check if we have at least one API key
        available_keys = sum(1 for status in key_status.values() if status['available'])
        
        if available_keys == 0:
            logger.error("❌ No API keys found in environment")
            return False
        
        logger.info(f"✅ Environment loaded successfully with {available_keys} API keys")
        return True
        
    except Exception as e:
        logger.error(f"❌ Failed to load environment: {e}")
        return False

if __name__ == "__main__":
    # Configure logging for standalone run
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    success = load_orchestratex_environment()
    
    if success:
        print("\n🎉 Environment loaded successfully!")
        print("You can now start the Python backend services.")
    else:
        print("\n❌ Failed to load environment.")
        print("Check if orche.env exists and contains valid API keys.")