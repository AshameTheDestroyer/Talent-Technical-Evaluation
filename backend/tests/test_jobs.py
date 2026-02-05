import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from models.job import Job


def test_create_job(client: TestClient, sample_job_data: dict):
    """Test creating a new job"""
    response = client.post("/jobs", json=sample_job_data)
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert len(data["id"]) > 0  # UUID should be returned


def test_get_job_list(client: TestClient, sample_job_data: dict):
    """Test getting list of jobs"""
    # Create a job first
    response = client.post("/jobs", json=sample_job_data)
    assert response.status_code == 200
    job_id = response.json()["id"]
    
    # Get the list of jobs
    response = client.get("/jobs")
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert len(data["data"]) >= 1
    
    # Find our job in the list
    found_job = None
    for job in data["data"]:
        if job["id"] == job_id:
            found_job = job
            break
    
    assert found_job is not None
    assert found_job["title"] == sample_job_data["title"]
    assert found_job["seniority"] == sample_job_data["seniority"]
    assert found_job["description"] == sample_job_data["description"]
    assert found_job["skill_categories"] == sample_job_data["skill_categories"]
    assert found_job["active"] == sample_job_data["active"]


def test_get_job_details(client: TestClient, sample_job_data: dict):
    """Test getting job details by ID"""
    # Create a job first
    response = client.post("/jobs", json=sample_job_data)
    assert response.status_code == 200
    job_id = response.json()["id"]
    
    # Get job details
    response = client.get(f"/jobs/{job_id}")
    assert response.status_code == 200
    job_data = response.json()
    assert job_data["id"] == job_id
    assert job_data["title"] == sample_job_data["title"]
    assert job_data["seniority"] == sample_job_data["seniority"]
    assert job_data["description"] == sample_job_data["description"]
    assert job_data["skill_categories"] == sample_job_data["skill_categories"]
    assert job_data["active"] == sample_job_data["active"]
    assert "applicants_count" in job_data


def test_update_job(client: TestClient, sample_job_data: dict):
    """Test updating an existing job"""
    # Create a job first
    response = client.post("/jobs", json=sample_job_data)
    assert response.status_code == 200
    job_id = response.json()["id"]
    
    # Update the job
    updated_data = {
        "title": "Updated Software Engineer",
        "description": "Updated job description"
    }
    response = client.patch(f"/jobs/{job_id}", json=updated_data)
    assert response.status_code == 200
    
    # Verify the update
    response = client.get(f"/jobs/{job_id}")
    assert response.status_code == 200
    job_data = response.json()
    assert job_data["title"] == updated_data["title"]
    assert job_data["description"] == updated_data["description"]


def test_update_nonexistent_job(client: TestClient):
    """Test updating a nonexistent job"""
    updated_data = {
        "title": "Updated Software Engineer",
        "description": "Updated job description"
    }
    response = client.patch("/jobs/nonexistent-id", json=updated_data)
    assert response.status_code == 404
    assert "Job not found" in response.json()["detail"]


def test_delete_job(client: TestClient, sample_job_data: dict):
    """Test deleting a job"""
    # Create a job first
    response = client.post("/jobs", json=sample_job_data)
    assert response.status_code == 200
    job_id = response.json()["id"]
    
    # Delete the job
    response = client.delete(f"/jobs/{job_id}")
    assert response.status_code == 200
    
    # Verify the job is gone
    response = client.get(f"/jobs/{job_id}")
    assert response.status_code == 404
    assert "Job not found" in response.json()["detail"]


def test_delete_nonexistent_job(client: TestClient):
    """Test deleting a nonexistent job"""
    response = client.delete("/jobs/nonexistent-id")
    assert response.status_code == 404
    assert "Job not found" in response.json()["detail"]