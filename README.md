# Mini Instagram API

A backend implementation for a mini-Instagram application built with Django and Django Rest Framework.

## Features

- **Authentication**: JWT-based authentication with email verification.
- **Posts**: CRUD operations for posts with Base64 image support.
- **Interactions**: Like and comment on posts.
- **Feed**: A nested feed endpoint showing users and their posts.
- **Filtering & Search**: Filter posts by date and search by title/content.
- **Validation**: Strict data validation for all inputs.
- **Background Tasks**: Celery for long-running tasks (like cleaning up unverified users).

## Infrastructure

- **Django 6.0.1**
- **Rest Framework**
- **PostgreSQL** (Database)
- **Redis** (Broker for Celery)
- **Celery** (Task Queue)
- **Docker & Docker Compose**

## Getting Started

### Prerequisites

- Docker and Docker Compose installed on your machine.

### Local Setup

1.  **Clone the repository**:
    ```bash
    git clone <repository-url>
    cd mini-instagram
    ```

2.  **Environment Variables**:
    Copy `.env.example` to `.env` and adjust the settings if necessary.
    ```bash
    cp .env.example .env
    ```

3.  **Build and Start with Docker Compose**:
    ```bash
    docker compose up --build
    ```
    This will start the following services:
    - `db`: PostgreSQL database.
    - `redis`: Redis server.
    - `web`: Django application (running on http://localhost:8000).
    - `celery-worker`: Celery worker for background tasks.
    - `celery-beat`: Celery beat for periodic tasks.

4.  **Run Migrations**:
    ```bash
    docker compose exec web python manage.py migrate
    ```

5.  **Create a Superuser** (Optional):
    ```bash
    docker compose exec web python manage.py createsuperuser
    ```

## API Endpoints

### Authentication
- `POST /auth/register/`: Register a new user.
- `POST /auth/verify-email/`: Verify email with token.
- `POST /auth/login/`: Login and get JWT tokens.

### Feed
- `GET /feed/`: Get the nested feed of users and their posts (supports pagination).

### Posts
- `GET /posts/`: List posts (supports search and date filtering).
- `POST /posts/`: Create a new post (Verified users only).
- `GET /posts/<id>/`: Get post detail.
- `PATCH /posts/<id>/`: Update post (Author only).
- `DELETE /posts/<id>/`: Delete post (Author only).
- `POST /posts/<id>/like/`: Like/Unlike a post.

### Comments
- `GET /posts/<id>/comments/`: List comments for a post.
- `POST /posts/<id>/comments/`: Create a comment (Verified users only).
- `DELETE /posts/<post_id>/comments/<comment_id>/`: Delete comment (Author only).

## API Documentation

The project includes automatically generated API documentation using `drf-spectacular`.

- **Swagger UI**: [http://localhost:8000/api/schema/swagger-ui/](http://localhost:8000/api/schema/swagger-ui/)
- **Redoc**: [http://localhost:8000/api/schema/redoc/](http://localhost:8000/api/schema/redoc/)
- **OpenAPI Schema**: [http://localhost:8000/api/schema/](http://localhost:8000/api/schema/)

## Project Structure

```bash
├── authentication # Auth logic, registration, verification
├── common         # Shared models, permissions, paginations, serializers
├── config         # Project settings, URLs, Celery config
├── posts          # Posts, comments, and likes
├── users          # Custom User model and managers
├── scripts        # Utility scripts
└── docker-compose.yml
```

## Quality and Style

The project follows strict coding standards:
- **Formatting**: `black` and `isort` for consistent code style.
- **Linting**: `flake8` for code quality checks (see `.flake8`).
- **Configuration**: `.editorconfig` for editor consistency.
- **Validation**: Comprehensive model and serializer validation.

## Running Tests

To run the automated tests:
```bash
docker compose exec web python manage.py test
```

## Code Quality (Pre-commit)

This project uses `pre-commit` to maintain code quality. To set up the hooks locally:

1.  Install `pre-commit`: `pip install pre-commit`
2.  Install the hooks: `pre-commit install`

Now, `black`, `isort`, and `flake8` will run automatically on every commit.

## Deployment

The project includes a CD workflow in `.github/workflows/deploy.yml` that automates deployment to a production server on every push to `main`.

### Setup

To enable automated deployment, you must add the following **Secrets** to your GitHub repository (`Settings > Secrets and variables > Actions`):

1.  `SERVER_IP`: The public IP address of your production server.
2.  `SERVER_USER`: The username used to connect via SSH (e.g., `root` or `ubuntu`).
3.  `SSH_PRIVATE_KEY`: Your SSH private key (ensure the corresponding public key is in `~/.ssh/authorized_keys` on the server).
4.  `DEPLOY_PATH`: The absolute path to the project directory on your server (e.g., `/var/www/mini-instagram`).
