# Talent Technical Evaluation

Comprehensive full‑stack ai-powered sample application for creating, managing, and evaluating hiring assessments. This repository contains a Python FastAPI backend and a TypeScript React frontend built with Vite and React Router. The project demonstrates common hiring workflows including job posting, assessment creation, candidate application, and AI-assisted scoring.

## Features

- User authentication and role-based flows (candidates, HR).
- Job posting and management.
- Assessments attached to jobs with rich question types.
- Candidate application submission and progress tracking.
- AI-powered scoring and rationalization.
- Admin dashboard with overview charts and pagination.

## Technology stack

- Backend: Python, FastAPI, Pydantic, SQLAlchemy, Alembic, Uvicorn.
- Frontend: React (TypeScript), React Router, Vite, TailwindCSS.
- API client: Axios, React Query.
- Database: SQLite (default; configurable via `DATABASE_URL`).
- Dev & tooling: pytest, Pre-commit, ESLint/TypeScript (frontend).

## Prerequisites

- Python 3.10+ (recommended).
- Node.js 18+ and npm or pnpm.

## Quick start

Follow these steps to run the backend and frontend locally.

### Backend

1. Change to the backend directory:

   - `cd backend`

2. Create a virtual environment and activate it:

```bash
python -m venv .venv
source .venv/bin/activate
```

3. Install Python dependencies:

```bash
pip install -r requirements.txt
```

4. Create an environment file:

   - Copy `.env.example` to `.env` and update values as needed (DB URL, secrets, AI keys).

5. Run database migrations (Alembic):

```bash
alembic upgrade head
```

6. Start the development server:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`. Open the automatic docs at `http://localhost:8000/docs`.

See backend-specific notes in [backend/README.md](backend/README.md).

### Frontend

1. Change to the frontend directory:

   - `cd frontend`

2. Install dependencies:

```bash
npm install
```

3. Create an environment file:

   - Copy `.env.example` to `.env` and set the API URL and any other values required.

4. Start the development server:

```bash
npm run dev
```

The app will be available at `http://localhost:5173` by default.

See frontend-specific instructions in [frontend/README.md](frontend/README.md).

## Configuration & environment variables

- Backend uses `.env` and supports overriding via environment variables. Key items include `DATABASE_URL`, `HOST`, `PORT`, and AI provider keys. Defaults are defined in `backend/config.py`.
- Frontend uses `.env` in the `frontend` folder; copy `.env.example` and configure the API base URL.

## Running tests

- Backend tests: from the `backend` directory run `pytest` or `python run_tests.py`.
- Frontend: type-checking and other checks are available via the `package.json` scripts.

## Project structure

- `backend/` — FastAPI application, models, services, tests, Alembic migrations.
- `frontend/` — React TypeScript app, routes, components, and styles.

## Development notes

- The default backend database is SQLite for convenience. To use Postgres or another DB, set `DATABASE_URL` accordingly and run migrations.
- CORS is configured to allow the common Vite dev port; update `CORS_ORIGINS` in the backend `.env` if your setup differs.
- AI integration points are present under `backend/integrations/ai_integration` and `backend/services/ai_service.py` — supply API keys via `.env` to enable AI features.

## Contributing

Contributions are welcome. Please open issues for bugs or feature requests and submit pull requests for changes. Follow existing code style and add tests for new behavior.

## License

This repository does not include a license file. Add a `LICENSE` if you intend to open-source the project.
