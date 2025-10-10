#!/usr/bin/env python3
"""
Verify that all 287 BMRS API endpoints are accessible through the client.

This script checks that the BMRSClient properly inherits from GeneratedBMRSMethods
and that all endpoints are available.
"""

def verify_endpoints():
    """Verify all 287 endpoints are accessible."""
    try:
        from elexon_bmrs import BMRSClient
        
        # Create client instance
        client = BMRSClient()
        
        # Get all get_ methods
        methods = [m for m in dir(client) if m.startswith('get_')]
        
        print(f"✅ Total get_ methods found: {len(methods)}")
        
        if len(methods) == 287:
            print("🎉 SUCCESS: All 287 endpoints are accessible!")
        else:
            print(f"❌ ERROR: Expected 287 methods, found {len(methods)}")
            return False
        
        # Test a few key methods exist
        key_methods = [
            'get_balancing_dynamic',
            'get_generation_actual_per_type', 
            'get_demand_outturn_national',
            'get_datasets_freq',
            'get_system_frequency'
        ]
        
        print("\n🔍 Testing key methods:")
        for method in key_methods:
            if hasattr(client, method):
                print(f"  ✅ {method}")
            else:
                print(f"  ❌ {method} - MISSING!")
                return False
        
        # Test method documentation
        print("\n📚 Testing method documentation:")
        try:
            help_text = help(client.get_balancing_dynamic)
            print("  ✅ Method documentation accessible")
        except Exception as e:
            print(f"  ❌ Method documentation error: {e}")
            return False
        
        print("\n🎯 All verification tests passed!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure to install the package: pip install -e .")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Verifying BMRS API Client Endpoints")
    print("=" * 50)
    
    success = verify_endpoints()
    
    if success:
        print("\n✅ VERIFICATION COMPLETE: All 287 endpoints are properly accessible!")
        exit(0)
    else:
        print("\n❌ VERIFICATION FAILED: Some endpoints are missing or inaccessible.")
        exit(1)
