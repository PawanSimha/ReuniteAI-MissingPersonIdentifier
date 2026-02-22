"""
Face Encoder Module
Extracts face embeddings using face_recognition
"""

import face_recognition
import numpy as np


def extract_face_encoding(image):
    """
    Extracts face encoding from a loaded image.

    Args:
        image (numpy array): Loaded image

    Returns:
        numpy.ndarray | None
    """
    try:
        # Detect face locations
        face_locations = face_recognition.face_locations(image)

        if not face_locations:
            return None

        # Extract encodings
        encodings = face_recognition.face_encodings(image, face_locations)

        if not encodings:
            return None

        return np.array(encodings[0])

    except Exception as e:
        print("Face encoding error:", e)
        return None
