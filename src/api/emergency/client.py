import logging
from typing import Any, Dict, cast

import requests

logger = logging.getLogger(__name__)


class EmergencyClient:
    """Client for external emergency resource and navigation services."""

    OVERPASS_URL = "https://overpass-api.de/api/interpreter"
    OSRM_URL = "https://router.project-osrm.org/route/v1/driving/"
    TIMEOUT = 10.0  # seconds

    def __init__(self) -> None:
        self.session = requests.Session()

    def search_resources(
        self, lat: float, lon: float, resource_type: str, radius: int = 5000
    ) -> Dict[str, Any]:
        """
        Search for emergency resources using Overpass API.

        Mappings:
        - hospital -> amenity=hospital
        - police -> amenity=police
        - fire_station -> amenity=fire_station
        - blood_bank -> healthcare=blood_bank
        """
        tag_map = {
            "hospital": '["amenity"="hospital"]',
            "police": '["amenity"="police"]',
            "fire_station": '["amenity"="fire_station"]',
            "blood_bank": '["healthcare"="blood_bank"]',
        }

        query_tag = tag_map.get(resource_type)
        if not query_tag:
            raise ValueError(f"Invalid resource type: {resource_type}")

        overpass_query = f"""
        [out:json][timeout:25];
        (
          node{query_tag}(around:{radius},{lat},{lon});
          way{query_tag}(around:{radius},{lat},{lon});
          relation{query_tag}(around:{radius},{lat},{lon});
        );
        out center;
        """

        try:
            response = self.session.post(
                self.OVERPASS_URL, data={"data": overpass_query}, timeout=self.TIMEOUT
            )
            response.raise_for_status()
            return cast(Dict[str, Any], response.json())
        except requests.RequestException as e:
            logger.error(f"Overpass API error: {e}")
            raise RuntimeError("Failed to fetch resources from Overpass API") from e

    def get_route(
        self, start_lat: float, start_lon: float, end_lat: float, end_lon: float
    ) -> Dict[str, Any]:
        """Fetch navigation route from OSRM."""
        coords = f"{start_lon},{start_lat};{end_lon},{end_lat}"
        url = f"{self.OSRM_URL}{coords}?overview=full&geometries=polyline"

        try:
            response = self.session.get(url, timeout=self.TIMEOUT)
            response.raise_for_status()
            return cast(Dict[str, Any], response.json())
        except requests.RequestException as e:
            logger.error(f"OSRM API error: {e}")
            raise RuntimeError("Failed to fetch route from OSRM API") from e
