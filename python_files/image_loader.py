import face_recognition
import cv2
import numpy as np

def load_image(image_path: str, max_width: int = 1000):
    """
    Loads an image and resizes it if it exceeds max_width to optimize processing speed.
    """
    try:
        image = face_recognition.load_image_file(image_path)
        
        # Check if resizing is needed
        height, width = image.shape[:2]
        if width > max_width:
            ratio = max_width / width
            new_size = (max_width, int(height * ratio))
            # Resize while maintaining aspect ratio
            image = cv2.resize(image, new_size, interpolation=cv2.INTER_AREA)
            print(f"[INFO] Image resized from {width}x{height} to {new_size[0]}x{new_size[1]}")
            
        return image
    except Exception as e:
        print(f"Error loading image: {e}")
        return None
