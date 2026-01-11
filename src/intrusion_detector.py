"""
SentinelEdge - Intrusion Detection Logic Module
Implements time-based and confidence-based intrusion decision logic.
Edge Computing: All logic runs locally without cloud dependencies.
"""

from enum import Enum
from datetime import datetime
import time


class IntrusionState(Enum):
    """Intrusion detection states."""
    CLEAR = "CLEAR"           # No person detected
    DETECTING = "DETECTING"   # Person detected, analyzing
    ALERT = "ALERT"           # Intrusion confirmed, alert triggered


class IntrusionDetector:
    """
    Manages intrusion detection logic with time-based and confidence-based filtering.
    Prevents false alarms by requiring continuous detection over time.
    """
    
    def __init__(self, 
                 detection_threshold_seconds=3.0,
                 confidence_threshold=0.6,
                 clear_timeout_seconds=2.0):
        """
        Initialize intrusion detector.
        
        Args:
            detection_threshold_seconds (float): Time person must be continuously
                                                 detected before triggering alert
            confidence_threshold (float): Minimum average confidence (0-1)
            clear_timeout_seconds (float): Time without detection before returning 
                                          to CLEAR state
        """
        self.detection_threshold = detection_threshold_seconds
        self.confidence_threshold = confidence_threshold
        self.clear_timeout = clear_timeout_seconds
        
        # State tracking
        self.state = IntrusionState.CLEAR
        self.detection_start_time = None
        self.last_detection_time = None
        self.alert_triggered_time = None
        
        # Detection history for confidence averaging
        self.confidence_history = []
        self.max_history_size = 30  # Last 30 detections (~1 second at 30fps)
        
        # Statistics
        self.total_detections = 0
        self.total_alerts = 0
        self.false_alarm_preventions = 0
        
    def update(self, person_detected, person_count=0, max_confidence=0.0):
        """
        Update intrusion state based on detection results.
        
        Args:
            person_detected (bool): Whether any person was detected this frame
            person_count (int): Number of persons detected
            max_confidence (float): Highest confidence score among detections
            
        Returns:
            dict: State information including current state, time in state, etc.
        """
        current_time = time.time()
        
        if person_detected:
            self.total_detections += 1
            self.last_detection_time = current_time
            
            # Add to confidence history
            self.confidence_history.append(max_confidence)
            if len(self.confidence_history) > self.max_history_size:
                self.confidence_history.pop(0)
            
            # Calculate average confidence
            avg_confidence = sum(self.confidence_history) / len(self.confidence_history)
            
            # State machine logic
            if self.state == IntrusionState.CLEAR:
                # Transition to DETECTING
                self.state = IntrusionState.DETECTING
                self.detection_start_time = current_time
                
            elif self.state == IntrusionState.DETECTING:
                # Check if we've been detecting long enough
                time_detecting = current_time - self.detection_start_time
                
                # Check confidence threshold
                if avg_confidence < self.confidence_threshold:
                    # Low confidence - might be false positive
                    self.false_alarm_preventions += 1
                    # Stay in DETECTING but don't trigger
                    pass
                elif time_detecting >= self.detection_threshold:
                    # Threshold exceeded with good confidence - trigger alert
                    self.state = IntrusionState.ALERT
                    self.alert_triggered_time = current_time
                    self.total_alerts += 1
            
            # If already in ALERT, stay there while person present
            
        else:
            # No person detected
            if self.state == IntrusionState.CLEAR:
                # Already clear, nothing to do
                pass
                
            elif self.state == IntrusionState.DETECTING:
                # Check if we've been without detection long enough
                if self.last_detection_time:
                    time_since_detection = current_time - self.last_detection_time
                    if time_since_detection >= self.clear_timeout:
                        # Return to CLEAR
                        self.state = IntrusionState.CLEAR
                        self.detection_start_time = None
                        self.confidence_history = []
                        
            elif self.state == IntrusionState.ALERT:
                # Check if we should clear the alert
                if self.last_detection_time:
                    time_since_detection = current_time - self.last_detection_time
                    if time_since_detection >= self.clear_timeout:
                        # Return to CLEAR
                        self.state = IntrusionState.CLEAR
                        self.detection_start_time = None
                        self.alert_triggered_time = None
                        self.confidence_history = []
        
        # Calculate time in current state
        time_in_state = 0.0
        if self.state == IntrusionState.DETECTING and self.detection_start_time:
            time_in_state = current_time - self.detection_start_time
        elif self.state == IntrusionState.ALERT and self.alert_triggered_time:
            time_in_state = current_time - self.alert_triggered_time
        
        # Calculate average confidence
        avg_confidence = (sum(self.confidence_history) / len(self.confidence_history) 
                         if self.confidence_history else 0.0)
        
        return {
            'state': self.state,
            'person_count': person_count,
            'avg_confidence': avg_confidence,
            'time_in_state': time_in_state,
            'detection_threshold': self.detection_threshold,
            'is_intrusion': self.state == IntrusionState.ALERT,
            'timestamp': datetime.now()
        }
    
    def get_statistics(self):
        """Get detection statistics."""
        return {
            'total_detections': self.total_detections,
            'total_alerts': self.total_alerts,
            'false_alarm_preventions': self.false_alarm_preventions,
            'current_state': self.state.value,
            'detection_threshold': self.detection_threshold,
            'confidence_threshold': self.confidence_threshold
        }
    
    def reset(self):
        """Reset detector to initial state."""
        self.state = IntrusionState.CLEAR
        self.detection_start_time = None
        self.last_detection_time = None
        self.alert_triggered_time = None
        self.confidence_history = []


