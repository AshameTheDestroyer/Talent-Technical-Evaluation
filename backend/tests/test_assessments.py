import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from models.assessment import Assessment


def test_create_assessment(client: TestClient, sample_job_data: dict, sample_assessment_data: dict):
    """Test creating a new assessment for a job"""
    # Create a job first
    response = client.post("/jobs", json=sample_job_data)
    assert response.status_code == 200
    job_id = response.json()["id"]
    
    # Create an assessment for the job
    response = client.post(f"/assessments/jobs/{job_id}", json=sample_assessment_data)
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert len(data["id"]) > 0  # UUID should be returned


def test_get_assessment_list(client: TestClient, sample_job_data: dict, sample_assessment_data: dict):
    """Test getting list of assessments for a job"""
    # Create a job first
    response = client.post("/jobs", json=sample_job_data)
    assert response.status_code == 200
    job_id = response.json()["id"]
    
    # Create an assessment for the job
    response = client.post(f"/assessments/jobs/{job_id}", json=sample_assessment_data)
    assert response.status_code == 200
    assessment_id = response.json()["id"]
    
    # Get the list of assessments for the job
    response = client.get(f"/assessments/jobs/{job_id}")
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert len(data["data"]) >= 1
    
    # Find our assessment in the list
    found_assessment = None
    for assessment in data["data"]:
        if assessment["id"] == assessment_id:
            found_assessment = assessment
            break
    
    assert found_assessment is not None
    assert found_assessment["id"] == assessment_id
    assert found_assessment["title"] == sample_assessment_data["title"]
    assert found_assessment["passing_score"] == sample_assessment_data["passing_score"]
    assert found_assessment["questions"] == []
    assert found_assessment["questions_count"] == 0


def test_get_assessment_details(client: TestClient, sample_job_data: dict, sample_assessment_data: dict):
    """Test getting assessment details"""
    # Create a job first
    response = client.post("/jobs", json=sample_job_data)
    assert response.status_code == 200
    job_id = response.json()["id"]
    
    # Create an assessment for the job
    response = client.post(f"/assessments/jobs/{job_id}", json=sample_assessment_data)
    assert response.status_code == 200
    assessment_id = response.json()["id"]
    
    # Get assessment details
    response = client.get(f"/assessments/jobs/{job_id}/{assessment_id}")
    assert response.status_code == 200
    assessment_data = response.json()
    assert assessment_data["id"] == assessment_id
    assert assessment_data["job_id"] == job_id
    assert assessment_data["title"] == sample_assessment_data["title"]
    assert assessment_data["passing_score"] == sample_assessment_data["passing_score"]
    assert assessment_data["questions"] == []
    assert assessment_data["questions_count"] == 0


def test_update_assessment(client: TestClient, sample_job_data: dict, sample_assessment_data: dict):
    """Test updating an existing assessment"""
    # Create a job first
    response = client.post("/jobs", json=sample_job_data)
    assert response.status_code == 200
    job_id = response.json()["id"]
    
    # Create an assessment for the job
    response = client.post(f"/assessments/jobs/{job_id}", json=sample_assessment_data)
    assert response.status_code == 200
    assessment_id = response.json()["id"]
    
    # Update the assessment
    updated_data = {
        "title": "Updated Technical Assessment",
        "passing_score": 80.0
    }
    response = client.patch(f"/assessments/jobs/{job_id}/{assessment_id}", json=updated_data)
    assert response.status_code == 200
    
    # Verify the update
    response = client.get(f"/assessments/jobs/{job_id}/{assessment_id}")
    assert response.status_code == 200
    assessment_data = response.json()
    assert assessment_data["title"] == updated_data["title"]
    assert assessment_data["passing_score"] == updated_data["passing_score"]


def test_update_nonexistent_assessment(client: TestClient, sample_job_data: dict):
    """Test updating a nonexistent assessment"""
    # Create a job first
    response = client.post("/jobs", json=sample_job_data)
    assert response.status_code == 200
    job_id = response.json()["id"]
    
    updated_data = {
        "title": "Updated Technical Assessment",
        "passing_score": 80.0
    }
    response = client.patch(f"/assessments/jobs/{job_id}/nonexistent-id", json=updated_data)
    assert response.status_code == 404
    assert "Assessment not found" in response.json()["detail"]


def test_regenerate_assessment(client: TestClient, sample_job_data: dict, sample_assessment_data: dict):
    """Test regenerating an assessment"""
    # Create a job first
    response = client.post("/jobs", json=sample_job_data)
    assert response.status_code == 200
    job_id = response.json()["id"]
    
    # Create an assessment for the job
    response = client.post(f"/assessments/jobs/{job_id}", json=sample_assessment_data)
    assert response.status_code == 200
    assessment_id = response.json()["id"]
    
    # Regenerate the assessment
    regenerate_data = {
        "title": "Regenerated Technical Assessment",
        "passing_score": 75.0
    }
    response = client.patch(f"/assessments/jobs/{job_id}/{assessment_id}/regenerate", json=regenerate_data)
    assert response.status_code == 200
    
    # Verify the regeneration
    response = client.get(f"/assessments/jobs/{job_id}/{assessment_id}")
    assert response.status_code == 200
    assessment_data = response.json()
    assert assessment_data["title"] == regenerate_data["title"]
    assert assessment_data["passing_score"] == regenerate_data["passing_score"]


def test_regenerate_nonexistent_assessment(client: TestClient, sample_job_data: dict):
    """Test regenerating a nonexistent assessment"""
    # Create a job first
    response = client.post("/jobs", json=sample_job_data)
    assert response.status_code == 200
    job_id = response.json()["id"]
    
    regenerate_data = {
        "title": "Regenerated Technical Assessment",
        "passing_score": 75.0
    }
    response = client.patch(f"/assessments/jobs/{job_id}/nonexistent-id/regenerate", json=regenerate_data)
    assert response.status_code == 404
    assert "Assessment not found" in response.json()["detail"]


def test_delete_assessment(client: TestClient, sample_job_data: dict, sample_assessment_data: dict):
    """Test deleting an assessment"""
    # Create a job first
    response = client.post("/jobs", json=sample_job_data)
    assert response.status_code == 200
    job_id = response.json()["id"]
    
    # Create an assessment for the job
    response = client.post(f"/assessments/jobs/{job_id}", json=sample_assessment_data)
    assert response.status_code == 200
    assessment_id = response.json()["id"]
    
    # Delete the assessment
    response = client.delete(f"/assessments/jobs/{job_id}/{assessment_id}")
    assert response.status_code == 200
    
    # Verify the assessment is gone
    response = client.get(f"/assessments/jobs/{job_id}/{assessment_id}")
    assert response.status_code == 404
    assert "Assessment not found for this job" in response.json()["detail"]


def test_delete_nonexistent_assessment(client: TestClient, sample_job_data: dict):
    """Test deleting a nonexistent assessment"""
    # Create a job first
    response = client.post("/jobs", json=sample_job_data)
    assert response.status_code == 200
    job_id = response.json()["id"]
    
    response = client.delete(f"/assessments/jobs/{job_id}/nonexistent-id")
    assert response.status_code == 404
    assert "Assessment not found" in response.json()["detail"]