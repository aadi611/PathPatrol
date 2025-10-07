"""
Test script to verify PWA implementation
Checks all required files and configurations
"""
import json
from pathlib import Path


def test_pwa_setup():
    """Test PWA configuration"""
    print("🔍 Testing PWA Setup...\n")
    
    project_root = Path(__file__).parent
    issues = []
    successes = []
    
    # 1. Check manifest.json
    print("1️⃣ Checking manifest.json...")
    manifest_path = project_root / 'static' / 'manifest.json'
    if manifest_path.exists():
        try:
            with open(manifest_path, 'r') as f:
                manifest = json.load(f)
            
            # Verify required fields
            required_fields = ['name', 'short_name', 'start_url', 'display', 'icons']
            for field in required_fields:
                if field not in manifest:
                    issues.append(f"Manifest missing required field: {field}")
                else:
                    successes.append(f"✅ Manifest has {field}")
            
            # Check icons
            if 'icons' in manifest:
                print(f"   Found {len(manifest['icons'])} icon definitions")
                successes.append(f"✅ Manifest has {len(manifest['icons'])} icons")
            
        except json.JSONDecodeError as e:
            issues.append(f"Manifest JSON invalid: {e}")
    else:
        issues.append("Manifest file not found at static/manifest.json")
    
    # 2. Check service worker
    print("\n2️⃣ Checking service-worker.js...")
    sw_path = project_root / 'static' / 'service-worker.js'
    if sw_path.exists():
        successes.append("✅ Service worker file exists")
        with open(sw_path, 'r') as f:
            sw_content = f.read()
            if 'addEventListener' in sw_content:
                successes.append("✅ Service worker has event listeners")
            if 'install' in sw_content:
                successes.append("✅ Service worker has install event")
            if 'fetch' in sw_content:
                successes.append("✅ Service worker has fetch event")
    else:
        issues.append("Service worker not found at static/service-worker.js")
    
    # 3. Check offline page
    print("\n3️⃣ Checking offline.html...")
    offline_path = project_root / 'static' / 'offline.html'
    if offline_path.exists():
        successes.append("✅ Offline page exists")
    else:
        issues.append("Offline page not found at static/offline.html")
    
    # 4. Check icons
    print("\n4️⃣ Checking PWA icons...")
    icons_dir = project_root / 'static' / 'icons'
    required_sizes = [72, 96, 128, 144, 152, 192, 384, 512]
    
    if icons_dir.exists():
        existing_icons = list(icons_dir.glob('icon-*.png'))
        print(f"   Found {len(existing_icons)} icon files")
        
        for size in required_sizes:
            icon_file = icons_dir / f'icon-{size}x{size}.png'
            if icon_file.exists():
                successes.append(f"✅ Icon {size}x{size} exists")
            else:
                issues.append(f"Missing icon: {size}x{size}.png")
    else:
        issues.append("Icons directory not found at static/icons/")
    
    # 5. Check Streamlit config
    print("\n5️⃣ Checking Streamlit configuration...")
    config_path = project_root / '.streamlit' / 'config.toml'
    if config_path.exists():
        successes.append("✅ Streamlit config exists")
        with open(config_path, 'r') as f:
            config_content = f.read()
            if 'enableStaticServing' in config_content:
                successes.append("✅ Static serving is configured")
            else:
                issues.append("Static serving not enabled in config.toml")
    else:
        issues.append("Streamlit config not found at .streamlit/config.toml")
    
    # 6. Check PWA utilities
    print("\n6️⃣ Checking PWA utilities...")
    pwa_utils_path = project_root / 'utils' / 'pwa_utils.py'
    if pwa_utils_path.exists():
        successes.append("✅ PWA utilities exist")
    else:
        issues.append("PWA utilities not found at utils/pwa_utils.py")
    
    # Print results
    print("\n" + "="*60)
    print("📊 TEST RESULTS")
    print("="*60)
    
    if successes:
        print(f"\n✅ PASSED ({len(successes)}):")
        for success in successes:
            print(f"  {success}")
    
    if issues:
        print(f"\n❌ ISSUES ({len(issues)}):")
        for issue in issues:
            print(f"  ❌ {issue}")
    else:
        print("\n🎉 All checks passed!")
    
    # Overall score
    total_checks = len(successes) + len(issues)
    score = (len(successes) / total_checks * 100) if total_checks > 0 else 0
    
    print(f"\n📈 PWA Readiness Score: {score:.1f}%")
    
    if score == 100:
        print("\n✅ Your PWA is fully configured and ready to deploy!")
        print("\n📋 Next Steps:")
        print("  1. Run the app: streamlit run app.py")
        print("  2. Open in Chrome and test install")
        print("  3. Test offline mode in DevTools")
        print("  4. Deploy with HTTPS for production")
    elif score >= 80:
        print("\n⚠️ Your PWA is mostly ready, but has some issues to fix.")
    else:
        print("\n❌ Your PWA needs more work before deployment.")
    
    return len(issues) == 0


if __name__ == '__main__':
    test_pwa_setup()
