import os
import pandas as pd
import pytest

def test_data_files_exist():
    """Check if all required CSV files exist in the data directory."""
    data_files = [
        "data/hospitals.csv",
        "data/bloodbanks.csv",
        "data/policestations.csv",
        "data/firestations.csv"
    ]
    for file_path in data_files:
        assert os.path.exists(file_path), f"{file_path} is missing"

def test_csv_structure():
    """Verify that CSV files have the correct column structure."""
    expected_columns = ["Name", "Area", "Contact", "Latitude", "Longitude"]
    data_files = [
        "data/hospitals.csv",
        "data/bloodbanks.csv",
        "data/policestations.csv",
        "data/firestations.csv"
    ]
    
    for file_path in data_files:
        df = pd.read_csv(file_path)
        assert all(col in df.columns for col in expected_columns), f"Incorrect columns in {file_path}"

def test_area_consistency():
    """Ensure that the 'Area' column contains expected locations."""
    valid_areas = ["Gachibowli", "Madhapur", "Kukatpally", "Ameerpet", "Secunderabad"]
    df = pd.read_csv("data/hospitals.csv")
    
    # Check if at least one record matches our expected locations
    areas_found = df["Area"].unique()
    assert any(area in valid_areas for area in areas_found), "No valid areas found in hospitals.csv"

def test_latitude_longitude_ranges():
    """Validate that coordinates are within realistic ranges for Hyderabad."""
    # Hyderabad approx range: Lat 17.2-17.6, Lon 78.2-78.6
    data_files = [
        "data/hospitals.csv",
        "data/bloodbanks.csv",
        "data/policestations.csv",
        "data/firestations.csv"
    ]
    
    for file_path in data_files:
        df = pd.read_csv(file_path)
        assert df["Latitude"].between(17.0, 18.0).all(), f"Invalid latitude in {file_path}"
        assert df["Longitude"].between(78.0, 79.0).all(), f"Invalid longitude in {file_path}"
