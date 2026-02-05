# Test Suite for AI-Powered Hiring Assessment Platform

This directory contains all the tests for the AI-Powered Hiring Assessment Platform.

## Test Organization

The tests are organized into several categories:

### 1. Core Functionality Tests
- `test_users.py` - Tests for user registration, login, and profile management
- `test_jobs.py` - Tests for job posting and management
- `test_assessments.py` - Tests for assessment creation and management
- `test_applications.py` - Tests for application submission and scoring

### 2. AI Service Tests
- `test_ai_assessment.py` - Tests for AI-generated question creation
- `test_ai_scoring.py` - Tests for AI-based answer scoring
- `test_factory_pattern.py` - Tests for the AI provider factory pattern

### 3. Integration Tests
- `test_comprehensive_suite.py` - Comprehensive test suite covering all functionality
- `test_full_workflow_with_job_info.py` - Tests for complete workflows with job information
- `test_regenerate_endpoint_flow.py` - Tests for assessment regeneration functionality

### 4. Utility Tests
- `test_application_scores.py` - Tests for application scoring mechanisms
- `test_scoring_methodology.py` - Tests for different scoring methodologies

## Running Tests

### Individual Test Files
```bash
python -m pytest tests/test_users.py -v
python -m pytest tests/test_assessments.py -v
```

### All Tests
```bash
python run_tests.py
# or
python -m pytest tests/ -v
```

## Test Coverage

The test suite covers:
- User authentication and authorization
- Job creation and management
- Assessment creation with AI-generated questions
- Application submission and scoring
- AI provider factory pattern
- Database operations and relationships
- API endpoints and request/response handling
- Error handling and validation

## Test Data

The test suite includes seeded data for:
- 4 HR accounts with credentials
- 4 Candidate accounts with credentials
- Sample jobs with varying seniority levels
- Sample assessments with different question types
- Sample applications with answers

See the main README.md file for demo account credentials.