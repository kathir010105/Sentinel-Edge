"""
SentinelEdge - Person Detection Module
Uses YOLOv8 for local person detection on edge device.
Edge Computing: AI inference runs locally on GPU without cloud dependency.
"""

import cv2
import torch
from ultralytics import YOLO
from datetime import datetime
import os


class PersonDetector:
    """Handles person detection using YOLOv8 model on edge device."""
    
    def __init__(self, model_name='yolov8n.pt', confidence_threshold=0.5):
        """
        Initialize person detector with YOLOv8.
        
        Args:
            model_name (str): YOLOv8 model variant (yolov8n.pt for nano - fastest)
            confidence_threshold (float): Minimum confidence for detection (0-1)
        """
        self.model_name = model_name
        self.confidence_threshold = confidence_threshold
        self.model = None
        self.device = None
        
        # COCO class ID for 'person' is 0
        self.person_class_id = 0
        
    def load_model(self):
        """
        Load YOLOv8 model and configure for edge inference.
        Model auto-downloads if not present.
        """
        print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Loading YOLOv8 model: {self.model_name}")
        
        # Check GPU availability
        if torch.cuda.is_available():
            self.device = 'cuda'
            gpu_name = torch.cuda.get_device_name(0)
            print(f"[INFO] GPU detected: {gpu_name}")
            print(f"[INFO] CUDA version: {torch.version.cuda}")
        else:
            self.device = 'cpu'
            print("[WARNING] No GPU detected, using CPU (slower)")
        
        # Load YOLOv8 model (auto-downloads if needed)
        print(f"[INFO] Loading model to {self.device.upper()}...")
        self.model = YOLO(self.model_name)
        
        # Move model to device
        self.model.to(self.device)
        
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Model loaded successfully")
        print(f"[INFO] Confidence threshold: {self.confidence_threshold}")
        print(f"[INFO] Target class: Person (ID: {self.person_class_id})")
        
        return True
    
    def detect_persons(self, frame):
        """
        Detect persons in a frame using YOLOv8.
        
        Args:
            frame (numpy.ndarray): Input image frame
            
        Returns:
            tuple: (annotated_frame, person_count, detections_list)
        """
        if self.model is None:
            print("[ERROR] Model not loaded. Call load_model() first.")
            return frame, 0, []
        
        # Run inference
        results = self.model(frame, verbose=False, device=self.device)
        
        # Extract detections
        detections = []
        person_count = 0
        
        for result in results:
            boxes = result.boxes
            
            for box in boxes:
                # Get class ID and confidence
                class_id = int(box.cls[0])
                confidence = float(box.conf[0])
                
                # Filter for person class only
                if class_id == self.person_class_id and confidence >= self.confidence_threshold:
                    # Get bounding box coordinates
                    x1, y1, x2, y2 = box.xyxy[0]
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                    
                    detections.append({
                        'bbox': (x1, y1, x2, y2),
                        'confidence': confidence,
                        'class': 'person'
                    })
                    person_count += 1
        
        # Annotate frame with detections
        annotated_frame = self._draw_detections(frame.copy(), detections)
        
        return annotated_frame, person_count, detections
    
    def _draw_detections(self, frame, detections):
        """
        Draw bounding boxes and labels on frame.
        
        Args:
            frame (numpy.ndarray): Input frame
            detections (list): List of detection dictionaries
            
        Returns:
            numpy.ndarray: Annotated frame
        """
        for detection in detections:
            x1, y1, x2, y2 = detection['bbox']
            confidence = detection['confidence']
            
            # Draw bounding box (red for person detection)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
            
            # Prepare label
            label = f"Person: {confidence:.2f}"
            
            # Get label size for background
            (label_width, label_height), baseline = cv2.getTextSize(
                label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1
            )
            
            # Draw label background
            cv2.rectangle(
                frame,
                (x1, y1 - label_height - baseline - 5),
                (x1 + label_width, y1),
                (0, 0, 255),
                -1
            )
            
            # Draw label text
            cv2.putText(
                frame,
                label,
                (x1, y1 - baseline - 5),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (255, 255, 255),
                1
            )
        
        return frame
    
    def get_device_info(self):
        """Get information about the inference device."""
        return {
            'device': self.device,
            'model': self.model_name,
            'confidence_threshold': self.confidence_threshold,
            'cuda_available': torch.cuda.is_available(),
            'gpu_name': torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'N/A'
        }


def main():
    """Test person detection with live camera feed."""
    print("\n" + "="*60)
    print("SENTINEDGE - PERSON DETECTION TEST")
    print("="*60)
    print("Testing YOLOv8 person detection on edge device")
    print("="*60 + "\n")
    
    # Import camera feed module
    from camera_feed import CameraFeed
    
    # Initialize detector
    detector = PersonDetector(model_name='yolov8n.pt', confidence_threshold=0.5)
    
    # Load model (will download if not present)
    if not detector.load_model():
        print("[ERROR] Failed to load model")
        return
    
    # Display device info
    info = detector.get_device_info()
    print(f"\n[DEVICE INFO]")
    print(f"  Device: {info['device'].upper()}")
    print(f"  GPU: {info['gpu_name']}")
    print(f"  Model: {info['model']}")
    print(f"  Confidence: {info['confidence_threshold']}")
    
    # Initialize camera
    camera = CameraFeed(camera_id=0)
    if not camera.start():
        print("[ERROR] Failed to start camera")
        return
    
    print("\n" + "="*60)
    print("LIVE PERSON DETECTION ACTIVE")
    print("="*60)
    print("[INFO] Detection is running on your edge device")
    print("[CONTROLS] Press 'q' or ESC to exit")
    print("="*60 + "\n")
    
    frame_count = 0
    detection_count = 0
    
    try:
        while camera.is_running:
            ret, frame = camera.get_frame()
            
            if not ret:
                print("[WARNING] Failed to grab frame")
                break
            
            frame_count += 1
            
            # Run person detection
            annotated_frame, person_count, detections = detector.detect_persons(frame)
            
            if person_count > 0:
                detection_count += 1
            
            # Add status overlay
            status_color = (0, 0, 255) if person_count > 0 else (0, 255, 0)
            status_text = f"PERSONS DETECTED: {person_count}" if person_count > 0 else "NO PERSONS"
            
            cv2.putText(
                annotated_frame,
                "SentinelEdge - Person Detection",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2
            )
            
            cv2.putText(
                annotated_frame,
                status_text,
                (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                status_color,
                2
            )
            
            cv2.putText(
                annotated_frame,
                f"Frame: {frame_count} | Device: {info['device'].upper()}",
                (10, 90),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0),
                1
            )
            
            cv2.putText(
                annotated_frame,
                "Press 'q' or ESC to exit",
                (10, annotated_frame.shape[0] - 20),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 255),
                1
            )
            
            # Display annotated frame
            cv2.imshow('SentinelEdge - Person Detection', annotated_frame)
            
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
        
        print(f"\n[STATISTICS]")
        print(f"  Total frames: {frame_count}")
        print(f"  Frames with persons: {detection_count}")
        print(f"  Detection rate: {(detection_count/frame_count*100):.1f}%")
        print("\n[INFO] Detection system closed successfully\n")


if __name__ == "__main__":
    main()
