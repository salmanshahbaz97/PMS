#!/usr/bin/env python
"""
Test script to verify deployment readiness
"""
import os
import sys
from pathlib import Path

def test_imports():
    """Test if all required packages can be imported"""
    print("🔍 Testing imports...")
    
    try:
        import django
        print("✅ Django imported successfully")
    except ImportError as e:
        print(f"❌ Django import failed: {e}")
        return False
    
    try:
        import whitenoise
        print("✅ WhiteNoise imported successfully")
    except ImportError as e:
        print(f"❌ WhiteNoise import failed: {e}")
        return False
    
    try:
        import gunicorn
        print("✅ Gunicorn imported successfully")
    except ImportError as e:
        print(f"❌ Gunicorn import failed: {e}")
        return False
    
    try:
        import dj_database_url
        print("✅ dj-database-url imported successfully")
    except ImportError as e:
        print(f"❌ dj-database-url import failed: {e}")
        return False
    
    try:
        import decouple
        print("✅ python-decouple imported successfully")
    except ImportError as e:
        print(f"❌ python-decouple import failed: {e}")
        return False
    
    return True

def test_files():
    """Test if all required files exist"""
    print("\n📁 Testing required files...")
    
    required_files = [
        'requirements.txt',
        'Procfile',
        'runtime.txt',
        'manage.py',
        'pms/settings.py',
        'pms/urls.py',
        'core/urls.py',
        'core/views.py',
        'core/models.py',
        'static/css/style.css',
        'static/js/main.js'
    ]
    
    all_exist = True
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - MISSING")
            all_exist = False
    
    return all_exist

def test_settings():
    """Test Django settings configuration"""
    print("\n⚙️ Testing Django settings...")
    
    try:
        # Set up Django environment
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pms.settings')
        import django
        django.setup()
        
        from django.conf import settings
        
        # Test critical settings
        if hasattr(settings, 'SECRET_KEY'):
            print("✅ SECRET_KEY configured")
        else:
            print("❌ SECRET_KEY missing")
            return False
        
        if hasattr(settings, 'DATABASES'):
            print("✅ DATABASES configured")
        else:
            print("❌ DATABASES missing")
            return False
        
        if hasattr(settings, 'STATIC_ROOT'):
            print("✅ STATIC_ROOT configured")
        else:
            print("❌ STATIC_ROOT missing")
            return False
        
        if 'whitenoise.middleware.WhiteNoiseMiddleware' in settings.MIDDLEWARE:
            print("✅ WhiteNoise middleware configured")
        else:
            print("❌ WhiteNoise middleware missing")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Settings test failed: {e}")
        return False

def main():
    """Run all deployment tests"""
    print("🚀 PMS Deployment Readiness Test")
    print("=" * 40)
    
    tests = [
        ("Import Test", test_imports),
        ("Files Test", test_files),
        ("Settings Test", test_settings)
    ]
    
    all_passed = True
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        if not test_func():
            all_passed = False
    
    print("\n" + "=" * 40)
    if all_passed:
        print("🎉 ALL TESTS PASSED! Your code is ready for deployment!")
        print("\n📋 Next steps:")
        print("1. Push your code to GitHub")
        print("2. Follow the Render deployment guide")
        print("3. Set up environment variables")
        print("4. Deploy!")
    else:
        print("❌ Some tests failed. Please fix the issues above before deploying.")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 