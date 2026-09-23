import pytest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient


@pytest.fixture(autouse=True)
def mock_mongo(monkeypatch):
    mock_db = MagicMock()
    monkeypatch.setattr("app.config.db", mock_db)
    monkeypatch.setattr("app.recomRoute.db", mock_db)
    return mock_db


@pytest.fixture(autouse=True)
def mock_publisher(monkeypatch):
    mock_pub = MagicMock()
    mock_pub.pubRecom.return_value = True
    monkeypatch.setattr("app.recomRoute.get_rabbitmq_publisher", lambda: mock_pub)
    return mock_pub


@pytest.fixture
def client(mock_mongo, mock_publisher):
    from app.main import app
    return TestClient(app)


@pytest.fixture
def sample_item():
    return {
        "_id": "507f1f77bcf86cd799439011",
        "id": "507f1f77bcf86cd799439011",
        "name": "Test Shirt",
        "brand": "TestBrand",
        "light": 5, "dark": 3, "bright": 4, "warm": 2,
        "cool": 1, "fancy": 3, "casual": 5, "business": 2,
        "evening": 1, "minimalist": 4, "vintage": 2, "modern": 5,
        "floral": 1, "colourful": 3,
        "img_url": "http://example.com/img.jpg"
    }
