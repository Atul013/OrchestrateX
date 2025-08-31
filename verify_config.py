#!/usr/bin/env python3
"""
Configuration Verification Script
Run this tomorrow to verify all ports are configured correctly
"""

import json
import os
from pathlib import Path

def check_configuration():
    print("🔍 OrchestrateX Configuration Verification")
    print("=" * 50)
    
    config_status = {
        "docker_compose": False,
        "working_api": False,
        "batch_files": False,
        "simple_orchestrate": False
    }
    
    try:
        # Check docker-compose.yml
        with open('docker-compose.yml', 'r') as f:
            docker_content = f.read()
            if '"27019:27017"' in docker_content:
                print("✅ docker-compose.yml: Port 27019 configured")
                config_status["docker_compose"] = True
            else:
                print("❌ docker-compose.yml: Port 27019 NOT found")
        
        # Check working_api.py
        with open('working_api.py', 'r') as f:
            api_content = f.read()
            if 'localhost:27019' in api_content:
                print("✅ working_api.py: Port 27019 configured")
                config_status["working_api"] = True
            else:
                print("❌ working_api.py: Port 27019 NOT found")
        
        # Check batch files
        with open('start_mongodb.bat', 'r') as f:
            batch_content = f.read()
            if 'localhost:27019' in batch_content:
                print("✅ start_mongodb.bat: Port 27019 configured")
                config_status["batch_files"] = True
            else:
                print("❌ start_mongodb.bat: Port 27019 NOT found")
        
        # Check simple_orchestrateX.py
        with open('simple_orchestrateX.py', 'r') as f:
            simple_content = f.read()
            if 'localhost:27019' in simple_content:
                print("✅ simple_orchestrateX.py: Port 27019 configured")
                config_status["simple_orchestrate"] = True
            else:
                print("❌ simple_orchestrateX.py: Port 27019 NOT found")
        
        print("\n📊 Configuration Summary:")
        print("=" * 30)
        
        all_good = all(config_status.values())
        
        for component, status in config_status.items():
            emoji = "✅" if status else "❌"
            print(f"{emoji} {component}: {'OK' if status else 'NEEDS UPDATE'}")
        
        print("\n" + "=" * 50)
        if all_good:
            print("🎉 ALL CONFIGURATIONS CORRECT!")
            print("✅ Your system is ready for tomorrow!")
            print("✅ Just run: start_full_system.bat")
        else:
            print("⚠️  Some configurations need updates")
            print("🔧 Check the failed items above")
        
        print("\n🌐 Expected URLs tomorrow:")
        print("   Frontend: http://localhost:5176+ (auto-assigned)")
        print("   Backend:  http://localhost:8002")
        print("   MongoDB:  mongodb://localhost:27019")
        print("   DB Admin: http://localhost:8081 (admin/admin)")
        
        return all_good
        
    except FileNotFoundError as e:
        print(f"❌ File not found: {e}")
        return False
    except Exception as e:
        print(f"❌ Error checking configuration: {e}")
        return False

if __name__ == "__main__":
    success = check_configuration()
    
    if success:
        print("\n🚀 Ready to start tomorrow!")
    else:
        print("\n🔧 Please fix the configuration issues above")
    
    input("\nPress Enter to exit...")
