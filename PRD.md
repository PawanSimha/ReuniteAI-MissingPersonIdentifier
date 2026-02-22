# Product Requirements Document (PRD)

# ReuniteAI: Missing Person Identification System

## 1. Executive Summary
**ReuniteAI** is a web-based platform designed to assist in finding missing persons using facial recognition technology. It serves as a centralized database where users can report missing persons and verify if an individual matches existing records using AI-powered image matching.

## 2. Problem Statement
Thousands of people go missing every year. Traditional methods of finding them (posters, police reports) are manual and slow. There is a need for a scalable, automated system that can quickly compare photos of found individuals against a database of missing persons to find potential matches.

## 3. Goals & Objectives
- **Automate Identification**: Use facial recognition to instantly match uploaded photos with missing person records.
- **Centralized Database**: Maintain a secure, searchable database of missing persons.
- **Accessibility**: Provide an easy-to-use web interface for both public users and administrators.
- **Privacy & Security**: Ensure data is stored securely and access is controlled via role-based authentication.

## 4. Target Audience
- **General Public**: People looking for missing family members or reporting someone they found.
- **NGOs / Volunteers**: Organizations dedicated to finding missing people.
- **Law Enforcement (Future)**: Authorities who need a tool to quick-scan databases.
- **Administrators**: System managers who verify and manage records.

## 5. Core Features

### 5.1 User Features
- **User Authentication**: Sign up and login (encrypted passwords).
- **Report Missing Person**: Form to submit details (Name, Age, Location, Photo).
- **Verify/Search**: Upload a photo of a person to check if they are reported missing.
- **View Results**: See similarity match percentage and contact details if a match is found.
- **Profile Management**: Manage own account details.

### 5.2 Admin Features
- **Dashboard**: High-level stats (Total Missing, Found, Active Cases).
- **User Management**: List and manage registered users.
- **Database Management**: View and edit all missing person records.
- **System Testing**: Ability to run test matches.

## 6. Technical Architecture

### 6.1 Tech Stack
- **Frontend**: HTML5, CSS3 (Modern UI), JavaScript.
- **Backend**: Python (Flask).
- **AI/ML**: `face_recognition` library (dlib), OpenCV.
- **Database**: MongoDB (NoSQL) for flexibility with JSON-like documents.
- **Storage**: Local filesystem for images (mapped to DB records).

### 6.2 Data Flow
1. **Image Upload**: User uploads an image via the web UI.
2. **Preprocessing**: Image is loaded and faces are detected using HOG/CNN.
3. **Encoding**: The face is converted into a 128-d vector embedding.
4. **Matching**: The embedding is compared (Euclidean distance) against all stored embeddings in MongoDB.
5. **Result**: If distance < threshold (0.6), a match is returned with the person's details.

## 7. User Flows

### 7.1 Reporting a Missing Person
1. User logs in.
2. Navigates to "Report Missing".
3. Fills in details and uploads a clear photo.
4. System computes face encoding and saves record to MongoDB.
5. Confirmation message displayed.

### 7.2 Searching/Verifying a Person
1. User logs in (or accesses public search if enabled).
2. Navigates to "Upload Image".
3. Uploads a photo of the person found.
4. System processes image and runs matching algorithm.
5. **Match Found**: Displays "MATCH FOUND" with details.
6. **No Match**: Displays "No Match Found" and suggests reporting.

## 8. Future Roadmap
- [ ] **Mobile App**: Native Android/iOS app for field use.
- [ ] **Geo-Tagging**: Map integration to show where people went missing.
- [ ] **Notification System**: Email/SMS alerts when a match is found.
- [ ] **Multi-Face Detection**: Handle group photos.
- [ ] **API Access**: Public API for other agencies to connect.

## 9. Success Metrics
- **Accuracy**: >95% match rate on clear images.
- **Speed**: Match results in <2 seconds.
- **User Adoption**: Number of registered users and active cases reported.
