#!/usr/bin/env python3
"""
Simple test of the Advanced Multi-Model Orchestration Client
"""

import asyncio
import sys
from advanced_client import MultiModelOrchestrator

async def simple_test():
    """Simple test with a basic prompt"""
    print("="*60)
    print("🚀 OrchestrateX Advanced Client - Simple Test")
    print("="*60)
    
    # Simple test prompt
    prompt = "Explain the benefits of renewable energy in exactly 3 sentences."
    
    print(f"\n📝 Prompt: {prompt}")
    print("\n🔄 Starting orchestration...")
    
    async with MultiModelOrchestrator() as orchestrator:
        try:
            result = await orchestrator.orchestrate_with_critiques(prompt)
            
            print("\n" + "="*60)
            print("📊 RESULTS")
            print("="*60)
            
            # Primary Response
            if result.primary_response and result.primary_response.success:
                print(f"\n✅ PRIMARY RESPONSE ({result.primary_response.model_name}):")
                print(f"📄 Content: {result.primary_response.response_text}")
                print(f"💰 Cost: ${result.primary_response.cost_usd:.4f}")
                print(f"⚡ Latency: {result.primary_response.latency_ms}ms")
                print(f"🔢 Tokens: {result.primary_response.tokens_used}")
            
            # Critiques
            successful_critiques = [c for c in result.critique_responses if c.success]
            print(f"\n✅ CRITIQUES ({len(successful_critiques)} successful):")
            
            for i, critique in enumerate(successful_critiques, 1):
                print(f"\n{i}. {critique.model_name}:")
                print(f"   📄 {critique.response_text}")
                print(f"   💰 ${critique.cost_usd:.4f} | ⚡ {critique.latency_ms}ms | 🔢 {critique.tokens_used} tokens")
            
            # Summary
            all_responses = [result.primary_response] + result.critique_responses
            total_cost = sum(c.cost_usd for c in all_responses if c.success)
            total_calls = len([c for c in all_responses if c.success])
            success_rate = total_calls / len(all_responses) if all_responses else 0
            
            print(f"\n📊 SUMMARY:")
            print(f"   💰 Total Cost: ${total_cost:.4f}")
            print(f"   📞 API Calls: {total_calls}")
            print(f"   ✅ Success Rate: {success_rate:.1%}")
            
            print("\n🎉 Test completed successfully!")
            
        except Exception as e:
            print(f"\n❌ Test failed: {e}")
            return False
    
    return True

if __name__ == "__main__":
    asyncio.run(simple_test())
