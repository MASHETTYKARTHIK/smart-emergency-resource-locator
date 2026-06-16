from unittest.mock import MagicMock

import pytest

from src.api.emergency.client import EmergencyClient
from src.api.emergency.service import EmergencyService


@pytest.fixture
def mock_client():
    return MagicMock(spec=EmergencyClient)


@pytest.fixture
def service(mock_client):
    return EmergencyService(client=mock_client)


def test_haversine():
    # Gachibowli to HITEC City approx 3.5km
    dist = EmergencyService.haversine(17.4401, 78.3489, 17.4500, 78.3810)
    assert 3.0 < dist < 4.0  # nosec


def test_get_nearest_resource_success(service, mock_client):
    # Mock Overpass response
    mock_client.search_resources.return_value = {
        "elements": [
            {
                "lat": 17.445,
                "lon": 78.350,
                "tags": {"name": "Test Hospital"},
                "type": "node",
            }
        ]
    }
    # Mock OSRM response
    mock_client.get_route.return_value = {
        "routes": [{"duration": 300, "geometry": "abc123polyline"}]
    }

    result = service.get_nearest_resource(17.440, 78.348, "hospital")

    assert result["name"] == "Test Hospital"  # nosec
    assert result["distance_km"] > 0  # nosec
    assert result["eta_min"] == 5.0  # nosec
    assert result["route"] == "abc123polyline"  # nosec


def test_get_nearest_resource_fallback(service, mock_client):
    # Mock Overpass failure
    mock_client.search_resources.side_effect = Exception("API Down")

    # This should trigger fallback to local CSV (data/hospitals.csv)
    # Gachibowli coordinates
    result = service.get_nearest_resource(17.4401, 78.3489, "hospital")

    assert result["name"] is not None  # nosec
    assert result["distance_km"] >= 0  # nosec
    assert (
        result["eta_min"] is None
    )  # OSRM also skipped or failed during fallback  # nosec
    assert result["route"] is None  # nosec


def test_invalid_resource_type(service):
    with pytest.raises(ValueError, match="Invalid resource type"):
        service.get_nearest_resource(17.440, 78.348, "invalid_type")
