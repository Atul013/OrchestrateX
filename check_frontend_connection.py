#!/usr/bin/env python3
"""
Check what URL the frontend at orchestratex.me is actually using
"""

import requests
import json

def check_frontend_connection():
    """Check what backend the live frontend is connecting to"""
    print("🔍 Checking Live Frontend Connection")
    print("=" * 50)
    
    # Let's check what happens if we call the frontend directly
    print("🌐 Testing frontend at orchestratex.me...")
    
    try:
        # First, let's see if we can access the site
        response = requests.get("https://orchestratex.me", timeout=10)
        print(f"   Frontend status: {response.status_code}")
        
        # Look for API configuration in the response
        content = response.text
        if "localhost:8002" in content:
            print("   ❌ Frontend still points to localhost:8002")
        elif "orchestratex-backend" in content:
            print("   ⚠️ Frontend points to old backend")
        elif "orchestratex-api-84388526388" in content:
            print("   ✅ Frontend points to new Python API")
        else:
            print("   ❓ Could not determine API URL from frontend")
            
    except Exception as e:
        print(f"   ❌ Could not access frontend: {e}")
    
    print("\n💡 Diagnosis:")
    print("The message WAS stored in Firestore, but at 6:57 am")
    print("Your frontend screenshot shows 6:24 am")
    print("This suggests:")
    print("1. Your frontend might be caching responses")
    print("2. Or pointing to a different backend")
    print("3. Or the frontend needs to be redeployed with new config")
    
    print("\n🔧 Solutions:")
    print("1. Clear browser cache and try again")
    print("2. Check if frontend is deployed with updated API URLs")
    print("3. Verify the frontend build includes our changes")

if __name__ == "__main__":
    check_frontend_connection()