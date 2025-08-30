"""
Alternative test runner using pytest programmatically
"""

import sys
import os
sys.path.insert(0, r'c:\Users\kalad\OrchestrateX\backend')

import pytest
from io import StringIO

def run_tests():
    """Run tests programmatically"""
    print("Running tests programmatically...")
    
    # Change to the backend directory
    os.chdir(r'c:\Users\kalad\OrchestrateX\backend')
    
    # Capture output
    old_stdout = sys.stdout
    old_stderr = sys.stderr
    stdout_capture = StringIO()
    stderr_capture = StringIO()
    
    try:
        sys.stdout = stdout_capture
        sys.stderr = stderr_capture
        
        # Run pytest with specific arguments
        exit_code = pytest.main([
            'tests/test_sessions.py',
            '-v',
            '--tb=short',
            '--disable-warnings',
            '--no-header'
        ])
        
        # Restore output
        sys.stdout = old_stdout
        sys.stderr = old_stderr
        
        # Get captured output
        stdout_output = stdout_capture.getvalue()
        stderr_output = stderr_capture.getvalue()
        
        print("=" * 60)
        print("PYTEST OUTPUT:")
        print("=" * 60)
        print(stdout_output)
        
        if stderr_output:
            print("\nSTDERR OUTPUT:")
            print(stderr_output)
        
        print(f"\nExit code: {exit_code}")
        
        # Parse results
        lines = stdout_output.split('\n')
        passed = 0
        failed = 0
        errors = 0
        
        for line in lines:
            if ' PASSED ' in line:
                passed += 1
            elif ' FAILED ' in line:
                failed += 1
            elif ' ERROR ' in line:
                errors += 1
        
        total = passed + failed + errors
        
        print(f"\n{'='*60}")
        print(f"TEST SUMMARY:")
        print(f"{'='*60}")
        print(f"✅ Passed: {passed}")
        print(f"❌ Failed: {failed}")
        print(f"🔥 Errors: {errors}")
        print(f"📊 Total: {total}")
        
        if total > 0:
            success_rate = (passed / total) * 100
            print(f"📈 Success Rate: {success_rate:.1f}%")
        
        return exit_code == 0
        
    except Exception as e:
        sys.stdout = old_stdout
        sys.stderr = old_stderr
        print(f"Error running tests: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Alternative Test Runner for OrchestrateX")
    print("=" * 60)
    
    success = run_tests()
    
    if success:
        print("\n🎉 All tests completed successfully!")
    else:
        print("\n⚠️ Some tests failed or had errors.")
