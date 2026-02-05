import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from models.application import Application
from schemas.application import ApplicationAnswer


def test_create_application(client: TestClient, sample_job_data: dict, sample_assessment_data: dict, sample_user_data: dict):
    """Test creating a new application for an assessment"""
    # Create a job first
    response = client.post("/jobs", json=sample_job_data)
    assert response.status_code == 200
    job_id = response.json()["id"]
    
    # Create an assessment for the job
    response = client.post(f"/assessments/jobs/{job_id}", json=sample_assessment_data)
    assert response.status_code == 200
    assessment_id = response.json()["id"]
    
    # Register a user first
    response = client.post("/users/registration/signup", json=sample_user_data)
    assert response.status_code == 200
    token_response = response.json()
    user_id = token_response["token"].replace("fake_token_for_", "")
    
    # Create an application for the assessment
    application_data = {
        "job_id": job_id,
        "assessment_id": assessment_id,
        "user_id": user_id,
        "answers": [
            {
                "question_id": "question1",
                "answer_text": "Sample answer to question 1"
            },
            {
                "question_id": "question2", 
                "answer_text": "Sample answer to question 2"
            }
        ]
    }
    response = client.post(f"/applications/jobs/{job_id}/assessments/{assessment_id}", json=application_data)
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert len(data["id"]) > 0  # UUID should be returned


def test_get_applications_list(client: TestClient, sample_job_data: dict, sample_assessment_data: dict, sample_user_data: dict):
    """Test getting list of applications for an assessment"""
    # Create a job first
    response = client.post("/jobs", json=sample_job_data)
    assert response.status_code == 200
    job_id = response.json()["id"]
    
    # Create an assessment for the job
    response = client.post(f"/assessments/jobs/{job_id}", json=sample_assessment_data)
    assert response.status_code == 200
    assessment_id = response.json()["id"]
    
    # Register a user first
    response = client.post("/users/registration/signup", json=sample_user_data)
    assert response.status_code == 200
    token_response = response.json()
    user_id = token_response["token"].replace("fake_token_for_", "")
    
    # Create an application for the assessment
    application_data = {
        "job_id": job_id,
        "assessment_id": assessment_id,
        "user_id": user_id,
        "answers": [
            {
                "question_id": "question1",
                "answer_text": "Sample answer to question 1"
            }
        ]
    }
    response = client.post(f"/applications/jobs/{job_id}/assessments/{assessment_id}", json=application_data)
    assert response.status_code == 200
    application_id = response.json()["id"]
    
    # Get the list of applications for the assessment
    response = client.get(f"/applications/jobs/{job_id}/assessments/{assessment_id}")
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert len(data["data"]) >= 1
    
    # Find our application in the list
    found_application = None
    for application in data["data"]:
        if application["id"] == application_id:
            found_application = application
            break
    
    assert found_application is not None
    assert found_application["id"] == application_id
    assert found_application["job_id"] == job_id
    assert found_application["assessment_id"] == assessment_id
    assert found_application["user_id"] == user_id
    assert len(found_application["answers"]) == 1
    assert found_application["answers"][0]["question_id"] == "question1"
    assert found_application["answers"][0]["answer_text"] == "Sample answer to question 1"


def test_create_application_with_invalid_job_or_assessment(client: TestClient, sample_user_data: dict):
    """Test creating an application with invalid job or assessment"""
    # Register a user first
    response = client.post("/users/registration/signup", json=sample_user_data)
    assert response.status_code == 200
    token_response = response.json()
    user_id = token_response["token"].replace("fake_token_for_", "")
    
    # Try to create an application with invalid job/assessment IDs
    application_data = {
        "job_id": "invalid-job-id",
        "assessment_id": "invalid-assessment-id",
        "user_id": user_id,
        "answers": []
    }
    response = client.post("/applications/jobs/invalid-job-id/assessments/invalid-assessment-id", json=application_data)
    assert response.status_code == 404
    assert "Assessment not found for this job" in response.json()["detail"]


def test_health_check_endpoint(client: TestClient):
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert data["status"] == "healthy"
    assert "database" in data
    assert data["database"] == "connected"
    assert "timestamp" in data