#!/usr/bin/env python3
"""
Simple test for the Advanced OrchestrateX Client
Tests the complete multi-model orchestration with critiques
"""

import asyncio
import logging
import os
from advanced_client import MultiModelOrchestrator, format_for_ui

# Set up logging to be less verbose for demo
logging.basicConfig(level=logging.WARNING, format='%(levelname)s - %(message)s')

async def test_advanced_client():
    """Test the advanced multi-model orchestration client"""
    
    print("🚀 Testing Advanced OrchestrateX Client")
    print("=" * 45)
    
    # Check for API keys
    has_openrouter = bool(os.getenv("OPENROUTER_API_KEY"))
    print(f"OpenRouter API Key: {'✅ Found' if has_openrouter else '❌ Not found (will use simulation)'}")
    
    async with MultiModelOrchestrator() as orchestrator:
        
        # Test prompt
        prompt = "Write a Python function to implement a secure user authentication system"
        
        print(f"\n🎯 Test Prompt: {prompt}")
        print(f"📡 Starting multi-model orchestration...")
        
        # Get complete orchestration with critiques
        result = await orchestrator.orchestrate_with_critiques(prompt)
        
        print(f"\n📊 Orchestration Results:")
        print(f"Overall Success: {'✅' if result.success else '❌'}")
        print(f"Selected Model: {result.selected_model}")
        print(f"Total Time: {result.total_latency_ms}ms")
        print(f"Total Cost: ${result.total_cost_usd:.4f}")
        
        # Primary Response
        print(f"\n🎯 Primary Response ({result.primary_response.model_name}):")
        print(f"Success: {'✅' if result.primary_response.success else '❌'}")
        print(f"Latency: {result.primary_response.latency_ms}ms")
        print(f"Cost: ${result.primary_response.cost_usd:.4f}")
        if result.primary_response.success:
            preview = result.primary_response.response_text[:150]
            print(f"Preview: {preview}...")
        else:
            print(f"Error: {result.primary_response.error_message}")
        
        # Critique Responses
        print(f"\n📝 Critique Responses ({len(result.critique_responses)} models):")
        successful_critiques = 0
        
        for i, critique in enumerate(result.critique_responses, 1):
            status = "✅" if critique.success else "❌"
            print(f"{i}. {status} {critique.model_name}")
            print(f"   Latency: {critique.latency_ms}ms | Cost: ${critique.cost_usd:.4f}")
            
            if critique.success:
                successful_critiques += 1
                preview = critique.response_text[:100]
                print(f"   Preview: {preview}...")
            else:
                print(f"   Error: {critique.error_message}")
        
        print(f"\n📈 Summary:")
        print(f"Successful Critiques: {successful_critiques}/{len(result.critique_responses)}")
        
        # Test UI formatting
        print(f"\n🖥️ UI Integration Test:")
        ui_data = format_for_ui(result)
        print(f"UI Data Keys: {list(ui_data.keys())}")
        print(f"Primary Model: {ui_data['primary']['model']}")
        print(f"Critique Models: {[c['model'] for c in ui_data['critiques']]}")
        
        # Show confidence scores
        print(f"\n🎯 Model Confidence Scores:")
        for model, score in result.model_confidence_scores.items():
            marker = "👑" if model == result.selected_model else "  "
            print(f"{marker} {model}: {score:.3f}")
        
        # Statistics
        print(f"\n📊 Client Statistics:")
        orchestrator.print_stats()
        
        return result

async def test_concurrent_performance():
    """Test concurrent performance with multiple prompts"""
    
    print(f"\n⚡ Concurrent Performance Test")
    print("=" * 35)
    
    test_prompts = [
        "Implement a binary search algorithm",
        "Explain machine learning basics",
        "Design a REST API architecture"
    ]
    
    async with MultiModelOrchestrator() as orchestrator:
        
        print(f"Testing {len(test_prompts)} prompts concurrently...")
        
        # Run multiple orchestrations concurrently
        tasks = [
            orchestrator.orchestrate_with_critiques(prompt) 
            for prompt in test_prompts
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        print(f"\n📊 Concurrent Results:")
        for i, result in enumerate(results, 1):
            if isinstance(result, Exception):
                print(f"{i}. ❌ Failed: {result}")
            else:
                print(f"{i}. {'✅' if result.success else '❌'} {result.selected_model} - {result.total_latency_ms}ms")
        
        orchestrator.print_stats()

if __name__ == "__main__":
    async def main():
        try:
            # Test basic functionality
            result = await test_advanced_client()
            
            # Test concurrent performance
            await test_concurrent_performance()
            
            print(f"\n🎉 All tests completed!")
            
        except Exception as e:
            print(f"\n❌ Test failed: {e}")
            import traceback
            traceback.print_exc()
    
    asyncio.run(main())
