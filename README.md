# RunTracker

![Python](https://img.shields.io/badge/python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-latest-green)
![Docker](https://img.shields.io/badge/Docker-ready-blue)

REST API for tracking running workouts.

## Description

RunTracker lets you record your running workouts and get statistics on them.

## Prerequisites

- Docker
- Docker Compose >= 2.0

## Installation

RunTracker uses Docker to containerize the system and simplify deployment.
The `.env` file must be edited to provide the correct environment variables.

```bash
# Clone the git repository
git clone https://github.com/LecoqML0/RunTracker.git
cd RunTracker

# Copy the environment variables file
cp .env.example .env
# Edit it before launching (see Configuration section)

# Launch RunTracker
docker compose up --build
```

## Configuration

| Variable                      | Description                    | Default      |
|-------------------------------|--------------------------------|--------------|
| `SECRET_KEY`                  | JWT signing key                | —            |
| `ALGORITHM`                   | JWT signing algorithm          | `HS256`      |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | JWT token lifetime (minutes)   | `30`         |
| `DATABASE_URL`                | Full PostgreSQL connection URL | —            |
| `POSTGRES_USER`               | PostgreSQL username            | `postgres`   |
| `POSTGRES_PASSWORD`           | PostgreSQL password            | —            |
| `POSTGRES_DB`                 | PostgreSQL database name       | `runtracker` |

### Secret key

Generate a strong secret key with: `openssl rand -hex 32`

### Database URL

Example of a valid format: `postgresql://postgres:password@db:5432/runtracker`

## Project structure

├── app/  
│   ├── api/  
│   ├── schemas/  
│   ├── config.py  
│   ├── database.py  
│   ├── main.py  
│   └── security.py  
├── scripts/  
│   └── create_admin.py  
├── docker-compose.yaml  
├── Dockerfile  
├── README.md  
└── requirements.txt

- `api/` — FastAPI route handlers
- `schemas/` — Pydantic models (user, run, ...)

## Endpoints

### `/auth`

- `POST /register` — create a new user account
- `POST /login` — authenticate and retrieve a JWT token, required to access all other endpoints

### `/user/me`

Get information about the currently authenticated user, or delete the account.

### `/run`

Manage the authenticated user's workouts. Use `/run/{run_id}` to get, update or delete a specific workout.

### `/admin`

Restricted to users with administrator privileges. Allows managing users and workouts.

## Documentation

Interactive API documentation is available at `/docs` (e.g. `http://localhost:8000/docs`).