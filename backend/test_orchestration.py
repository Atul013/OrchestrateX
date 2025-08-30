#!/usr/bin/env python3
"""
Test script for the Enhanced Orchestration System

Tests the complete pipeline:
1. ML-based model selection
2. AI provider integration
3. Multi-model iteration
4. Database persistence
"""

import asyncio
import sys
import os
import logging
from datetime import datetime

# Add the backend to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

async def test_orchestration_system():
    """Test the complete orchestration system"""
    
    print("🚀 Testing Enhanced Orchestration System")
    print("=" * 50)
    
    try:
        # Import components
        from backend.app.orchestration.enhanced_engine import enhanced_engine
        from backend.app.ai_providers.enhanced_manager import enhanced_provider_manager
        
        print("✅ Successfully imported orchestration components")
        
        # Initialize the system
        print("\n🔧 Initializing system...")
        await enhanced_engine.initialize()
        await enhanced_provider_manager.initialize()
        
        print("✅ System initialized successfully")
        
        # Test 1: Model Selection
        print("\n🎯 Test 1: ML Model Selection")
        test_prompts = [
            "Write a Python function to sort an array",
            "Explain the economic impact of renewable energy",
            "Create a creative story about space exploration",
            "Solve this math equation: 2x + 5 = 15"
        ]
        
        for prompt in test_prompts:
            best_model, confidence_scores = enhanced_engine.select_best_model(prompt)
            print(f"📝 '{prompt[:40]}...' → {best_model} ({max(confidence_scores.values()):.3f})")
        
        # Test 2: End-to-End Orchestration
        print("\n🎭 Test 2: End-to-End Orchestration")
        
        session_id = f"test_session_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
        test_prompt = "Write a Python function to implement binary search with detailed comments"
        
        print(f"Session ID: {session_id}")
        print(f"Prompt: {test_prompt}")
        
        result = await enhanced_engine.orchestrate_prompt(
            session_id=session_id,
            prompt=test_prompt,
            max_iterations=3,
            quality_threshold=0.8
        )
        
        print("\n📊 Orchestration Results:")
        print(f"Status: {result['status']}")
        print(f"Selected Model: {result['selected_model']}")
        print(f"Thread ID: {result['thread_id']}")
        
        if result['status'] == 'completed':
            print(f"Final Response Preview: {result['final_response'][:200]}...")
        
        # Test 3: Provider Manager
        print("\n🔌 Test 3: Provider Manager")
        
        available_models = enhanced_provider_manager.get_available_models()
        print(f"Available Models: {', '.join(available_models)}")
        
        # Test direct provider call
        test_response = await enhanced_provider_manager.generate_response(
            "GPT-OSS", 
            "Hello, test message"
        )
        
        print(f"Test Response from GPT-OSS:")
        print(f"  Response: {test_response.response_text[:100]}...")
        print(f"  Tokens: {test_response.tokens_used}")
        print(f"  Cost: ${test_response.cost_usd:.4f}")
        print(f"  Time: {test_response.response_time_ms}ms")
        
        print("\n✅ All tests completed successfully!")
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_model_selector_only():
    """Test just the model selector component"""
    
    print("🎯 Testing Model Selector Only")
    print("=" * 30)
    
    try:
        # Import and test model selector directly
        sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'orchestration'))
        from model_selector import ModelSelector
        
        selector = ModelSelector()
        
        # Try to load trained model
        model_path = os.path.join(os.path.dirname(__file__), '..', 'orchestration', 'model_selector.pkl')
        if os.path.exists(model_path):
            selector.load_model(model_path)
            print("✅ Loaded trained model")
        else:
            print("⚠️ Trained model not found, using fallback")
        
        # Test predictions
        test_prompts = [
            "Debug this JavaScript error",
            "Write a creative poem about AI",
            "Calculate the derivative of x^2 + 3x",
            "Analyze market trends for renewable energy"
        ]
        
        for prompt in test_prompts:
            if hasattr(selector, 'model') and selector.model is not None:
                best_model, scores = selector.select_best_model(prompt)
                print(f"'{prompt[:30]}...' → {best_model} ({max(scores.values()):.3f})")
            else:
                print(f"'{prompt[:30]}...' → [No trained model available]")
        
        return True
        
    except Exception as e:
        print(f"❌ Model selector test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🧪 OrchestrateX System Testing")
    print("Choose test mode:")
    print("1. Full orchestration system test")
    print("2. Model selector only test")
    
    choice = input("Enter choice (1 or 2): ").strip()
    
    if choice == "1":
        success = asyncio.run(test_orchestration_system())
    elif choice == "2":
        success = asyncio.run(test_model_selector_only())
    else:
        print("Invalid choice")
        success = False
    
    if success:
        print("\n🎉 Testing completed successfully!")
    else:
        print("\n💥 Testing failed!")
        sys.exit(1)
