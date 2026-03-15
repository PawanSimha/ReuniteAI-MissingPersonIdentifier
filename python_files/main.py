# ReuniteAI - Missing Person Identification System
# Copyright (C) 2026 Pawan Simha
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
ReuniteAI - Main Execution File
Orchestrates face matching workflow
"""

# -------------------- MODULE IMPORTS --------------------
from python_files.image_loader import load_image
from python_files.face_encoder import extract_face_encoding
from python_files.matcher import find_best_match
from python_files.storage_manager import ensure_directories
from python_files.db_manager import fetch_person_details, get_all_face_encodings, update_case_status

# -------------------- STANDARD IMPORTS ------------------
import os

# -------------------------------------------------------
# Main Pipeline
# -------------------------------------------------------

def run_matching_pipeline(uploaded_image_path):
    """
    Main matching pipeline that processes uploaded image and compares with database.
    
    Args:
        uploaded_image_path (str): Path to the uploaded image file
    
    Returns:
        dict: Result dictionary with status, similarity, and person details if matched
    """
    ensure_directories()

    # Load and process uploaded image
    image = load_image(uploaded_image_path)
    if image is None:
        return {
            "status": "error",
            "message": "Failed to load image"
        }

    uploaded_encoding = extract_face_encoding(image)
    if uploaded_encoding is None:
        return {
            "status": "error",
            "message": "No face detected in uploaded image"
        }

    # Load all face encodings from MongoDB
    database_encodings = get_all_face_encodings()

    if not database_encodings:
        return {
            "status": "no_match",
            "similarity": 0,
            "image_path": uploaded_image_path,
            "message": "No records in database"
        }

    # Find best match
    result = find_best_match(uploaded_encoding, database_encodings)

    if result["match"]:
        person = fetch_person_details(result["person_id"])
        
        # Update case status to matched
        if person:
            update_case_status(result["person_id"], "matched")

        return {
            "status": "match",
            "person": person,
            "similarity": result["similarity"],
            "image_path": uploaded_image_path
        }

    return {
        "status": "no_match",
        "similarity": result["similarity"],
        "image_path": uploaded_image_path,
        "message": "No match found above threshold"
    }



# -------------------------------------------------------
# Entry Point (CLI TEST ONLY)
# -------------------------------------------------------

if __name__ == "__main__":
    output = run_matching_pipeline()
    print(output)
