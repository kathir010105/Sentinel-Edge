"""
SentinelEdge - Camera Feed Module
Captures live video feed from webcam for intrusion detection.
Edge Computing: Processes video locally without cloud dependencies.
"""

import cv2
import sys
from datetime import datetime


class CameraFeed:
    """Handles webcam capture and display for edge-based processing."""
    
    def __init__(self, camera_id=0):
        """
        Initialize camera feed.
        
        Args:
            camera_id (int): Camera device ID (0 for default webcam)
        """
        self.camera_id = camera_id
        self.cap = None
        self.is_running = False
        
    def start(self):
        """Start camera capture."""
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Initializing camera {self.camera_id}...")
        
        # Open camera
        self.cap = cv2.VideoCapture(self.camera_id)
        
        # Check if camera opened successfully
        if not self.cap.isOpened():
            print(f"[ERROR] Cannot access camera {self.camera_id}")
            print("Possible issues:")
            print("  - Camera is being used by another application")
            print("  - Camera permissions not granted")
            print("  - Invalid camera ID")
            return False
        
        # Set camera properties for better performance
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        self.is_running = True
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Camera started successfully")
        print(f"[INFO] Resolution: 640x480")
        return True
    
    def get_frame(self):
        """
        Capture a single frame from camera.
        
        Returns:
            tuple: (success, frame) where success is boolean and frame is numpy array
        """
        if not self.is_running or self.cap is None:
            return False, None
        
        ret, frame = self.cap.read()
        return ret, frame
    
    def stop(self):
        """Release camera resources."""
        if self.cap is not None:
            self.cap.release()
        self.is_running = False
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Camera stopped")
    
    def display_feed(self):
        """
        Display live camera feed in a window.
        Press 'q' or ESC to exit.
        """
        if not self.start():
            return
        
        print("\n" + "="*60)
        print("SENTINEDGE - LIVE CAMERA FEED")
        print("="*60)
        print("[INFO] Camera feed is running")
        print("[CONTROLS] Press 'q' or ESC to exit")
        print("="*60 + "\n")
        
        frame_count = 0
        
        try:
            while self.is_running:
                ret, frame = self.get_frame()
                
                if not ret:
                    print("[WARNING] Failed to grab frame")
                    break
                
                frame_count += 1
                
                # Add info overlay on frame
                cv2.putText(frame, "SentinelEdge - Live Feed", 
                           (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 
                           0.7, (0, 255, 0), 2)
                
                cv2.putText(frame, f"Frame: {frame_count}", 
                           (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 
                           0.5, (0, 255, 0), 1)
                
                cv2.putText(frame, "Press 'q' or ESC to exit", 
                           (10, frame.shape[0] - 20), 
                           cv2.FONT_HERSHEY_SIMPLEX, 
                           0.5, (0, 255, 255), 1)
                
                # Display the frame
                cv2.imshow('SentinelEdge - Camera Feed', frame)
                
                # Check for exit key (q or ESC)
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q') or key == 27:  # 27 is ESC key
                    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Exit requested by user")
                    break
        
        except KeyboardInterrupt:
            print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Interrupted by user")
        
        finally:
            # Cleanup
            self.stop()
            cv2.destroyAllWindows()
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Total frames processed: {frame_count}")
            print("[INFO] Camera feed closed successfully\n")


def main():
    """Main function to run camera feed test."""
    print("\n" + "="*60)
    print("SENTINEDGE - CAMERA FEED TEST")
    print("="*60)
    print("This module tests the camera feed for edge-based detection.")
    print("="*60 + "\n")
    
    # Create camera feed instance
    camera = CameraFeed(camera_id=0)
    
    # Display live feed
    camera.display_feed()


if __name__ == "__main__":
    main()
