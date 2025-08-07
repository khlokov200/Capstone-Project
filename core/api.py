# core/api.py
"""Weather API client module"""

import requests
import ssl
import urllib3
from typing import Dict, Optional

# Disable SSL warnings for development
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class WeatherAPI:
    """Handles all weather API communications"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"
        self.timeout = 30  # Increased timeout
        
        # Create a session with SSL configuration
        self.session = requests.Session()
        
        # Configure session for better SSL handling
        adapter = requests.adapters.HTTPAdapter(
            max_retries=requests.adapters.Retry(
                total=3,
                backoff_factor=1,
                status_forcelist=[500, 502, 503, 504]
            )
        )
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)
    
    def fetch_weather(self, city: str, unit: str = "metric") -> Optional[Dict]:
        """
        Fetch weather data for a city
        
        Args:
            city: Name of the city
            unit: "metric" for Celsius, "imperial" for Fahrenheit
            
        Returns:
            Dictionary with weather data or None if error
        """
        if not city:
            raise ValueError("City name cannot be empty")
            
        params = {
            'q': city.strip(),  # Ensure clean city name
            'appid': self.api_key,
            'units': unit
        }
        
        try:
            response = self.session.get(
                self.base_url,
                params=params,
                timeout=self.timeout,
                verify=False  # For development only
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            if response.status_code == 404:
                raise ValueError(f"City '{city}' not found")
            raise Exception(f"Weather API error: {str(e)}")
        
        # Try multiple methods to handle SSL issues
        methods = [
            self._fetch_with_session,
            self._fetch_with_verify_false,
            self._fetch_with_http
        ]
        
        for method in methods:
            try:
                result = method(params)
                if result:
                    return result
            except Exception as e:
                print(f"Method {method.__name__} failed: {e}")
                continue
        
        print("All connection methods failed")
        return None
    
    def _fetch_with_session(self, params):
        """Try with configured session"""
        response = self.session.get(self.base_url, params=params, timeout=self.timeout)
        response.raise_for_status()
        return response.json()
    
    def _fetch_with_verify_false(self, params):
        """Try with SSL verification disabled"""
        response = requests.get(
            self.base_url, 
            params=params, 
            timeout=self.timeout,
            verify=False
        )
        response.raise_for_status()
        return response.json()
    
    def _fetch_with_http(self, params):
        """Try with HTTP instead of HTTPS as fallback"""
        http_url = self.base_url.replace("https://", "http://")
        response = requests.get(http_url, params=params, timeout=self.timeout)
        response.raise_for_status()
        return response.json()