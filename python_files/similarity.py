import numpy as np

def calculate_distance(encoding1, encoding2):
    """
    Calculates Euclidean distance between two face encodings.
    """
    return np.linalg.norm(np.array(encoding1) - np.array(encoding2))


def calculate_distance_batch(upload_encoding, database_encodings):
    """
    Calculates Euclidean distances between one encoding and a batch of encodings.
    
    Args:
        upload_encoding (ndarray): The encoding to compare
        database_encodings (ndarray): Matrix of shape (N, 128)
        
    Returns:
        ndarray: Vector of distances of shape (N,)
    """
    return np.linalg.norm(database_encodings - upload_encoding, axis=1)


def distance_to_similarity(distance, max_distance=1.0):
    """
    Converts face distance into similarity percentage.

    Args:
        distance (float): Face distance
        max_distance (float): Maximum possible distance

    Returns:
        float: Similarity percentage (0–100)
    """
    similarity = max(0.0, (1 - distance / max_distance) * 100)
    return round(similarity, 2)
