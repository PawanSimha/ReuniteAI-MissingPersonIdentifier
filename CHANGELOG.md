# Changelog

All notable changes to **ReuniteAI** are documented in this file.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project uses [Semantic Versioning](https://semver.org/).

## [Unreleased]

- Public REST API (token-gated) for third-party agency integration.
- SMS / Email alert notifications to guardians upon match detection.
- Geo-tagging & interactive maps for missing-person locations.
- Mobile companion app (React Native / Flutter).

## [1.0.0] — 2026

### Added
- **Containerization**: multi-stage `Dockerfile` (dlib compiled in a builder stage, slim non-root runtime as `appuser`), `docker-compose.yml` orchestration (`web` + `db` on MongoDB 7) with healthchecks and persistent volumes, and `.dockerignore`.
- **CI/CD**: GitHub Actions workflows — `ci.yml` (unit tests against a MongoDB service container + compose validation) and `docker.yml` (BuildKit build → GHCR publish with `latest`/`sha-`/semver tags → Trivy vulnerability scan with SARIF upload to GitHub Advanced Security).
- **Liveness probe**: `GET /health` endpoint (HTTP 200 = app + DB healthy, 503 otherwise) backing the Docker `HEALTHCHECK`.
- **UI redesign**: split-panel auth page, floating "glass pill" navbar with drop-shadow, plain (non-tiled) logo, and global scale tuning for desktop display.
- **Project hygiene**: `.gitattributes` (line-ending normalization), `.editorconfig`, `CONTRIBUTING.md`, and this changelog.

### Fixed
- `dlib`/`face_recognition` installs: `--no-build-isolation` with apt-provided CMake (avoids pip-fetched CMake ≥ 3.31 policy failure) plus pip retry/timeout flags for large sdist downloads.
- Prefixed `--prefix` installs of pip site-packages resolved via `PYTHONPATH` so runtime scripts resolve correctly inside the container.
- Dependency pin for `bcrypt==4.0.1` to keep `passlib 1.7.4` compatible (bcrypt ≥ 4.1 breaks it).
- Signup UI test assertions updated for the redesigned auth page.

### Changed
- Server binds `0.0.0.0` and honors the `PORT` environment variable (default `5000`; `8000` in containers). Dev server is now reachable across the local network.
- `README.md` gains Docker quickstart, CI/CD documentation, and status badges; `PRD.md` reflects the v1.0.0 implementation status and containerization constraints.
- `sitemap.xml` and `robots.txt` repointed to the GitHub Pages marketing site.

---

## Template reference (older history)

Pre-1.0 development history was not kept under semantic versioning; see `git log` for the full commit history.

[Unreleased]: https://github.com/PawanSimha/ReuniteAI-MissingPersonIdentifier/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/PawanSimha/ReuniteAI-MissingPersonIdentifier/releases/tag/v1.0.0