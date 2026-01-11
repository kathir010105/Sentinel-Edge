"""
SentinelEdge - Alert System Module
Handles alert triggers, screenshot capture, event logging, and notifications.
Edge Computing: All alerts generated and stored locally without cloud dependencies.
"""

import cv2
import os
from datetime import datetime
import json


class AlertSystem:
    """
    Manages alert generation, evidence capture, and event logging.
    Designed for edge deployment with local storage.
    """
    
    def __init__(self, alerts_dir='alerts', logs_dir='logs'):
        """
        Initialize alert system.
        
        Args:
            alerts_dir (str): Directory to save alert screenshots/videos
            logs_dir (str): Directory to save event logs
        """
        self.alerts_dir = alerts_dir
        self.logs_dir = logs_dir
        
        # Create directories if they don't exist
        os.makedirs(self.alerts_dir, exist_ok=True)
        os.makedirs(self.logs_dir, exist_ok=True)
        
        # Alert tracking
        self.current_alert_id = None
        self.alert_count = 0
        self.last_alert_time = None
        self.alert_active = False
        
        # Evidence collection
        self.alert_screenshots = []
        self.max_screenshots_per_alert = 5
        
        # Log file path
        self.log_file = os.path.join(self.logs_dir, 'intrusion_log.txt')
        self.json_log_file = os.path.join(self.logs_dir, 'intrusion_log.json')
        
        # Initialize logs
        self._initialize_logs()
        
        print(f"[ALERT] Alert system initialized")
        print(f"[ALERT] Screenshots will be saved to: {os.path.abspath(self.alerts_dir)}")
        print(f"[ALERT] Logs will be saved to: {os.path.abspath(self.logs_dir)}")
    
    def _initialize_logs(self):
        """Initialize log files if they don't exist."""
        # Text log
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w') as f:
                f.write("="*60 + "\n")
                f.write("SentinelEdge - Intrusion Detection Log\n")
                f.write("="*60 + "\n")
                f.write(f"Log created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("="*60 + "\n\n")
        
        # JSON log
        if not os.path.exists(self.json_log_file):
            with open(self.json_log_file, 'w') as f:
                json.dump([], f)
    
    def trigger_alert(self, frame, state_info, detections):
        """
        Trigger an alert when intrusion is detected.
        
        Args:
            frame (numpy.ndarray): Current video frame
            state_info (dict): State information from intrusion detector
            detections (list): List of person detections
            
        Returns:
            str: Alert ID for this alert
        """
        if not self.alert_active:
            # New alert triggered
            self.alert_count += 1
            self.current_alert_id = f"ALERT_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{self.alert_count:03d}"
            self.alert_active = True
            self.last_alert_time = datetime.now()
            self.alert_screenshots = []
            
            # Log alert start
            self._log_event("ALERT_START", state_info, detections)
            
            print(f"\n{'='*60}")
            print(f"🚨 ALERT TRIGGERED: {self.current_alert_id}")
            print(f"{'='*60}")
            print(f"Time: {self.last_alert_time.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"Persons detected: {state_info.get('person_count', 0)}")
            print(f"Confidence: {state_info.get('avg_confidence', 0):.2f}")
            print(f"{'='*60}\n")
        
        # Capture screenshot (limited to max per alert)
        if len(self.alert_screenshots) < self.max_screenshots_per_alert:
            screenshot_path = self._save_screenshot(frame, state_info)
            if screenshot_path:
                self.alert_screenshots.append(screenshot_path)
        
        return self.current_alert_id
    
    def clear_alert(self, state_info):
        """
        Clear active alert when system returns to CLEAR state.
        
        Args:
            state_info (dict): Final state information
        """
        if self.alert_active:
            # Log alert end
            self._log_event("ALERT_END", state_info, [])
            
            duration = (datetime.now() - self.last_alert_time).total_seconds()
            
            print(f"\n{'='*60}")
            print(f"✓ ALERT CLEARED: {self.current_alert_id}")
            print(f"{'='*60}")
            print(f"Duration: {duration:.1f}s")
            print(f"Screenshots captured: {len(self.alert_screenshots)}")
            print(f"{'='*60}\n")
            
            self.alert_active = False
            self.current_alert_id = None
    
    def _save_screenshot(self, frame, state_info):
        """
        Save a screenshot of the alert frame.
        
        Args:
            frame (numpy.ndarray): Frame to save
            state_info (dict): State information for filename
            
        Returns:
            str: Path to saved screenshot or None if failed
        """
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')[:-3]  # milliseconds
            filename = f"{self.current_alert_id}_{timestamp}.jpg"
            filepath = os.path.join(self.alerts_dir, filename)
            
            cv2.imwrite(filepath, frame)
            print(f"[ALERT] Screenshot saved: {filename}")
            
            return filepath
        
        except Exception as e:
            print(f"[ERROR] Failed to save screenshot: {e}")
            return None
    
    def _log_event(self, event_type, state_info, detections):
        """
        Log an event to both text and JSON log files.
        
        Args:
            event_type (str): Type of event (ALERT_START, ALERT_END, etc.)
            state_info (dict): State information
            detections (list): Detection information
        """
        timestamp = datetime.now()
        
        # Text log
        try:
            with open(self.log_file, 'a') as f:
                f.write(f"[{timestamp.strftime('%Y-%m-%d %H:%M:%S')}] {event_type}\n")
                f.write(f"  Alert ID: {self.current_alert_id}\n")
                f.write(f"  State: {state_info.get('state', 'UNKNOWN')}\n")
                f.write(f"  Persons: {state_info.get('person_count', 0)}\n")
                f.write(f"  Confidence: {state_info.get('avg_confidence', 0):.2f}\n")
                f.write(f"  Detections: {len(detections)}\n")
                f.write("-" * 60 + "\n")
        except Exception as e:
            print(f"[ERROR] Failed to write text log: {e}")
        
        # JSON log
        try:
            # Read existing logs
            with open(self.json_log_file, 'r') as f:
                logs = json.load(f)
            
            # Add new log entry
            log_entry = {
                'timestamp': timestamp.isoformat(),
                'event_type': event_type,
                'alert_id': self.current_alert_id,
                'state': str(state_info.get('state', 'UNKNOWN')),
                'person_count': state_info.get('person_count', 0),
                'avg_confidence': state_info.get('avg_confidence', 0),
                'detections_count': len(detections),
                'screenshots': self.alert_screenshots if event_type == 'ALERT_END' else []
            }
            logs.append(log_entry)
            
            # Write back
            with open(self.json_log_file, 'w') as f:
                json.dump(logs, f, indent=2)
        
        except Exception as e:
            print(f"[ERROR] Failed to write JSON log: {e}")
    
    def get_statistics(self):
        """Get alert system statistics."""
        return {
            'total_alerts': self.alert_count,
            'alert_active': self.alert_active,
            'current_alert_id': self.current_alert_id,
            'alerts_dir': os.path.abspath(self.alerts_dir),
            'logs_dir': os.path.abspath(self.logs_dir)
        }


def main():
    """Test complete intrusion detection system with alerts."""
    print("\n" + "="*60)
    print("SENTINEDGE - COMPLETE SYSTEM TEST")
    print("="*60)
    print("Testing full intrusion detection with alert system")
    print("="*60 + "\n")
    
    # Import required modules
    from camera_feed import CameraFeed
    from person_detector import PersonDetector
    from intrusion_detector import IntrusionDetector, IntrusionState
    import cv2
    
    # Initialize all components
    print("[INIT] Loading AI model...")
    detector = PersonDetector(model_name='yolov8n.pt', confidence_threshold=0.5)
    if not detector.load_model():
        print("[ERROR] Failed to load model")
        return
    
    print("[INIT] Initializing intrusion logic...")
    intrusion_detector = IntrusionDetector(
        detection_threshold_seconds=3.0,
        confidence_threshold=0.6,
        clear_timeout_seconds=2.0
    )
    
    print("[INIT] Initializing alert system...")
    alert_system = AlertSystem(alerts_dir='alerts', logs_dir='logs')
    
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
    
    print("\n" + "="*60)
    print("🔴 SENTINEDGE SYSTEM ACTIVE")
    print("="*60)
    print("[INFO] System will capture screenshots and log events")
    print("[INFO] Stay in front of camera for 3+ seconds to trigger")
    print("[CONTROLS] Press 'q' or ESC to exit")
    print("="*60 + "\n")
    
    frame_count = 0
    alert_flash = False
    
    try:
        while camera.is_running:
            ret, frame = camera.get_frame()
            
            if not ret:
                print("[WARNING] Failed to grab frame")
                break
            
            frame_count += 1
            
            # Run person detection
            annotated_frame, person_count, detections = detector.detect_persons(frame)
            
            # Get max confidence
            max_confidence = max([d['confidence'] for d in detections], default=0.0)
            
            # Update intrusion logic
            state_info = intrusion_detector.update(
                person_detected=(person_count > 0),
                person_count=person_count,
                max_confidence=max_confidence
            )
            
            # Handle alerts based on state
            if state_info['state'] == IntrusionState.ALERT:
                alert_system.trigger_alert(annotated_frame, state_info, detections)
                alert_flash = not alert_flash  # Flashing effect
            else:
                if alert_system.alert_active:
                    alert_system.clear_alert(state_info)
                alert_flash = False
            
            # Determine colors based on state
            if state_info['state'] == IntrusionState.ALERT:
                status_color = (0, 0, 255) if alert_flash else (0, 0, 200)
                status_text = "⚠️ INTRUSION ALERT ⚠️"
                bg_color = (0, 0, 100)
            elif state_info['state'] == IntrusionState.DETECTING:
                status_color = (0, 165, 255)
                status_text = "🔍 ANALYZING..."
                bg_color = (20, 20, 20)
            else:
                status_color = (0, 255, 0)
                status_text = "✓ SYSTEM CLEAR"
                bg_color = (20, 20, 20)
            
            # Draw background banner
            cv2.rectangle(annotated_frame, (0, 0), (annotated_frame.shape[1], 140), 
                         bg_color, -1)
            
            # Title
            cv2.putText(annotated_frame, "SentinelEdge - Intrusion Detection System",
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            # Status
            cv2.putText(annotated_frame, f"STATUS: {status_text}",
                       (10, 65), cv2.FONT_HERSHEY_SIMPLEX, 0.8, status_color, 2)
            
            # Details
            if state_info['state'] == IntrusionState.DETECTING:
                progress = min(state_info['time_in_state'] / state_info['detection_threshold'], 1.0)
                detail_text = f"Detection: {state_info['time_in_state']:.1f}s / {state_info['detection_threshold']:.1f}s ({progress*100:.0f}%)"
            elif state_info['state'] == IntrusionState.ALERT:
                detail_text = f"Alert: {alert_system.current_alert_id} | Duration: {state_info['time_in_state']:.1f}s"
            else:
                detail_text = f"Monitoring... | Frame: {frame_count}"
            
            cv2.putText(annotated_frame, detail_text,
                       (10, 95), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            
            # Alert info
            if state_info['state'] != IntrusionState.CLEAR:
                info_text = f"Persons: {person_count} | Confidence: {state_info['avg_confidence']:.2f}"
                cv2.putText(annotated_frame, info_text,
                           (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            
            # Statistics corner
            alert_stats = alert_system.get_statistics()
            cv2.putText(annotated_frame, f"Total Alerts: {alert_stats['total_alerts']}",
                       (annotated_frame.shape[1] - 180, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            
            # Controls
            cv2.putText(annotated_frame, "Press 'q' or ESC to exit",
                       (10, annotated_frame.shape[0] - 20),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)
            
            # Display frame
            cv2.imshow('SentinelEdge - Complete System', annotated_frame)
            
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
        
        # Display final statistics
        stats = intrusion_detector.get_statistics()
        alert_stats = alert_system.get_statistics()
        
        print(f"\n{'='*60}")
        print("FINAL STATISTICS")
        print(f"{'='*60}")
        print(f"Total frames processed: {frame_count}")
        print(f"Total detections: {stats['total_detections']}")
        print(f"Total alerts triggered: {alert_stats['total_alerts']}")
        print(f"False alarms prevented: {stats['false_alarm_preventions']}")
        print(f"Screenshots saved: {alert_stats['alerts_dir']}")
        print(f"Logs saved: {alert_stats['logs_dir']}")
        print(f"{'='*60}\n")
        print("[INFO] SentinelEdge system shutdown complete\n")


if __name__ == "__main__":
    main()
