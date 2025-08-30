#!/usr/bin/env python3
"""
Simple test for orchestration components
"""

import sys
import os
import asyncio
import logging

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

logging.basicConfig(level=logging.INFO)

async def test_enhanced_engine():
    """Test the enhanced orchestration engine"""
    
    print("🎭 Testing Enhanced Orchestration Engine")
    print("=" * 40)
    
    try:
        # Test model selector
        print("\n🎯 Testing Model Selector...")
        
        from app.orchestration.enhanced_engine import enhanced_engine
        
        # Test model selection
        test_prompts = [
            "Write a Python function for sorting",
            "Explain quantum physics",
            "Create a marketing campaign"
        ]
        
        for prompt in test_prompts:
            model, scores = enhanced_engine.select_best_model(prompt)
            print(f"'{prompt[:30]}...' → {model} ({max(scores.values()):.3f})")
        
        print("\n✅ Model selector working!")
        
        # Test database initialization
        print("\n💾 Testing Database Connection...")
        try:
            await enhanced_engine.initialize()
            print("✅ Database connection successful!")
        except Exception as e:
            print(f"⚠️ Database connection failed (expected): {e}")
            print("    This is normal if MongoDB isn't running")
        
        print("\n🎉 Enhanced engine test completed!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_provider_manager():
    """Test the provider manager"""
    
    print("\n🔌 Testing Provider Manager")
    print("=" * 30)
    
    try:
        from app.ai_providers.enhanced_manager import enhanced_provider_manager
        
        # Test initialization
        await enhanced_provider_manager.initialize()
        
        # Test model availability
        models = enhanced_provider_manager.get_available_models()
        print(f"Available models: {', '.join(models)}")
        
        # Test simulated response
        response = await enhanced_provider_manager.generate_response(
            "GPT-OSS", 
            "Hello world test"
        )
        
        print(f"Test Response:")
        print(f"  Model: {response.model_name}")
        print(f"  Provider: {response.provider}")
        print(f"  Response: {response.response_text[:100]}...")
        print(f"  Tokens: {response.tokens_used}")
        print(f"  Cost: ${response.cost_usd:.4f}")
        
        print("✅ Provider manager working!")
        return True
        
    except Exception as e:
        print(f"❌ Provider test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    async def main():
        success1 = await test_enhanced_engine()
        success2 = await test_provider_manager()
        
        if success1 and success2:
            print("\n🎉 All tests passed!")
        else:
            print("\n💥 Some tests failed!")
    
    asyncio.run(main())
