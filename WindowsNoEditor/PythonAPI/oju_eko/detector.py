from ultralytics import YOLO
import cv2
import os

class OjuEkoDetector:
    def __init__(self, model_path='yolov8n.pt'):
        """
        Initialize the Oju-Eko Perception Model.
        Defaulting to YOLOv8 Nano for real-time performance on lower-end hardware.
        """
        print(f"Loading model: {model_path}...")
        self.model = YOLO(model_path)
        
        # Phase 1 Target Classes (Baseline mapping for demo)
        # In the final version, these will be replaced by our custom trained weights
        self.custom_classes = {
            'Danfo': 'bus',
            'Okada': 'motorcycle',
            'Keke': 'auto_rickshaw', # Note: standard YOLO doesn't have this, we use 'motorcycle' or 'car' as placeholder
            'Pothole': 'stop sign', # Placeholder for demo
            'Pedestrian': 'person'
        }

    def detect(self, frame):
        """
        Run inference on a single frame.
        """
        results = self.model(frame, verbose=False)
        return results

    def visualize(self, frame, results):
        """
        Overlay bounding boxes and labels on the frame.
        """
        annotated_frame = results[0].plot()
        return annotated_frame

def main():
    # Setup for a quick test
    detector = OjuEkoDetector()
    
    # Check if we have a test image
    test_img_path = 'test_frame.jpg'
    if not os.path.exists(test_img_path):
        print("No test image found. Creating a blank test...")
        import numpy as np
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        cv2.putText(frame, "Waiting for Lagos-v1 data...", (100, 240), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    else:
        frame = cv2.imread(test_img_path)

    results = detector.detect(frame)
    annotated = detector.visualize(frame, results)
    
    cv2.imwrite('detection_output.jpg', annotated)
    print("Detection complete. Output saved to detection_output.jpg")

if __name__ == '__main__':
    main()
