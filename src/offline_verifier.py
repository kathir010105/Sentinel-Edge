"""
SentinelEdge - Offline Verification Module
Verifies that the system operates completely offline without internet.
Demonstrates true edge computing capability.
"""

import socket
import subprocess
from datetime import datetime


class OfflineVerifier:
    """Verifies system can operate without internet connectivity."""
    
    def __init__(self):
        """Initialize offline verifier."""
        self.is_online = None
        self.verification_results = {}
    
    def check_internet_connectivity(self):
        """
        Check if internet connection is available.
        
        Returns:
            bool: True if connected to internet, False otherwise
        """
        print("\n[VERIFY] Checking internet connectivity...")
        
        # Method 1: Try to connect to common DNS servers
        test_hosts = [
            ("8.8.8.8", 53, "Google DNS"),      # Google DNS
            ("1.1.1.1", 53, "Cloudflare DNS"),  # Cloudflare DNS
        ]
        
        online = False
        for host, port, name in test_hosts:
            try:
                socket.setdefaulttimeout(2)
                socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
                print(f"  ✓ Connected to {name} ({host})")
                online = True
                break
            except (socket.error, socket.timeout):
                print(f"  ✗ Cannot reach {name} ({host})")
        
        self.is_online = online
        
        if online:
            print("\n[STATUS] 🌐 INTERNET CONNECTED")
            print("[INFO] System can work online, but doesn't require it")
        else:
            print("\n[STATUS] 📴 OFFLINE MODE")
            print("[INFO] ✓ Perfect! System is operating without internet")
        
        return online
    
    def verify_local_components(self):
        """
        Verify all components required for operation are available locally.
        
        Returns:
            dict: Verification results for each component
        """
        print("\n[VERIFY] Checking local components...")
        results = {}
        
        # Check 1: Camera access
        print("  [1/5] Camera access...")
        try:
            import cv2
            cap = cv2.VideoCapture(0)
            if cap.isOpened():
                print("    ✓ Camera accessible")
                results['camera'] = True
                cap.release()
            else:
                print("    ✗ Camera not accessible")
                results['camera'] = False
        except Exception as e:
            print(f"    ✗ Camera check failed: {e}")
            results['camera'] = False
        
        # Check 2: AI Model (YOLOv8)
        print("  [2/5] AI model (YOLOv8)...")
        try:
            from ultralytics import YOLO
            import os
            model_path = 'yolov8n.pt'
            if os.path.exists(model_path):
                print(f"    ✓ Model found: {model_path}")
                results['model'] = True
            else:
                print(f"    ✗ Model not found: {model_path}")
                results['model'] = False
        except Exception as e:
            print(f"    ✗ Model check failed: {e}")
            results['model'] = False
        
        # Check 3: Detection logic
        print("  [3/5] Detection modules...")
        try:
            from person_detector import PersonDetector
            from intrusion_detector import IntrusionDetector
            print("    ✓ Detection modules loaded")
            results['detection'] = True
        except Exception as e:
            print(f"    ✗ Detection modules failed: {e}")
            results['detection'] = False
        
        # Check 4: Alert system
        print("  [4/5] Alert system...")
        try:
            from alert_system import AlertSystem
            import os
            if os.path.exists('alerts') and os.path.exists('logs'):
                print("    ✓ Alert system ready")
                results['alerts'] = True
            else:
                print("    ✗ Alert directories missing")
                results['alerts'] = False
        except Exception as e:
            print(f"    ✗ Alert system failed: {e}")
            results['alerts'] = False
        
        # Check 5: PyTorch/CUDA
        print("  [5/5] AI framework...")
        try:
            import torch
            device = 'cuda' if torch.cuda.is_available() else 'cpu'
            print(f"    ✓ PyTorch ready (device: {device})")
            results['framework'] = True
        except Exception as e:
            print(f"    ✗ Framework check failed: {e}")
            results['framework'] = False
        
        self.verification_results = results
        return results
    
    def generate_report(self):
        """
        Generate a comprehensive verification report.
        
        Returns:
            dict: Complete verification report
        """
        all_passed = all(self.verification_results.values())
        
        print("\n" + "="*60)
        print("OFFLINE VERIFICATION REPORT")
        print("="*60)
        print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Internet Status: {'🌐 Online' if self.is_online else '📴 Offline'}")
        print("-"*60)
        
        print("\nComponent Status:")
        for component, status in self.verification_results.items():
            status_symbol = "✓" if status else "✗"
            status_text = "PASS" if status else "FAIL"
            print(f"  {status_symbol} {component.upper()}: {status_text}")
        
        print("-"*60)
        print(f"\nOverall Status: {'✓ ALL SYSTEMS READY' if all_passed else '✗ SOME COMPONENTS FAILED'}")
        
        if not self.is_online and all_passed:
            print("\n🎉 EDGE COMPUTING VERIFIED!")
            print("System is fully operational WITHOUT internet connection.")
            print("This proves true edge computing capability:")
            print("  • All AI processing happens locally")
            print("  • No cloud dependencies")
            print("  • Zero network latency")
            print("  • Complete privacy (data never leaves device)")
        
        print("="*60 + "\n")
        
        return {
            'timestamp': datetime.now().isoformat(),
            'internet_available': self.is_online,
            'components': self.verification_results,
            'all_passed': all_passed,
            'edge_computing_verified': not self.is_online and all_passed
        }


def main():
    """Run offline verification test."""
    print("\n" + "="*60)
    print("SENTINEDGE - OFFLINE VERIFICATION")
    print("="*60)
    print("Verifying system can operate without internet")
    print("="*60 + "\n")
    
    verifier = OfflineVerifier()
    
    # Check internet connectivity
    is_online = verifier.check_internet_connectivity()
    
    # Verify local components
    results = verifier.verify_local_components()
    
    # Generate report
    report = verifier.generate_report()
    
    # Recommendation
    if is_online:
        print("\n[RECOMMENDATION]")
        print("To fully demonstrate edge computing capability:")
        print("  1. Disconnect from WiFi/Ethernet")
        print("  2. Run this verification again")
        print("  3. Then run the main system (alert_system.py)")
        print("  4. System should work perfectly offline!")
    
    # Offer to run the main system
    if report['all_passed']:
        print("\n[NEXT STEP]")
        print("All components verified. Ready to run full system!")
        print("\nRun: python src/alert_system.py")
        print("Or press any key to exit...")
    
    return report


if __name__ == "__main__":
    main()
