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

from flask import Flask, render_template, request, redirect, url_for, session, flash, send_from_directory
from flask_wtf.csrf import CSRFProtect

import os
import uuid
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from python_files.auth_manager import signup_user, login_user, get_all_users, initialize_admin_account
from python_files.db_manager import get_all_missing_persons, insert_new_person
from python_files.main import run_matching_pipeline
from python_files.face_encoder import extract_face_encoding
from python_files.image_loader import load_image
from python_files.storage_manager import ensure_directories

app = Flask(__name__)
# Use environment variable for security, fallback to default for dev convenience
app.secret_key = os.getenv("SECRET_KEY")
if not app.secret_key:
    # In production, this should cause an immediate failure to prevent insecure defaults
    if not os.getenv("FLASK_DEBUG", "False").lower() in ("true", "1", "t"):
        raise RuntimeError("SECRET_KEY environment variable is not set!")
    else:
        # For local development only, if .env is missing
        app.secret_key = "dev_fallback_key_replace_in_production"

csrf = CSRFProtect(app)


# ---------------- UPLOAD CONFIG ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "images", "temp")
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
ensure_directories()

# Initialize admin account on startup
initialize_admin_account()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ---------------- HOME (LOGIN PAGE) ----------------
@app.route("/")
def home():
    return render_template("login.html")


# ---------------- SIGNUP ----------------
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        result = signup_user(
            request.form["first_name"],
            request.form["last_name"],
            request.form["username"],
            request.form["email"],
            request.form["password"]
        )
        
        if result["status"] == "success":
            flash("Registration successful! Please login.", "success")
            return redirect(url_for("home"))
        else:
            flash(result["message"], "error")
            return render_template("login.html")

    return render_template("login.html")


# ---------------- LOGIN ----------------
@app.route("/login", methods=["POST"])
def login():
    result = login_user(
        request.form["email"],
        request.form["password"]
    )

    if result["status"] == "success":
        session["user_email"] = result["email"]
        session["role"] = result["role"]

        if result["role"] == "admin":
            return redirect(url_for("admin_dashboard"))
        else:
            return redirect(url_for("user_home"))
    else:
        flash(result["message"], "error")
        return redirect(url_for("home"))


# ---------------- USER HOME ----------------
@app.route("/user/home")
def user_home():
    if "user_email" not in session:
        return redirect("/")

    return render_template("user_home.html")


# ---------------- ADMIN DASHBOARD ----------------
@app.route("/admin/dashboard")
def admin_dashboard():
    if session.get("role") != "admin":
        return redirect("/")

    users = get_all_users()
    persons = get_all_missing_persons()

    total_users = len(users)
    total_missing = len(persons)
    total_matched = len([p for p in persons if p.get("case_status") == "matched"])

    return render_template(
        "dashboard.html",
        total_users=total_users,
        total_missing=total_missing,
        total_matched=total_matched
    )


# ---------------- USER PROFILE ----------------
@app.route("/profile")
def profile():
    if "user_email" not in session:
        return redirect("/")

    users = get_all_users()
    # Find the current user in the list of users
    user = next((u for u in users if u.get("email") == session.get("user_email")), None)

    if not user:
        flash("User profile not found.", "error")
        return redirect(url_for("user_home"))

    return render_template("profile.html", user=user)


# ---------------- UPLOAD + MATCH (USER) ----------------
@app.route("/upload", methods=["GET", "POST"])
def upload():
    if "user_email" not in session:
        return redirect("/")

    if request.method == "POST":
        if 'image' not in request.files:
            flash("No file selected", "error")
            return render_template("upload.html")
        
        file = request.files['image']
        
        if file.filename == '':
            flash("No file selected", "error")
            return render_template("upload.html")
        
        if file and allowed_file(file.filename):
            # Generate unique filename
            filename = str(uuid.uuid4()) + '.' + secure_filename(file.filename).rsplit('.', 1)[1].lower()
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)

            # Run matching pipeline
            result = run_matching_pipeline(file_path)
            
            # Store relative path for template display (ensure no leading slash)
            if "image_path" in result:
                result["image_path"] = f"images/temp/{filename}"
            
            return render_template("result.html", result=result)
        else:
            flash("Invalid file type. Please upload JPG, PNG, or JPEG images.", "error")
            return render_template("upload.html")

    return render_template("upload.html")

