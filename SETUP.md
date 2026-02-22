# Quick Setup Guide

## Prerequisites Check
- [ ] Python 3.8+ installed
- [ ] MongoDB installed and running
- [ ] pip installed

## Step-by-Step Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

**Note**: If `face_recognition` installation fails:
- **Windows**: Usually works automatically
- **Linux**: Install cmake first: `sudo apt-get install cmake`
- **Mac**: `brew install cmake`

### 2. Start MongoDB
```bash
# Windows (if installed as service, starts automatically)
# Or run manually:
mongod

# Linux
sudo systemctl start mongod
# Or
mongod

# Mac
mongod
```

### 3. Run the Application
```bash
python app.py
```

### 4. Access the Application
Open your browser and go to: `http://localhost:5000`

### 5. Login Credentials

**Admin Account** (automatically created):
- Email: `pawansimha@gmail.com`
- Password: `[REFER TO .env]` (Initialized on first run)


**Normal User**: Register a new account through the signup page

## Testing the System

1. **As Admin**:
   - Login with admin credentials
   - View dashboard statistics
   - Upload test images
   - View all users and missing persons

2. **As Normal User**:
   - Register and login
   - Upload an image to check for matches
   - Report a missing person if no match found

## Directory Structure
The application will automatically create:
- `images/temp/` - Temporary uploads
- `images/database/` - Stored missing person images

## Troubleshooting

**MongoDB Connection Error**:
- Check if MongoDB is running: `mongod --version`
- Verify connection string in `python_files/db_manager.py`

**Face Recognition Issues**:
- Ensure images contain clear, front-facing faces
- Try images with good lighting
- Check that face_recognition library installed correctly

**Image Upload Errors**:
- Check file permissions on `images/` directory
- Verify file format (JPG, PNG, JPEG only)
- Ensure sufficient disk space

## Next Steps

1. Add missing person records to the database
2. Test face recognition with various images
3. Customize settings in `python_files/matcher.py` (similarity threshold)
4. Review and adjust security settings as needed

