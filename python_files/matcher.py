from python_files.similarity import calculate_distance_batch, distance_to_similarity
import numpy as np

# Similarity threshold in percentage
MATCH_THRESHOLD = 60.0


def find_best_match(upload_encoding, database_encodings):
    """
    Compares uploaded face encoding with database encodings using NumPy vectorization.

    Args:
        upload_encoding (np.ndarray): The query encoding
        database_encodings (dict): { "person_id": np.ndarray }

    Returns:
        dict: Best match results
    """
    if not database_encodings:
        return {"match": False, "person_id": None, "similarity": 0.0}

    person_ids = list(database_encodings.keys())
    encodings_matrix = np.array(list(database_encodings.values()))

    # Calculate distances for the entire batch at once (NumPy C-speed)
    distances = calculate_distance_batch(upload_encoding, encodings_matrix)
    
    # Find index of the minimum distance
    min_idx = np.argmin(distances)
    best_distance = distances[min_idx]
    best_match_id = person_ids[min_idx]
    best_similarity = distance_to_similarity(best_distance)

    print(f"[BEST MATCH] {best_match_id} | Similarity: {best_similarity:.2f}% | Distance: {best_distance:.4f}")

    if best_similarity >= MATCH_THRESHOLD:
        return {
            "match": True,
            "person_id": best_match_id,
            "similarity": round(best_similarity, 2)
        }

    return {
        "match": False,
        "person_id": None,
        "similarity": round(best_similarity, 2)
    }
