"""Tests for the job controller module."""

from datetime import timedelta
from unittest.mock import patch

from controller.job_controller import get_all_jobs_above_24_hours, _process_job_item
from model.job import Job

def create_mock_job():
    """Create a mock job for testing."""
    return Job(
        id="test-id",
        object_name="test-object",
        object_type="VM",
        start_time="2024-01-01T00:00:00Z",
        duration=90000000,  # 25 hours in milliseconds
        job_status="RUNNING",
        job_type="Backup",
        sla_name="Gold",
        cluster_name="test-cluster"
    )

def create_mock_api_response():
    """Create a mock API response."""
    return {
        "data": {
            "reportData": {
                "edges": [
                    {
                        "cursor": "cursor1",
                        "node": {
                            "id": "test-id",
                            "objectName": "test-object",
                            "objectType": "VM",
                            "startTime": "2024-01-01T00:00:00Z",
                            "duration": 90000000,
                            "status": "RUNNING",
                            "jobType": "Backup",
                            "slaName": "Gold",
                            "clusterName": "test-cluster"
                        }
                    }
                ]
            }
        }
    }

def test_process_job_item_valid():
    """Test processing a valid job item."""
    mock_job = create_mock_job()
    mock_item = {
        "node": {
            "id": "test-id",
            "objectName": "test-object",
            "objectType": "VM",
            "startTime": "2024-01-01T00:00:00Z",
            "duration": 90000000,
            "status": "RUNNING",
            "jobType": "Backup",
            "slaName": "Gold",
            "clusterName": "test-cluster"
        }
    }
    
    with patch('data.job_data_operation.create_job_from_data', return_value=mock_job):
        result = _process_job_item(mock_item)
        assert result is not None
        assert result.id == "test-id"
        assert result.object_name == "test-object"
        assert result.cluster_name == "test-cluster"

def test_process_job_item_invalid():
    """Test processing an invalid job item."""
    mock_item = {"node": {}}
    result = _process_job_item(mock_item)
    assert result is None

def test_get_all_jobs_above_24_hours():
    """Test retrieving jobs above 24 hours."""
    mock_api_response = create_mock_api_response()
    mock_job = create_mock_job()
    
    with patch('connection.wrapper.request', return_value=mock_api_response), \
         patch('data.job_data_operation.create_job_from_data', return_value=mock_job):
        
        result = get_all_jobs_above_24_hours("fake-token")
        assert len(result) == 1
        assert result[0].id == "test-id"
        assert result[0].object_name == "test-object"
        assert result[0].cluster_name == "test-cluster"