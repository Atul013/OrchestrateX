#!/usr/bin/env python3
"""
Simple test for the OrchestrateX client
"""

import asyncio
import logging
from orchestratex_client import OrchestrateXClient

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def test_client():
    """Test the OrchestrateX client"""
    
    print("🧪 Testing OrchestrateX Client")
    print("=" * 30)
    
    async with OrchestrateXClient() as client:
        
        # Test 1: Single prompt
        print("\n🎯 Test 1: Single Prompt")
        prompt = "Write a Python function to implement binary search"
        
        result = await client.orchestrate_prompt(prompt)
        
        print(f"Success: {result.success}")
        print(f"Selected Model: {result.selected_model}")
        print(f"Confidence Scores: {result.confidence_scores}")
        print(f"Response Length: {len(result.final_response.response_text)} characters")
        print(f"Response Time: {result.total_time_ms}ms")
        print(f"Cost: ${result.total_cost_usd:.4f}")
        
        if result.fallback_attempts:
            print(f"Fallback Attempts: {result.fallback_attempts}")
        
        if result.success:
            print(f"Response Preview: {result.final_response.response_text[:200]}...")
        else:
            print(f"Error: {result.final_response.error_message}")
        
        # Test 2: Multiple prompts
        print("\n📊 Test 2: Batch Prompts")
        test_prompts = [
            "Explain quantum physics in simple terms",
            "Write a SQL query for user authentication",
            "Create a marketing strategy for mobile apps"
        ]
        
        batch_results = await client.process_batch(test_prompts, max_concurrent=2)
        
        for i, batch_result in enumerate(batch_results, 1):
            status = "✅" if batch_result.success else "❌"
            print(f"{i}. {status} {batch_result.selected_model} - {batch_result.total_time_ms}ms")
        
        # Show final statistics
        print("\n📈 Final Statistics:")
        client.print_stats()
        
        return True

if __name__ == "__main__":
    try:
        success = asyncio.run(test_client())
        if success:
            print("\n🎉 Client test completed successfully!")
        else:
            print("\n💥 Client test failed!")
    except Exception as e:
        print(f"\n❌ Test error: {e}")
        import traceback
        traceback.print_exc()
