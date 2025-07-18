"""
Weather Data Models
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class WeatherData:
    """Model for current weather data"""
    temperature: float
    description: str
    humidity: int
    wind_speed: float
    unit: str
    city: str

    @property
    def unit_label(self) -> str:
        """Get the temperature unit label"""
        return "°C" if self.unit == "metric" else "°F"

    @property
    def formatted_temperature(self) -> str:
        """Get formatted temperature with unit"""
        return f"{self.temperature}{self.unit_label}"


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
