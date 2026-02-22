# ReuniteAI Walkthrough Guide

This guide will help you navigate and use the core features of the ReuniteAI platform.

## 1. Getting Started

### Prerequisites
Ensure you have Python 3.8+ and MongoDB installed.

### Installation
1.  Clone the repository.
2.  Create virtual environment: `python -m venv venv`.
3.  Activate it: `venv\Scripts\activate`.
4.  Install dependencies: `pip install -r requirements.txt`.
5.  Start MongoDB: `mongod`.

### Running the App
Run `python app.py`. The app will be available at `http://127.0.0.1:5000`.

## 2. Default Login
The system comes with a pre-configured Admin account:
- **Email**: `pawansimha@gmail.com`
- **Password**: `[REDACTED]`


## 3. User Flows

### A. Registering a New Account
1.  Go to the Homepage.
2.  Click **"Sign Up"** (or toggle to "New Here?").
3.  Fill in your details (Name, Email, Password).
4.  Click **"Sign Up"**.
5.  You can now log in with your new credentials.

### B. Reporting a Missing Person
1.  Log in as a User.
2.  Click **"Report a Case"** on the dashboard.
3.  Fill in the missing person's details:
    -   Name, Guardian Name, Contact Info
    -   Last seen location & date
4.  **Upload a clear photo** of the missing person.
5.  Submit the form. The system will index the face for future searches.

### C. Searching for a Missing Person (Verification)
1.  Log in as a User.
2.  Click **"Verify a Person"** or **"Upload Image"**.
3.  Upload a photo of the person you have found or want to check.
4.  The system will process the image and compare it against the database.
5.  **Result**:
    -   **Match Found**: You will see the person's details and contact info.
    -   **No Match**: You will be prompted to report them if necessary.

### D. Admin Dashboard
1.  Log in as Admin (`pawansimha@gmail.com`).
2.  The Dashboard shows:
    -   Total Registered Users
    -   Total Missing Persons
    -   Matched Cases
3.  Use the sidebar or cards to:
    -   **View Users**: Manage registered accounts.
    -   **View Missing**: See the full database of missing persons.
