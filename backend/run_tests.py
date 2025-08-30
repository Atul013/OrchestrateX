#!/usr/bin/env python
"""
Simple test runner to see output
"""

import subprocess
import sys
import os

def main():
    # Change to backend directory
    os.chdir(r"c:\Users\kalad\OrchestrateX\backend")
    
    # Run pytest with detailed output
    cmd = [
        r"C:/Users/kalad/OrchestrateX/.venv/Scripts/python.exe",
        "-m", "pytest", 
        "tests/test_sessions.py",
        "-v", "--tb=short", "--no-header", "--disable-warnings"
    ]
    
    print("Running command:", " ".join(cmd))
    print("=" * 60)
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        print("STDOUT:")
        print(result.stdout)
        if result.stderr:
            print("\nSTDERR:")
            print(result.stderr)
        print(f"\nReturn code: {result.returncode}")
        
        # Parse the output to count results
        lines = result.stdout.split('\n')
        for line in lines:
            if 'passed' in line or 'failed' in line or 'error' in line:
                print(f"RESULT: {line}")
                
    except subprocess.TimeoutExpired:
        print("Test run timed out after 60 seconds")
    except Exception as e:
        print(f"Error running tests: {e}")

if __name__ == "__main__":
    main()
