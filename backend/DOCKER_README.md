# AI-Powered Hiring Assessment Platform - Docker Setup

This guide explains how to build and run the AI-Powered Hiring Assessment Platform using Docker.

## Prerequisites

- Docker installed on your machine
- Docker Compose installed (usually comes with Docker Desktop)

## Building and Running the Application

### 1. Clone the Repository

```bash
git clone <repository-url>
cd backend
```

### 2. Build and Run with Docker Compose

The easiest way to run the application is using Docker Compose:

```bash
docker-compose up --build
```

This command will:
- Build the backend image
- Start the backend service
- Expose the application on port 8000

### 3. Access the Application

Once the containers are running, you can access the application at:
- API Documentation: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

### 4. Alternative: Build and Run Individual Containers

If you prefer to build and run individual containers:

#### Build the Image
```bash
docker build -t assessment-platform-backend .
```

#### Run the Container
```bash
docker run -p 8000:8000 assessment-platform-backend
```

## Environment Variables

The application uses the following environment variables (defined in docker-compose.yml):

- `DATABASE_URL`: Database connection string (defaults to SQLite)
- `HOST`: Host address (defaults to 0.0.0.0)
- `PORT`: Port number (defaults to 8000)
- `DEBUG`: Debug mode (defaults to True)
- `LOG_LEVEL`: Logging level (defaults to INFO)
- `LOG_FILE`: Log file path (defaults to app.log)
- `SECRET_KEY`: Secret key for JWT tokens
- `ALGORITHM`: Algorithm for JWT encoding
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time
- `APP_NAME`: Application name
- `APP_VERSION`: Application version
- `APP_DESCRIPTION`: Application description

## Stopping the Application

To stop the application:

```bash
# If running with docker-compose
Ctrl+C in the terminal where it's running

# Or in another terminal
docker-compose down
```

## Troubleshooting

1. **Port Already in Use**: If port 8000 is already in use, change the port mapping in docker-compose.yml

2. **Permission Issues**: Make sure you have the necessary permissions to run Docker commands

3. **Build Errors**: Check that all dependencies in requirements.txt are compatible with the Python version

## Development Notes

- The current setup uses SQLite as the database for simplicity
- For production deployments, consider using PostgreSQL or MySQL
- The volume mount in docker-compose.yml allows for live reloading during development
- Logs are stored in the ./logs directory on the host machine