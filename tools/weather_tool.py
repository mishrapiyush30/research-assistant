"""Weather Tool for the Research Assistant Agent."""

from typing import Dict, Any, Optional
import requests
from langchain.tools import BaseTool


class WeatherTool(BaseTool):
    """Tool for retrieving current weather information."""
    
    name: str = "WeatherTool"
    description: str = """
    Useful for getting current weather conditions for a specific location.
    Input should be a city name or location (e.g., "New York", "Paris, France").
    Use this when you need real-time weather information.
    """
    
    def _get_coordinates(self, location: str) -> tuple:
        """Get latitude and longitude for a location using Open-Meteo Geocoding API."""
        url = f"https://geocoding-api.open-meteo.com/v1/search?name={location}&count=1&language=en&format=json"
        response = requests.get(url)
        data = response.json()
        
        if "results" not in data or not data["results"]:
            raise ValueError(f"Could not find location: {location}")
        
        result = data["results"][0]
        return result["latitude"], result["longitude"], result["name"], result.get("country", "")
    
    def _get_weather(self, lat: float, lon: float) -> Dict[str, Any]:
        """Get current weather for given coordinates using Open-Meteo API."""
        url = (
            f"https://api.open-meteo.com/v1/forecast"
            f"?latitude={lat}&longitude={lon}"
            f"&current=temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,wind_speed_10m,wind_direction_10m"
            f"&temperature_unit=celsius"
            f"&wind_speed_unit=kmh"
            f"&precipitation_unit=mm"
        )
        response = requests.get(url)
        return response.json()
    
    def _run(self, location: str) -> str:
        """Run the tool with the provided location."""
        try:
            # Get coordinates for the location
            lat, lon, name, country = self._get_coordinates(location)
            
            # Get current weather
            weather_data = self._get_weather(lat, lon)
            current = weather_data.get("current", {})
            
            # Format the response
            location_str = f"{name}, {country}" if country else name
            
            result = f"Current weather for {location_str}:\n\n"
            result += f"Temperature: {current.get('temperature_2m', 'N/A')}°C\n"
            result += f"Feels like: {current.get('apparent_temperature', 'N/A')}°C\n"
            result += f"Humidity: {current.get('relative_humidity_2m', 'N/A')}%\n"
            result += f"Precipitation: {current.get('precipitation', 'N/A')} mm\n"
            result += f"Wind: {current.get('wind_speed_10m', 'N/A')} km/h\n"
            result += f"Wind direction: {current.get('wind_direction_10m', 'N/A')}°\n"
            
            return result
            
        except Exception as e:
            return f"Error retrieving weather information: {str(e)}"
    
    async def _arun(self, location: str) -> str:
        """Run the tool asynchronously."""
        # For simplicity, we'll just call the synchronous version
        return self._run(location) 