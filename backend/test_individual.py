"""
Test individual endpoints to identify issues
"""

import subprocess
import sys
import os

def run_single_test(test_name):
    """Run a single test and return the result"""
    os.chdir(r"c:\Users\kalad\OrchestrateX\backend")
    
    cmd = [
        r"C:/Users/kalad/OrchestrateX/.venv/Scripts/python.exe",
        "-m", "pytest", 
        f"tests/test_sessions.py::TestSessionEndpoints::{test_name}",
        "-v", "--tb=short", "--disable-warnings"
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
        success = result.returncode == 0
        return success, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return False, "", "Timeout after 15 seconds"
    except Exception as e:
        return False, "", str(e)

def main():
    tests = [
        "test_create_session",
        "test_invalid_session_data", 
        "test_get_session",
        "test_list_user_sessions",
        "test_update_session_status",
        "test_session_not_found"
    ]
    
    results = {}
    
    for test in tests:
        print(f"\n{'='*50}")
        print(f"Testing: {test}")
        print('='*50)
        
        success, stdout, stderr = run_single_test(test)
        results[test] = success
        
        if success:
            print("✅ PASSED")
        else:
            print("❌ FAILED")
            if stdout:
                print("STDOUT:", stdout[-500:])  # Last 500 chars
            if stderr:
                print("STDERR:", stderr[-500:])  # Last 500 chars
    
    print("\n" + "="*60)
    print("SUMMARY:")
    print("="*60)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test, success in results.items():
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{test}: {status}")
    
    print(f"\nTotal: {passed}/{total} tests passing")

if __name__ == "__main__":
    main()
