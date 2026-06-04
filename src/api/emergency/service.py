import math
import os
from typing import Any, Dict, List, Optional, cast

import pandas as pd

from .client import EmergencyClient


class EmergencyService:
    """Service to handle emergency resource selection and navigation logic."""

    def __init__(self, client: Optional[EmergencyClient] = None) -> None:
        self.client = client or EmergencyClient()
        self.data_path = "data"

    @staticmethod
    def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calculate the great circle distance between two points on the earth in km."""
        R = 6371  # Radius of earth in km
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = (
            math.sin(dlat / 2) ** 2
            + math.cos(math.radians(lat1))
            * math.cos(math.radians(lat2))
            * math.sin(dlon / 2) ** 2
        )
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c

    def get_nearest_resource(
        self, lat: float, lon: float, resource_type: str
    ) -> Dict[str, Any]:
        """Find the nearest resource and get navigation details."""
        try:
            data = self.client.search_resources(lat, lon, resource_type)
            elements = data.get("elements", [])

            if not elements:
                return self._fallback_to_local(lat, lon, resource_type)

            nearest = self._process_elements(lat, lon, resource_type, elements)
        except Exception:
            # Fallback to local data if API fails
            return self._fallback_to_local(lat, lon, resource_type)

        # Get navigation details
        try:
            route_data = self.client.get_route(
                lat, lon, nearest["location"]["lat"], nearest["location"]["lon"]
            )

            routes = route_data.get("routes", [])
            if routes:
                nearest["eta_min"] = round(routes[0].get("duration", 0) / 60, 1)
                nearest["route"] = routes[0].get("geometry", "")
            else:
                nearest["eta_min"] = None
                nearest["route"] = None
        except Exception:
            nearest["eta_min"] = None
            nearest["route"] = None

        return nearest

    def _process_elements(
        self, lat: float, lon: float, resource_type: str, elements: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        nearest = None
        min_dist = float("inf")

        for element in elements:
            e_lat = element.get("lat") or element.get("center", {}).get("lat")
            e_lon = element.get("lon") or element.get("center", {}).get("lon")

            if e_lat is None or e_lon is None:
                continue

            dist = self.haversine(lat, lon, e_lat, e_lon)
            if dist < min_dist:
                min_dist = dist
                nearest = {
                    "type": resource_type,
                    "name": element.get("tags", {}).get("name", "Unknown"),
                    "location": {"lat": e_lat, "lon": e_lon},
                    "distance_km": round(dist, 2),
                }

        if not nearest:
            raise ValueError(f"Could not determine location for any {resource_type}")
        return nearest

    def _fallback_to_local(
        self, lat: float, lon: float, resource_type: str
    ) -> Dict[str, Any]:
        """Search in local CSV files if remote API is unavailable."""
        file_map = {
            "hospital": "hospitals.csv",
            "blood_bank": "bloodbanks.csv",
            "police": "policestations.csv",
            "fire_station": "firestations.csv",
        }

        filename = file_map.get(resource_type)
        if not filename:
            raise ValueError(
                f"Invalid resource type for local fallback: {resource_type}"
            )

        file_path = os.path.join(self.data_path, filename)
        if not os.path.exists(file_path):
            raise ValueError(f"Local data file not found: {file_path}")

        df = pd.read_csv(file_path)
        df["distance"] = df.apply(
            lambda row: self.haversine(
                lat, lon, float(row["Latitude"]), float(row["Longitude"])
            ),
            axis=1,
        )

        nearest_idx = df["distance"].idxmin()
        nearest_row = df.loc[nearest_idx]

        return {
            "type": resource_type,
            "name": str(nearest_row["Name"]),
            "location": {
                "lat": float(cast(Any, nearest_row["Latitude"])),
                "lon": float(cast(Any, nearest_row["Longitude"])),
            },
            "distance_km": round(float(cast(Any, nearest_row["distance"])), 2),
            "eta_min": None,
            "route": None,
        }
