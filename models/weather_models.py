"""
Weather Data Models
"""
from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class WeatherData:
    """Model for current weather data"""
    temperature: float
    description: str
    humidity: int
    wind_speed: float
    unit: str
    city: str
    # New weather elements
    visibility: Optional[int] = None  # in meters
    cloudiness: Optional[int] = None  # percentage
    sunrise: Optional[int] = None     # unix timestamp
    sunset: Optional[int] = None      # unix timestamp
    pressure: Optional[int] = None    # hPa
    wind_direction: Optional[int] = None  # degrees
    feels_like: Optional[float] = None    # temperature
    rain_1h: Optional[float] = None       # mm in last hour
    rain_3h: Optional[float] = None       # mm in last 3 hours
    snow_1h: Optional[float] = None       # mm in last hour
    snow_3h: Optional[float] = None       # mm in last 3 hours

    @property
    def unit_label(self) -> str:
        """Get the temperature unit label"""
        return "°C" if self.unit == "metric" else "°F"

    @property
    def formatted_temperature(self) -> str:
        """Get formatted temperature with unit"""
        return f"{self.temperature}{self.unit_label}"
    
    @property
    def formatted_feels_like(self) -> str:
        """Get formatted feels like temperature"""
        if self.feels_like is not None:
            return f"{self.feels_like}{self.unit_label}"
        return "N/A"
    
    @property
    def formatted_visibility(self) -> str:
        """Get formatted visibility"""
        if self.visibility is not None:
            return f"{self.visibility / 1000:.1f} km"
        return "N/A"
    
    @property
    def formatted_cloudiness(self) -> str:
        """Get formatted cloudiness"""
        if self.cloudiness is not None:
            return f"{self.cloudiness}%"
        return "N/A"
    
    @property
    def formatted_sunrise(self) -> str:
        """Get formatted sunrise time"""
        if self.sunrise is not None:
            return datetime.fromtimestamp(self.sunrise).strftime("%H:%M")
        return "N/A"
    
    @property
    def formatted_sunset(self) -> str:
        """Get formatted sunset time"""
        if self.sunset is not None:
            return datetime.fromtimestamp(self.sunset).strftime("%H:%M")
        return "N/A"
    
    @property
    def formatted_wind(self) -> str:
        """Get formatted wind information"""
        wind_info = f"{self.wind_speed}"
        if self.unit == "metric":
            wind_info += " m/s"
        else:
            wind_info += " mph"
        
        if self.wind_direction is not None:
            directions = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
                         "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
            direction_idx = int((self.wind_direction + 11.25) / 22.5) % 16
            wind_info += f" {directions[direction_idx]}"
        
        return wind_info
    
    @property
    def formatted_precipitation(self) -> str:
        """Get formatted precipitation info"""
        precip_info = []
        
        if self.rain_1h is not None and self.rain_1h > 0:
            precip_info.append(f"Rain: {self.rain_1h}mm/h")
        elif self.rain_3h is not None and self.rain_3h > 0:
            precip_info.append(f"Rain: {self.rain_3h/3:.1f}mm/h")
        
        if self.snow_1h is not None and self.snow_1h > 0:
            precip_info.append(f"Snow: {self.snow_1h}mm/h")
        elif self.snow_3h is not None and self.snow_3h > 0:
            precip_info.append(f"Snow: {self.snow_3h/3:.1f}mm/h")
        
        return ", ".join(precip_info) if precip_info else "None"
    
    @property
    def has_fog(self) -> bool:
        """Check if there's fog based on visibility"""
        if self.visibility is not None:
            return self.visibility < 1000  # Less than 1km visibility indicates fog
        return False
    
    @property
    def formatted_fog(self) -> str:
        """Get fog status"""
        return "Yes" if self.has_fog else "No"


@dataclass
class ForecastData:
    """Model for forecast data"""
    datetime: str
    temperature: float
    description: str
    unit: str

    @property
    def unit_label(self) -> str:
        return "°C" if self.unit == "metric" else "°F"


@dataclass
class JournalEntry:
    """Model for journal entries"""
    text: str
    mood: str
    datetime: Optional[str] = None


@dataclass
class ActivitySuggestion:
    """Model for activity suggestions"""
    suggestion: str
    weather_description: str
