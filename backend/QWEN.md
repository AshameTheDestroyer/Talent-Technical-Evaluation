# AI-Powered Hiring Assessment Platform Backend

## Project Overview

This is a FastAPI-based backend application for an AI-powered hiring assessment platform. The system enables HR professionals to create and manage assessments for job candidates, while allowing candidates to take assessments and review their results.

The application follows a clean architecture with proper separation of concerns:
- **API Layer**: Handles HTTP requests and responses
- **Service Layer**: Contains business logic
- **Database Layer**: Manages database connections and sessions
- **Model Layer**: Defines database models using SQLAlchemy
- **Schema Layer**: Defines Pydantic schemas for request/response validation

## Technologies Used

- **Python 3.11**
- **FastAPI**: Modern, fast web framework for building APIs
- **SQLAlchemy**: SQL toolkit and ORM for database operations
- **SQLite**: Lightweight database for development
- **Alembic**: Database migration tool
- **Pydantic**: Data validation and settings management
- **UUID**: For generating unique identifiers

## Architecture Components

### Directory Structure
```
backend/
├── api/                 # API route definitions
│   ├── user_routes.py   # User registration/login endpoints
│   ├── job_routes.py    # Job-related endpoints
│   ├── assessment_routes.py # Assessment-related endpoints
│   ├── application_routes.py # Application-related endpoints
│   └── routes.py        # Root and health check endpoints
├── database/            # Database connection utilities
│   └── database.py      # Database engine and session management
├── models/              # SQLAlchemy models
│   ├── user.py          # User model
│   ├── job.py           # Job model
│   ├── assessment.py    # Assessment model
│   ├── application.py   # Application model
│   └── base.py          # Base model class
├── schemas/             # Pydantic schemas
│   ├── user.py          # User schemas
│   ├── job.py           # Job schemas
│   ├── assessment.py    # Assessment schemas
│   ├── application.py   # Application schemas
│   └── base.py          # Base schema class
├── services/            # Business logic layer
│   ├── user_service.py  # User-related services
│   ├── job_service.py   # Job-related services
│   ├── assessment_service.py # Assessment-related services
│   ├── application_service.py # Application-related services
│   └── base_service.py  # Generic service functions
├── alembic/             # Database migration files
├── config.py            # Application configuration
├── logging_config.py    # Logging configuration
├── main.py              # Application entry point
├── .env                 # Environment variables
└── requirements.txt     # Python dependencies
```

### Key Features

1. **User Management**:
   - Registration and authentication
   - Role-based access (HR vs Applicant)

2. **Job Management**:
   - Create, update, delete job postings
   - Manage job details and requirements

3. **Assessment Management**:
   - Create assessments linked to jobs
   - Define questions and passing scores
   - Regenerate assessments with new questions

4. **Application Management**:
   - Submit applications with answers
   - Track application results and scores

### API Endpoints

#### Registration
- `POST /registration/signup` - User registration
- `POST /registration/login` - User login
- `POST /registration/logout` - User logout

#### Users
- `GET /users/{id}` - Get user details

#### Jobs
- `GET /jobs` - List jobs
- `GET /jobs/{id}` - Get job details
- `POST /jobs` - Create job
- `PATCH /jobs/{id}` - Update job
- `DELETE /jobs/{id}` - Delete job

#### Assessments
- `GET /assessments/jobs/{jid}` - List assessments for a job
- `GET /assessments/jobs/{jid}/{aid}` - Get assessment details
- `POST /assessments/jobs/{id}` - Create assessment
- `PATCH /assessments/jobs/{jid}/{aid}/regenerate` - Regenerate assessment
- `PATCH /assessments/jobs/{jid}/{aid}` - Update assessment
- `DELETE /assessments/jobs/{jid}/{aid}` - Delete assessment

#### Applications
- `GET /applications/jobs/{jid}/assessments/{aid}` - List applications
- `POST /applications/jobs/{jid}/assessments/{aid}` - Create application

#### Health Check
- `GET /` - Root endpoint
- `GET /health` - Health check endpoint

## Configuration

The application uses a `.env` file for configuration, managed through the `config.py` file:

```env
# Database Configuration
DATABASE_URL=sqlite:///./assessment_platform.db

# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=False

# Logging Configuration
LOG_LEVEL=INFO
LOG_FILE=app.log
LOG_FORMAT=%(asctime)s - %(name)s - %(levelname)s - %(message)s

# JWT Configuration (for future use)
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Application Configuration
APP_NAME=AI-Powered Hiring Assessment Platform
APP_VERSION=0.1.0
APP_DESCRIPTION=MVP for managing hiring assessments using AI
```

## Building and Running

### Prerequisites
- Python 3.11+
- pip package manager

### Setup Instructions

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   
2. **Set Up Environment Variables**:
   Copy the `.env.example` file to `.env` and adjust the values as needed.

3. **Run Database Migrations**:
   ```bash
   alembic upgrade head
   ```

4. **Start the Application**:
   ```bash
   python main.py
   ```
   
   Or using uvicorn directly:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

### Development Mode
For development, you can run the application with hot-reloading enabled:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Testing

To run tests (when available):
```bash
pytest
```

## Logging

The application implements comprehensive logging through the `logging_config.py` module:
- Logs are written to both file (`app.log`) and console
- Log level can be configured via the `LOG_LEVEL` environment variable
- Different log levels (DEBUG, INFO, WARNING, ERROR) are used appropriately
- All major operations are logged with contextual information

## Database Migrations

The application uses Alembic for database migrations:
- To create a new migration: `alembic revision --autogenerate -m "Description"`
- To apply migrations: `alembic upgrade head`
- To check current migration status: `alembic current`

## Development Conventions

1. **Code Style**:
   - Follow PEP 8 guidelines
   - Use type hints for all function parameters and return values
   - Write docstrings for all public functions and classes

2. **Error Handling**:
   - Use appropriate HTTP status codes
   - Return meaningful error messages
   - Log errors appropriately

3. **Security**:
   - Passwords should be hashed (currently using placeholder)
   - Input validation through Pydantic schemas
   - SQL injection prevention through SQLAlchemy ORM

4. **Architecture**:
   - Keep business logic in service layer
   - Use dependency injection for database sessions
   - Separate API routes by domain/model
   - Maintain clear separation between layers

## Future Enhancements

- JWT token-based authentication
- Password hashing implementation
- Advanced assessment features
- Admin dashboard endpoints
- More sophisticated logging and monitoring
- Unit and integration tests

# TODO:
- when creating an assessment we should pass the questions of the assessment. 
- all APIs input and output should have a cleare schema, even the enums should be clear and apear in the swagger apis (when visiting /docs)
- the validation of the inputs should be done by pydantic and in the model level, not in the model level only! 
- the answers is not a model itself, so the services/answer functions should be aware of that. 