def main():
    """Test intrusion detection logic with live camera feed."""
    print("\n" + "="*60)
    print("SENTINEDGE - INTRUSION DETECTION SYSTEM TEST")
    print("="*60)
    print("Testing complete intrusion detection with decision logic")
    print("="*60 + "\n")
    
    # Import required modules
    from camera_feed import CameraFeed
    from person_detector import PersonDetector
    import cv2
    
    # Initialize components
    print("[INIT] Loading AI model...")
    detector = PersonDetector(model_name='yolov8n.pt', confidence_threshold=0.5)
    if not detector.load_model():
        print("[ERROR] Failed to load model")
        return
    
    print("[INIT] Initializing intrusion logic...")
    intrusion_detector = IntrusionDetector(
        detection_threshold_seconds=3.0,  # Must see person for 3 seconds
        confidence_threshold=0.6,          # Average confidence must be >60%
        clear_timeout_seconds=2.0          # 2 seconds without detection = clear
    )
    
    print("[INIT] Starting camera...")
    camera = CameraFeed(camera_id=0)
    if not camera.start():
        print("[ERROR] Failed to start camera")
        return
    
    info = detector.get_device_info()
    print(f"\n[DEVICE INFO]")
    print(f"  Device: {info['device'].upper()}")
    print(f"  Model: {info['model']}")
    
    print(f"\n[INTRUSION SETTINGS]")
    print(f"  Detection Threshold: {intrusion_detector.detection_threshold}s")
    print(f"  Confidence Threshold: {intrusion_detector.confidence_threshold}")
    print(f"  Clear Timeout: {intrusion_detector.clear_timeout}s")
    
    print("\n" + "="*60)
    print("INTRUSION DETECTION ACTIVE")
    print("="*60)
    print("[INFO] System will trigger alert after 3 seconds of detection")
    print("[INFO] Move in front of camera and stay for 3+ seconds")
    print("[CONTROLS] Press 'q' or ESC to exit")
    print("="*60 + "\n")
    
    frame_count = 0
    
    try:
        while camera.is_running:
            ret, frame = camera.get_frame()
            
            if not ret:
                print("[WARNING] Failed to grab frame")
                break
            
            frame_count += 1
            
            # Run person detection
            annotated_frame, person_count, detections = detector.detect_persons(frame)
            
            # Get max confidence from detections
            max_confidence = max([d['confidence'] for d in detections], default=0.0)
            
            # Update intrusion logic
            state_info = intrusion_detector.update(
                person_detected=(person_count > 0),
                person_count=person_count,
                max_confidence=max_confidence
            )
            
            # Determine colors based on state
            if state_info['state'] == IntrusionState.ALERT:
                status_color = (0, 0, 255)  # Red - ALERT
                status_bg_color = (0, 0, 200)
                status_text = "⚠ INTRUSION ALERT ⚠"
            elif state_info['state'] == IntrusionState.DETECTING:
                status_color = (0, 165, 255)  # Orange - DETECTING
                status_bg_color = (0, 140, 200)
                status_text = "ANALYZING..."
            else:
                status_color = (0, 255, 0)  # Green - CLEAR
                status_bg_color = (0, 200, 0)
                status_text = "SYSTEM CLEAR"
            
            # Draw status banner
            cv2.rectangle(annotated_frame, (0, 0), (annotated_frame.shape[1], 120), 
                         (0, 0, 0), -1)
            
            # Title
            cv2.putText(annotated_frame, "SentinelEdge - Intrusion Detection",
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            # Status
            cv2.putText(annotated_frame, f"STATUS: {status_text}",
                       (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, status_color, 2)
            
            # Details
            if state_info['state'] == IntrusionState.DETECTING:
                progress = min(state_info['time_in_state'] / state_info['detection_threshold'], 1.0)
                detail_text = f"Detecting: {state_info['time_in_state']:.1f}s / {state_info['detection_threshold']:.1f}s ({progress*100:.0f}%)"
            elif state_info['state'] == IntrusionState.ALERT:
                detail_text = f"Alert Duration: {state_info['time_in_state']:.1f}s | Persons: {person_count}"
            else:
                detail_text = f"No threats detected"
            
            cv2.putText(annotated_frame, detail_text,
                       (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            
            # Confidence info
            if person_count > 0:
                cv2.putText(annotated_frame, 
                           f"Confidence: {state_info['avg_confidence']:.2f}",
                           (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
            
            # Controls
            cv2.putText(annotated_frame, "Press 'q' or ESC to exit",
                       (10, annotated_frame.shape[0] - 20),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)
            
            # Display frame
            cv2.imshow('SentinelEdge - Intrusion Detection System', annotated_frame)
            
            # Check for exit
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q') or key == 27:
                print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Exit requested")
                break
    
    except KeyboardInterrupt:
        print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Interrupted by user")
    
    finally:
        # Cleanup
        camera.stop()
        cv2.destroyAllWindows()
        
        # Display statistics
        stats = intrusion_detector.get_statistics()
        print(f"\n[STATISTICS]")
        print(f"  Total frames: {frame_count}")
        print(f"  Total detections: {stats['total_detections']}")
        print(f"  Total alerts: {stats['total_alerts']}")
        print(f"  False alarms prevented: {stats['false_alarm_preventions']}")
        print(f"  Final state: {stats['current_state']}")
        print("\n[INFO] Intrusion detection system closed successfully\n")


if __name__ == "__main__":
    main()
