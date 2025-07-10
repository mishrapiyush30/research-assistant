"""Tests for the WeatherTool."""

import pytest
from unittest.mock import patch, MagicMock

import sys
import os

# Add the parent directory to the path so we can import the tools
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tools import WeatherTool


class TestWeatherTool:
    """Test suite for the WeatherTool."""
    
    def test_init(self):
        """Test that the tool can be initialized."""
        tool = WeatherTool()
        assert tool.name == "WeatherTool"
        assert "weather" in tool.description
    
    @patch('requests.get')
    def test_get_coordinates(self, mock_get):
        """Test the _get_coordinates method."""
        # Mock the response for geocoding API
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "results": [
                {
                    "name": "New York",
                    "country": "United States",
                    "latitude": 40.7128,
                    "longitude": -74.0060
                }
            ]
        }
        mock_get.return_value = mock_response
        
        # Create the tool and call the method
        tool = WeatherTool()
        lat, lon, name, country = tool._get_coordinates("New York")
        
        # Check the results
        assert lat == 40.7128
        assert lon == -74.0060
        assert name == "New York"
        assert country == "United States"
        
        # Verify the mock was called correctly
        mock_get.assert_called_once()
        assert "geocoding-api.open-meteo.com" in mock_get.call_args[0][0]
        assert "New York" in mock_get.call_args[0][0]
    
    @patch('requests.get')
    def test_get_coordinates_no_results(self, mock_get):
        """Test the _get_coordinates method with no results."""
        # Mock the response for geocoding API with no results
        mock_response = MagicMock()
        mock_response.json.return_value = {"results": []}
        mock_get.return_value = mock_response
        
        # Create the tool and call the method
        tool = WeatherTool()
        
        # Check that the method raises a ValueError
        with pytest.raises(ValueError) as excinfo:
            tool._get_coordinates("NonexistentLocation12345")
        
        assert "Could not find location" in str(excinfo.value)
        
        # Verify the mock was called correctly
        mock_get.assert_called_once()
    
    @patch('requests.get')
    def test_get_weather(self, mock_get):
        """Test the _get_weather method."""
        # Mock the response for weather API
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "current": {
                "temperature_2m": 22.5,
                "relative_humidity_2m": 65,
                "apparent_temperature": 23.1,
                "precipitation": 0.0,
                "wind_speed_10m": 10.2,
                "wind_direction_10m": 180
            }
        }
        mock_get.return_value = mock_response
        
        # Create the tool and call the method
        tool = WeatherTool()
        result = tool._get_weather(40.7128, -74.0060)
        
        # Check the results
        assert result["current"]["temperature_2m"] == 22.5
        assert result["current"]["wind_speed_10m"] == 10.2
        
        # Verify the mock was called correctly
        mock_get.assert_called_once()
        assert "api.open-meteo.com" in mock_get.call_args[0][0]
        assert "latitude=40.7128" in mock_get.call_args[0][0]
        assert "longitude=-74.006" in mock_get.call_args[0][0]
    
    @patch.object(WeatherTool, '_get_coordinates')
    @patch.object(WeatherTool, '_get_weather')
    def test_run_success(self, mock_get_weather, mock_get_coordinates):
        """Test successful execution of the tool."""
        # Mock the _get_coordinates method
        mock_get_coordinates.return_value = (40.7128, -74.0060, "New York", "United States")
        
        # Mock the _get_weather method
        mock_get_weather.return_value = {
            "current": {
                "temperature_2m": 22.5,
                "relative_humidity_2m": 65,
                "apparent_temperature": 23.1,
                "precipitation": 0.0,
                "wind_speed_10m": 10.2,
                "wind_direction_10m": 180
            }
        }
        
        # Create the tool and run it
        tool = WeatherTool()
        result = tool._run("New York")
        
        # Check the result
        assert "Current weather for New York, United States" in result
        assert "Temperature: 22.5°C" in result
        assert "Humidity: 65%" in result
        assert "Wind: 10.2 km/h" in result
        
        # Verify the mocks were called correctly
        mock_get_coordinates.assert_called_once_with("New York")
        mock_get_weather.assert_called_once_with(40.7128, -74.0060) 