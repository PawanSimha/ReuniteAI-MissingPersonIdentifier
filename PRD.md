# Product Requirements Document: ReuniteAI

| Field | Detail |
|-------|--------|
| **Project Name** | ReuniteAI — AI-Powered Missing Person Identification |
| **Target Release** | Q3 2025 |
| **Status** | In Review |
| **Author** | Pawan Simha R |

---

## Executive Summary

ReuniteAI is a biometric-driven web platform that enables anyone to upload a photo of an unidentified person and receive an instant AI-powered match against a growing database of missing-person records. We are building this *now* because existing search methods — physical posters, manual case-file reviews, fragmented police databases — are too slow and lack cross-agency scalability, leaving thousands of families without closure.

---

## Problem Statement

Every year, **thousands of individuals go missing**. Traditional identification methods rely on manual poster distribution, siloed police records, and slow cross-referencing across jurisdictions. There is no centralized, low-friction system where both the public and authorities can instantly cross-check a found person's photo against all active missing-person cases. This delay directly reduces the probability of successful reunification.

---

## Target Personas

| Persona | Goal | Primary Friction |
|---------|------|-----------------|
| **Family Member / Guardian** | Report a missing relative and get notified if a match is found | No centralized system to upload and track a missing person across agencies |
| **NGO / Volunteer Worker** | Quickly verify if a found individual matches any open case | Manual, slow comparison of photos against multiple disconnected databases |
| **System Administrator** | Manage users, monitor platform health, and audit match records | No dashboard-level visibility into system usage, match rates, or data integrity |

---

## Success Metrics (OKRs / KPIs)

| Metric | Target | Measurement Method |
|--------|--------|-------------------|
| **Match Accuracy** | >95% precision on clear frontal-face images | Holdout test set of labeled missing-person photos |
| **Match Latency** | <2 seconds per upload (encoding + batch search) | Server-side timing instrumentation |
| **Case Resolution Rate** | 30% of reported missing persons matched within 90 days | Database case-status audit (`active` → `matched`) |
| **User Onboarding** | 1,000+ registered users within 6 months of GA | MongoDB user collection count |
| **System Uptime** | 99.5% availability | Flask health-check endpoint / uptime monitoring |

---

## Core Features & Requirements (MoSCoW Method)

### P0 — Must Have (V1 Critical)

| Feature | Description | Acceptance Criteria |
|---------|-------------|-------------------|
| **Secure Authentication** | bcrypt-hashed signup/login with session management | User can register, log in, and maintain a persistent session |
| **Report Missing Person** | Form to submit name, age, location, and photo of a missing person | Record stored in MongoDB with a 128-d face encoding attached |
| **AI Photo Search** | Upload a found person's photo; system detects face, encodes it, and runs Euclidean-distance batch matching | Results returned in <2 seconds; matches sorted by similarity score |
| **Match Results View** | Display matched person's name, guardian contact, location, and date reported | Confidence score shown; user can initiate contact from the UI |
| **Admin Dashboard** | Aggregate stats: total users, total missing cases, matched cases, recent activity | Real-time counts; case status toggle (`active` → `matched`) |

### P1 — Should Have (V1.1)

| Feature | Description |
|---------|-------------|
| **User Profile Management** | Self-service update of name, email, password |
| **Admin User Management** | List, filter, and disable registered user accounts |
| **CSRF Protection** | Flask-WTF token validation on all POST endpoints |
| **Image Validation** | Reject uploads with no detectable face; prompt user to retry |

### P2 — Could Have (Future)

| Feature | Description |
|---------|-------------|
| **Mobile Companion App** | React Native or Flutter client for field operatives |
| **Geo-Tagging & Maps** | Leaflet/Mapbox visualization of missing-person locations |
| **SMS / Email Alerts** | Automated notification to guardians upon match detection |
| **Public REST API** | Token-gated endpoints for third-party agency integration |
| **Multi-Face Detection** | Handle group photos — match each detected face independently |

---

## AI & Technical Constraints

| Constraint | Specification |
|------------|--------------|
| **Face Detection** | HOG + CNN cascade via `face_recognition` (dlib). Minimum face size: 80×80 pixels |
| **Face Encoding** | Deep Residual Network → 128-d float vector. Must produce consistent encodings (±0.02 variance) across lighting conditions |
| **Matching Algorithm** | NumPy-vectorized Euclidean distance. Threshold: **<0.6** for a positive match |
| **Latency Budget** | Full pipeline (load → detect → encode → match) must complete in **<2,000 ms** for a single query against 10,000 stored encodings |
| **Data Security** | Passwords hashed with **bcrypt** (rounds=12). Sessions signed with `SECRET_KEY` via Flask. No plaintext credentials stored |
| **Database** | MongoDB 4.4+ (`pymongo`). Face encodings stored as BSON arrays. Index on `face_encoding` for batch scan efficiency |
| **Image Storage** | Local filesystem partitioned into `images/temp/` (staging) and `images/database/` (permanent). Max upload size: **16 MB** |

---

## User Journey / Flow

### Primary Flow: Upload & Match

1. User navigates to `/login` and authenticates (or signs up at `/signup`).
2. After login, user lands on `/user/home` with options to **Report Missing** or **Upload for Search**.
3. User selects **Upload for Search** → `/upload` page loads with a file picker and submit button.
4. User selects a clear frontal-face photo and submits.
5. Backend pipeline executes:
   - `image_loader.py` loads and resizes the image.
   - `face_encoder.py` extracts the 128-d embedding.
   - `matcher.py` computes Euclidean distance against all stored embeddings.
   - `similarity.py` converts distances to a 0–100% similarity score.
6. If any match exceeds the **0.6 threshold**, the top results (name, guardian, contact, location, date) are rendered on `/result`.
7. If no match meets the threshold, a **"No Match Found"** message is displayed with a prompt to register the person as missing.

---

## Out of Scope (Non-Goals)

- **Real-time video surveillance or CCTV integration** — V1 is photo-upload only.
- **Mobile-native apps** — V1 is a responsive web interface only; native clients are P2.
- **Cross-modal search (text-to-image, voice)** — Matching is purely visual (face encoding).
- **Automated case resolution or law-enforcement notifications** — Matching confirms identity only; reunification logistics remain manual.
- **Multi-language support** — V1 English only.
- **Federated database sharing across independent ReuniteAI instances** — Each deployment operates on its own MongoDB.

---

## Go-To-Market (GTM) / Rollout Strategy

| Phase | Activities | Success Criteria |
|-------|------------|-----------------|
| **Alpha (Weeks 1–2)** | Internal testing with synthetic data. Validate pipeline latency and encoding accuracy against a labeled test set | Match latency <2s; precision >95% on test set |
| **Beta (Weeks 3–6)** | Onboard 3–5 NGOs / volunteer groups. Collect real-world uploads and match feedback. Tune distance threshold if needed | 50+ missing-person records; 10+ successful match confirmations |
| **GA (Week 7+)** | Public launch. Deploy to production environment. Publish on GitHub and social channels. Monitor dashboard metrics | 1,000 registered users; 30% case-resolution rate within 90 days of GA |
