#!/usr/bin/env python3
"""
Frontend-Backend Integration Test
Tests the complete UI → API → Orchestration → Refinement workflow
"""

import asyncio
import aiohttp
import json
import time
from datetime import datetime

class FrontendBackendIntegrationTest:
    def __init__(self):
        self.base_url = "http://localhost:8002"  # Enhanced UI Bridge
        self.test_results = []
        
    async def test_health_endpoint(self):
        """Test the health check endpoint"""
        print("🔍 Testing health endpoint...")
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.base_url}/health") as response:
                    if response.status == 200:
                        data = await response.json()
                        print(f"✅ Health check passed: {data['status']}")
                        print(f"   Orchestrator available: {data['orchestrator_available']}")
                        self.test_results.append(("Health Check", True, data))
                        return True
                    else:
                        print(f"❌ Health check failed: {response.status}")
                        self.test_results.append(("Health Check", False, f"Status: {response.status}"))
                        return False
        except Exception as e:
            print(f"❌ Health check error: {e}")
            self.test_results.append(("Health Check", False, str(e)))
            return False

    async def test_orchestration_endpoint(self):
        """Test the main orchestration endpoint"""
        print("\n🎭 Testing orchestration endpoint...")
        
        test_prompt = "Explain the benefits of renewable energy in simple terms"
        
        try:
            async with aiohttp.ClientSession() as session:
                payload = {
                    "prompt": test_prompt,
                    "include_critiques": True,
                    "store_result": True
                }
                
                start_time = time.time()
                async with session.post(
                    f"{self.base_url}/api/orchestration/process",
                    json=payload,
                    headers={"Content-Type": "application/json"}
                ) as response:
                    end_time = time.time()
                    
                    if response.status == 200:
                        data = await response.json()
                        
                        print(f"✅ Orchestration successful")
                        print(f"   Model: {data.get('selected_model', 'Unknown')}")
                        print(f"   Response length: {len(data.get('primary_response', {}).get('response_text', ''))}")
                        print(f"   Critiques: {len(data.get('critique_responses', []))}")
                        print(f"   Latency: {end_time - start_time:.2f}s")
                        print(f"   Cost: ${data.get('total_cost_usd', 0):.4f}")
                        print(f"   Refinement available: {data.get('refinement_available', False)}")
                        
                        self.test_results.append(("Orchestration", True, data))
                        return data
                    else:
                        error_text = await response.text()
                        print(f"❌ Orchestration failed: {response.status}")
                        print(f"   Error: {error_text}")
                        self.test_results.append(("Orchestration", False, f"Status: {response.status}"))
                        return None
                        
        except Exception as e:
            print(f"❌ Orchestration error: {e}")
            self.test_results.append(("Orchestration", False, str(e)))
            return None

    async def test_refinement_endpoint(self, orchestration_result):
        """Test the refinement endpoint"""
        print("\n✨ Testing refinement endpoint...")
        
        if not orchestration_result or not orchestration_result.get('refinement_available'):
            print("⏭️  Skipping refinement test - no critiques available")
            return False
            
        try:
            async with aiohttp.ClientSession() as session:
                payload = {
                    "original_result": orchestration_result,
                    "selected_critique_index": 0  # Use first critique
                }
                
                start_time = time.time()
                async with session.post(
                    f"{self.base_url}/api/orchestration/refine",
                    json=payload,
                    headers={"Content-Type": "application/json"}
                ) as response:
                    end_time = time.time()
                    
                    if response.status == 200:
                        data = await response.json()
                        
                        print(f"✅ Refinement successful")
                        print(f"   Original length: {data.get('comparison', {}).get('original_length', 0)}")
                        print(f"   Refined length: {data.get('comparison', {}).get('refined_length', 0)}")
                        print(f"   Improvement: {data.get('comparison', {}).get('improvement', False)}")
                        print(f"   Refinement latency: {end_time - start_time:.2f}s")
                        print(f"   Additional cost: ${data.get('refined_response', {}).get('cost_usd', 0):.4f}")
                        
                        self.test_results.append(("Refinement", True, data))
                        return True
                    else:
                        error_text = await response.text()
                        print(f"❌ Refinement failed: {response.status}")
                        print(f"   Error: {error_text}")
                        self.test_results.append(("Refinement", False, f"Status: {response.status}"))
                        return False
                        
        except Exception as e:
            print(f"❌ Refinement error: {e}")
            self.test_results.append(("Refinement", False, str(e)))
            return False

    async def test_legacy_chat_endpoint(self):
        """Test the legacy chat endpoint for backward compatibility"""
        print("\n🔄 Testing legacy chat endpoint...")
        
        try:
            async with aiohttp.ClientSession() as session:
                payload = {"message": "What is machine learning?"}
                
                async with session.post(
                    f"{self.base_url}/chat",
                    json=payload,
                    headers={"Content-Type": "application/json"}
                ) as response:
                    
                    if response.status == 200:
                        data = await response.json()
                        print(f"✅ Legacy endpoint working")
                        self.test_results.append(("Legacy Chat", True, "Compatible"))
                        return True
                    else:
                        print(f"❌ Legacy endpoint failed: {response.status}")
                        self.test_results.append(("Legacy Chat", False, f"Status: {response.status}"))
                        return False
                        
        except Exception as e:
            print(f"❌ Legacy endpoint error: {e}")
            self.test_results.append(("Legacy Chat", False, str(e)))
            return False

    def print_summary(self):
        """Print test summary"""
        print("\n" + "="*60)
        print("📊 FRONTEND-BACKEND INTEGRATION TEST SUMMARY")
        print("="*60)
        
        passed = sum(1 for _, success, _ in self.test_results if success)
        total = len(self.test_results)
        
        for test_name, success, details in self.test_results:
            status = "✅ PASS" if success else "❌ FAIL"
            print(f"{status} {test_name}")
            
        print(f"\nOverall: {passed}/{total} tests passed")
        
        if passed == total:
            print("\n🎉 ALL TESTS PASSED!")
            print("Frontend-backend integration is working correctly!")
            print("\n🚀 Ready for production deployment!")
        else:
            print(f"\n⚠️  {total - passed} tests failed")
            print("Please check the backend service status")
            
        print("\n📋 Next Steps:")
        print("1. Start frontend: npm run dev in both React projects")
        print("2. Visit http://localhost:5174 for the Chat UI")
        print("3. Visit http://localhost:5173 for the Landing Page")
        print("4. Test the complete user workflow")

async def main():
    """Run all integration tests"""
    print("🧪 FRONTEND-BACKEND INTEGRATION TEST SUITE")
    print("="*60)
    print("Testing the complete UI → API → Orchestration workflow")
    print("="*60)
    
    tester = FrontendBackendIntegrationTest()
    
    # Test health endpoint
    health_ok = await tester.test_health_endpoint()
    
    if not health_ok:
        print("\n❌ Backend is not responding!")
        print("Please start the enhanced UI bridge API:")
        print("   python enhanced_ui_bridge_api.py")
        return
    
    # Test orchestration
    orchestration_result = await tester.test_orchestration_endpoint()
    
    # Test refinement (if orchestration worked)
    if orchestration_result:
        await tester.test_refinement_endpoint(orchestration_result)
    
    # Test legacy endpoint
    await tester.test_legacy_chat_endpoint()
    
    # Print summary
    tester.print_summary()

if __name__ == "__main__":
    asyncio.run(main())