# ---------------- REGISTER MISSING ----------------
@app.route("/register_missing", methods=["GET", "POST"])
def register_missing():
    if "user_email" not in session:
        return redirect("/")

    if request.method == "POST":
        image_path = request.form.get("image_path")
        
        # Handle both absolute and relative paths for backend processing
        if image_path:
            # Normalize slashes first
            image_path = image_path.replace("/", os.sep).replace("\\", os.sep)
            
            # If relative, join with BASE_DIR
            if not os.path.isabs(image_path):
                # If it starts with images/, ensure we join correctly
                # On Windows if images_dir is C:\...\images and path is images\temp...
                # we don't want C:\...\images\images\...
                # Actually BASE_DIR is project root, so joining with images/... is fine.
                image_path = os.path.join(BASE_DIR, image_path)
        
        if not image_path or not os.path.exists(image_path):
            flash("Image file not found", "error")
            return redirect(url_for("upload"))

        person_id = str(uuid.uuid4())

        # Extract face encoding from image
        image = load_image(image_path)
        face_encoding = None
        if image is not None:
            face_encoding = extract_face_encoding(image)

        # Move image to database folder
        from python_files.storage_manager import move_to_database
        new_image_path = move_to_database(image_path, f"{person_id}.jpg")

        person_details = {
            "full_name": request.form["full_name"],
            "guardian_name": request.form["guardian_name"],
            "phone": request.form["phone"],
            "email": request.form.get("email", ""),
            "home_address": request.form["home_address"],
            "missing_location": request.form["missing_location"],
            "missing_date": request.form["missing_date"]
        }

        insert_new_person(
            person_id=person_id,
            face_encoding=face_encoding,
            image_path=new_image_path,
            person_details=person_details
        )

        flash("Missing person registered successfully!", "success")
        return redirect(url_for("user_home"))

    image_path = request.args.get("image_path")
    if not image_path:
        flash("No image provided", "error")
        return redirect(url_for("upload"))
    
    # Standardize image_path for URLs: no leading slash, forward slashes
    # If it was absolute, make it relative to images/
    clean_path = image_path.replace("\\", "/")
    if "images/" in clean_path:
        clean_path = clean_path.split("images/")[1]
        clean_path = "images/" + clean_path
    
    # Ensure NO leading slash for template consistency (template adds it)
    if clean_path.startswith("/"):
        clean_path = clean_path[1:]
    
    return render_template(
        "register_missing.html",
        image_path=clean_path
    )

# ---------------- VIEW MISSING PERSONS (ADMIN) ----------------
@app.route("/missing")
def missing():
    if session.get("role") != "admin":
        return redirect("/")

    persons = get_all_missing_persons()
    return render_template("missing.html", persons=persons)


# ---------------- VIEW USERS (ADMIN ONLY) -------------------
@app.route("/users")
def users():
    if session.get("role") != "admin":
        return redirect("/")

    users = get_all_users()
    return render_template("users.html", users=users)


# ---------------- CONTACT ----------------
@app.route("/contact")
def contact():
    return render_template("contact.html")


# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# ---------------- SERVE IMAGES ----------------
@app.route('/images/<path:filename>')
def serve_image(filename):
    """Serve images from the images directory"""
    images_dir = os.path.join(BASE_DIR, 'images')
    # Use os-specific separators for the filename to be safe
    safe_filename = filename.replace('/', os.sep).replace('\\', os.sep)
    return send_from_directory(images_dir, safe_filename)

# ---------------- 404 PAGE ROUTE ----------------
@app.route("/404")
def view_404():
    return render_template("404.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


# ---------------- START SERVER ----------------
if __name__ == "__main__":
    debug_mode = os.getenv("FLASK_DEBUG", "False").lower() in ("true", "1", "t")
    app.run(debug=debug_mode)

# ---------------- 404 ERROR ----------------
