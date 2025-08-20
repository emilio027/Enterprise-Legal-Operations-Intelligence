"""
Test cases for the main application.
"""

import pytest
import sys
import os

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from main import app


@pytest.fixture
def client():
    """Test client fixture."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_home_endpoint(client):
    """Test the home endpoint."""
    response = client.get('/')
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == 'Intelligence Platform API'
    assert data['status'] == 'running'


def test_health_check(client):
    """Test the health check endpoint."""
    response = client.get('/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'
    assert data['service'] == 'intelligence-platform'


def test_api_status(client):
    """Test the API status endpoint."""
    response = client.get('/api/v1/status')
    assert response.status_code == 200
    data = response.get_json()
    assert data['api_version'] == 'v1'
    assert data['status'] == 'operational'
    assert 'features' in data
    assert len(data['features']) > 0


def test_invalid_endpoint(client):
    """Test accessing an invalid endpoint."""
    response = client.get('/invalid-endpoint')
    assert response.status_code == 404
