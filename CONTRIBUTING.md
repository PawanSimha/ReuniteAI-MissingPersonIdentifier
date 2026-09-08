# Contributing to ReuniteAI

Thanks for your interest in contributing. These guidelines keep the project reviewable, testable, and professional.

## Development flow

1. **Fork** the [repository](https://github.com/PawanSimha/ReuniteAI-MissingPersonIdentifier) and clone it:

   ```bash
   git clone git@github.com:<you>/ReuniteAI-MissingPersonIdentifier.git
   cd ReuniteAI-MissingPersonIdentifier
   ```

2. Create a feature branch:

   ```bash
   git checkout -b feat/your-feature
   ```

   Branch naming: `feat/…`, `fix/…`, `docs/…`, `chore/…`, `build/…`, `test/…`.

3. Make your changes. Keep them **small and focused** on one concern.
4. Run the test suite locally (needs a reachable MongoDB):

   ```bash
   docker compose up -d db        # container MongoDB (or start your local service)
   python -m unittest discover tests -v
   ```

   Tests import the Flask app, which connects to MongoDB at startup — a reachable database is required.
5. Verify the container stack still builds and validates:

   ```bash
   docker compose config --quiet
   docker compose up -d --build
   ```

6. Commit with **[Conventional Commits](https://www.conventionalcommits.org/)**:

   ```text
   feat(api): add token-gated public search endpoint
   fix(docker): pin bcrypt to 4.0.1 for passlib compat
   docs(readme): document PORT environment variable
   ```

7. Push and open a **Pull Request** against `main`.

## What to include in a PR

- A clear title and description of *what* and *why*.
- Tests for new behavior (existing suites must keep passing).
- Updated `CHANGELOG.md` entry under **Unreleased** when behavior changes.
- No environment files (`.env*` stay gitignored — only `.env.example` is tracked).

## CI

Pull requests automatically run **`ci.yml`** (unit tests against a fresh MongoDB container + `docker compose config` validation). The **`docker.yml`** workflow builds and publishes the GHCR image with a Trivy vulnerability scan on changes to `main`. GitHub Actions must pass for merge.

## Reporting issues

Include: reproduction steps, expected vs. actual behavior, screenshots if visual, and the `docker compose ps` output / error logs when the bug is container-related.