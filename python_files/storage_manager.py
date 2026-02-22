import os
import shutil

# Get the project root directory (parent of python_files)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMP_DIR = os.path.join(BASE_DIR, "images", "temp")
DATABASE_DIR = os.path.join(BASE_DIR, "images", "database")


def ensure_directories():
    """
    Ensures required directories exist.
    """
    os.makedirs(TEMP_DIR, exist_ok=True)
    os.makedirs(DATABASE_DIR, exist_ok=True)


def move_to_database(image_path, new_name=None):
    """
    Moves an image from temp folder to database folder.

    Args:
        image_path (str): Path to temp image (can be absolute or relative)
        new_name (str): Optional new filename

    Returns:
        str: New image path in database (relative path from project root)
    """
    ensure_directories()

    # Handle both absolute and relative paths
    if not os.path.isabs(image_path):
        image_path = os.path.join(BASE_DIR, image_path)

    filename = new_name if new_name else os.path.basename(image_path)
    destination = os.path.join(DATABASE_DIR, filename)

    shutil.move(image_path, destination)
    
    # Return relative path for database storage
    return os.path.join("images", "database", filename)
