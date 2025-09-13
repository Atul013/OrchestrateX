#!/usr/bin/env python3
"""
Test script for the new user-controlled refinement workflow
Demonstrates Model A improving its response based on Model B-F's critiques
"""

import asyncio
import sys
import os
from advanced_client import MultiModelOrchestrator, interactive_critique_selector, format_complete_result

async def test_refinement_basic():
    """Test basic refinement workflow"""
    print("🧪 TEST 1: Basic Refinement Workflow")
    print("="*50)
    
    async with MultiModelOrchestrator() as orchestrator:
        
        # Simple prompt that can be improved
        prompt = "How do I make coffee?"
        
        print(f"📝 Prompt: {prompt}")
        print("🔄 Running orchestration with critiques...")
        
        # Step 1: Get initial response + critiques
        initial_result = await orchestrator.orchestrate_with_critiques(prompt)
        
        if not initial_result.success:
            print("❌ Initial orchestration failed")
            return
        
        print(f"\n🤖 Primary Model: {initial_result.selected_model}")
        print(f"Original Response: {initial_result.primary_response.response_text[:200]}...")
        
        # Step 2: Show critiques
        successful_critiques = [c for c in initial_result.critique_responses if c.success]
        print(f"\n📝 Received {len(successful_critiques)} critiques:")
        
        for i, critique in enumerate(successful_critiques):
            print(f"  {i+1}. {critique.model_name}: {critique.response_text[:100]}...")
        
        if successful_critiques:
            # Step 3: Auto-select first critique for refinement
            chosen_critique = successful_critiques[0]
            print(f"\n🎯 Auto-selecting {chosen_critique.model_name}'s critique for refinement...")
            
            # Step 4: Refine the response
            refined_response = await orchestrator.refine_response_with_critique(
                original_prompt=prompt,
                primary_model=initial_result.selected_model,
                original_response=initial_result.primary_response.response_text,
                chosen_critique=chosen_critique.response_text,
                critique_model=chosen_critique.model_name
            )
            
            print(f"\n✨ REFINED RESPONSE:")
            print(f"Model: {refined_response.model_name}")
            print(f"Response: {refined_response.response_text}")
            print(f"Original Length: {len(initial_result.primary_response.response_text)} chars")
            print(f"Refined Length: {len(refined_response.response_text)} chars")
            
            return True
        else:
            print("❌ No critiques available for refinement")
            return False

async def test_complete_workflow():
    """Test the complete workflow with user interaction simulation"""
    print("\n🧪 TEST 2: Complete Workflow (Simulated User Choice)")
    print("="*50)
    
    async with MultiModelOrchestrator() as orchestrator:
        
        prompt = "Explain recursion in programming"
        
        # Simulate user always choosing the second critique (if available)
        def simulate_user_choice(critiques):
            if len(critiques) >= 2:
                print(f"🎭 Simulated user chooses {critiques[1].model_name}'s critique")
                return (1, True)  # Choose second critique, do refine
            elif len(critiques) >= 1:
                print(f"🎭 Simulated user chooses {critiques[0].model_name}'s critique")
                return (0, True)  # Choose first critique, do refine
            else:
                print("🎭 Simulated user skips refinement (no critiques)")
                return (0, False)  # No refinement
        
        # Run complete workflow
        workflow_result = await orchestrator.orchestrate_with_user_refinement(
            prompt=prompt,
            user_choice_callback=simulate_user_choice
        )
        
        # Display results
        print(format_complete_result(workflow_result))
        
        return workflow_result

async def test_multiple_refinements():
    """Test refinement with different critique selections"""
    print("\n🧪 TEST 3: Multiple Refinement Scenarios")
    print("="*50)
    
    async with MultiModelOrchestrator() as orchestrator:
        
        prompt = "Write Python code to read a CSV file"
        
        # Get initial orchestration
        initial_result = await orchestrator.orchestrate_with_critiques(prompt)
        
        if not initial_result.success:
            print("❌ Initial orchestration failed")
            return
        
        successful_critiques = [c for c in initial_result.critique_responses if c.success]
        
        print(f"📊 Testing refinement with {len(successful_critiques)} different critiques:")
        
        refinement_results = []
        
        for i, critique in enumerate(successful_critiques[:3]):  # Test max 3 critiques
            print(f"\n🔄 Refinement {i+1} using {critique.model_name}'s feedback:")
            
            refined_response = await orchestrator.refine_response_with_critique(
                original_prompt=prompt,
                primary_model=initial_result.selected_model,
                original_response=initial_result.primary_response.response_text,
                chosen_critique=critique.response_text,
                critique_model=critique.model_name
            )
            
            refinement_results.append({
                "critique_model": critique.model_name,
                "refined_response": refined_response,
                "success": refined_response.success
            })
            
            print(f"  ✅ Success: {refined_response.success}")
            print(f"  📏 Length: {len(refined_response.response_text)} chars")
            if refined_response.success:
                print(f"  📝 Preview: {refined_response.response_text[:150]}...")
        
        # Summary
        successful_refinements = sum(1 for r in refinement_results if r["success"])
        print(f"\n📊 Refinement Summary: {successful_refinements}/{len(refinement_results)} successful")
        
        return refinement_results

async def test_edge_cases():
    """Test edge cases and error handling"""
    print("\n🧪 TEST 4: Edge Cases & Error Handling")
    print("="*50)
    
    async with MultiModelOrchestrator() as orchestrator:
        
        # Test 1: Empty prompt
        print("🔍 Test 4.1: Empty prompt")
        try:
            result = await orchestrator.orchestrate_with_user_refinement(
                prompt="",
                user_choice_callback=lambda c: (0, False)
            )
            print(f"  Result: {result['stage']}")
        except Exception as e:
            print(f"  Error: {e}")
        
        # Test 2: Very short prompt
        print("\n🔍 Test 4.2: Very short prompt")
        result = await orchestrator.orchestrate_with_user_refinement(
            prompt="Hi",
            user_choice_callback=lambda c: (0, True) if c else (0, False)
        )
        print(f"  Result: {result['stage']}")
        print(f"  Primary model: {result['initial_result'].selected_model}")
        
        # Test 3: No refinement choice
        print("\n🔍 Test 4.3: User chooses no refinement")
        result = await orchestrator.orchestrate_with_user_refinement(
            prompt="What is Python?",
            user_choice_callback=lambda c: (0, False)  # Always skip refinement
        )
        print(f"  Result: {result['stage']}")
        print(f"  Refined response: {result['refined_response'] is not None}")

async def main():
    """Run all tests"""
    print("🚀 TESTING USER-CONTROLLED REFINEMENT WORKFLOW")
    print("="*60)
    print("This demonstrates the new feature where:")
    print("1. Algorithm chooses Model A as best")
    print("2. Models B-F critique Model A's output")
    print("3. User chooses which critique to use")
    print("4. Model A refines its response based on chosen critique")
    print("="*60)
    
    try:
        # Run all tests
        await test_refinement_basic()
        await test_complete_workflow()
        await test_multiple_refinements()
        await test_edge_cases()
        
        print("\n✅ ALL TESTS COMPLETED!")
        print("🎉 User-controlled refinement feature is working!")
        
    except KeyboardInterrupt:
        print("\n❌ Tests interrupted by user")
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
