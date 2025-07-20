"""
Machine Learning Models for Weather Dashboard
Enhanced data models with ML capabilities
"""
from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict, Any, Optional
import numpy as np


@dataclass
class MLEnhancedWeatherData:
    """Weather data enhanced with ML predictions and insights"""
    
    # Basic weather data
    city: str
    temperature: float
    description: str
    humidity: int
    wind_speed: float
    pressure: float
    visibility: float
    cloudiness: int
    unit_system: str
    datetime: datetime
    
    # ML enhancements
    predicted_temperature_trend: Optional[List[float]] = None
    weather_pattern_score: Optional[float] = None
    anomaly_score: Optional[float] = None
    comfort_index: Optional[float] = None
    recommendations: Optional[List[str]] = None
    seasonal_analysis: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for ML processing"""
        return {
            'city': self.city,
            'temperature': self.temperature,
            'humidity': self.humidity,
            'wind_speed': self.wind_speed,
            'pressure': self.pressure,
            'visibility': self.visibility,
            'cloudiness': self.cloudiness,
            'datetime': self.datetime.timestamp(),
            'hour': self.datetime.hour,
            'day_of_week': self.datetime.weekday(),
            'month': self.datetime.month,
            'season': self._get_season()
        }
    
    def _get_season(self) -> int:
        """Get season from date (0=Winter, 1=Spring, 2=Summer, 3=Fall)"""
        month = self.datetime.month
        if month in [12, 1, 2]:
            return 0  # Winter
        elif month in [3, 4, 5]:
            return 1  # Spring
        elif month in [6, 7, 8]:
            return 2  # Summer
        else:
            return 3  # Fall


@dataclass
class WeatherPrediction:
    """Weather prediction model output"""
    
    city: str
    prediction_time: datetime
    predicted_temperature: float
    confidence_score: float
    trend_direction: str  # "increasing", "decreasing", "stable"
    prediction_horizon_hours: int
    
    def __str__(self):
        return f"Predicted {self.predicted_temperature:.1f}°C for {self.city} " \
               f"(confidence: {self.confidence_score:.2f})"


@dataclass
class WeatherPattern:
    """Identified weather pattern"""
    
    pattern_name: str
    description: str
    frequency: float
    typical_conditions: Dict[str, Any]
    associated_cities: List[str]
    seasonal_tendency: Optional[str] = None
    
    def __str__(self):
        return f"{self.pattern_name}: {self.description} (freq: {self.frequency:.2f})"


@dataclass
class WeatherAnomaly:
    """Detected weather anomaly"""
    
    city: str
    datetime: datetime
    anomaly_type: str
    severity_score: float  # 0-1, higher = more anomalous
    description: str
    expected_value: float
    actual_value: float
    
    def __str__(self):
        return f"Anomaly in {self.city}: {self.description} " \
               f"(severity: {self.severity_score:.2f})"


@dataclass
class PersonalizedRecommendation:
    """Personalized weather-based recommendation"""
    
    category: str  # "activity", "clothing", "travel", "health"
    recommendation: str
    confidence: float
    reasoning: str
    weather_conditions: Dict[str, Any]
    
    def __str__(self):
        return f"{self.category.title()}: {self.recommendation} " \
               f"(confidence: {self.confidence:.2f})"


@dataclass
class WeatherInsights:
    """Comprehensive weather analysis insights"""
    
    city: str
    analysis_period: str
    
    # Statistical insights
    temperature_stats: Dict[str, float]
    humidity_stats: Dict[str, float]
    wind_stats: Dict[str, float]
    
    # Trend analysis
    temperature_trend: str
    seasonal_patterns: List[WeatherPattern]
    
    # Predictions
    short_term_forecast: List[WeatherPrediction]
    long_term_trends: Dict[str, Any]
    
    # Anomalies
    detected_anomalies: List[WeatherAnomaly]
    
    # Recommendations
    personalized_recommendations: List[PersonalizedRecommendation]
    
    def get_summary(self) -> str:
        """Get a human-readable summary of insights"""
        summary = f"Weather Insights for {self.city} ({self.analysis_period}):\n"
        summary += f"• Average Temperature: {self.temperature_stats.get('mean', 0):.1f}°\n"
        summary += f"• Temperature Trend: {self.temperature_trend}\n"
        summary += f"• Detected Patterns: {len(self.seasonal_patterns)}\n"
        summary += f"• Anomalies Found: {len(self.detected_anomalies)}\n"
        summary += f"• Recommendations: {len(self.personalized_recommendations)}\n"
        return summary


class MLDataPreprocessor:
    """Preprocesses weather data for ML models"""
    
    @staticmethod
    def normalize_features(data: Dict[str, Any]) -> Dict[str, float]:
        """Normalize features for ML processing"""
        normalized = {}
        
        # Temperature normalization (assuming -50 to 50 Celsius range)
        if 'temperature' in data:
            normalized['temp_norm'] = (data['temperature'] + 50) / 100
        
        # Humidity normalization (0-100%)
        if 'humidity' in data:
            normalized['humidity_norm'] = data['humidity'] / 100
        
        # Wind speed normalization (0-50 m/s typical range)
        if 'wind_speed' in data:
            normalized['wind_norm'] = min(data['wind_speed'] / 50, 1.0)
        
        # Pressure normalization (900-1100 hPa typical range)
        if 'pressure' in data:
            normalized['pressure_norm'] = (data['pressure'] - 900) / 200
        
        # Visibility normalization (0-20 km typical range)
        if 'visibility' in data:
            normalized['visibility_norm'] = min(data['visibility'] / 20, 1.0)
        
        # Cloudiness normalization (0-100%)
        if 'cloudiness' in data:
            normalized['cloudiness_norm'] = data['cloudiness'] / 100
        
        # Time features (cyclical encoding)
        if 'hour' in data:
            normalized['hour_sin'] = np.sin(2 * np.pi * data['hour'] / 24)
            normalized['hour_cos'] = np.cos(2 * np.pi * data['hour'] / 24)
        
        if 'day_of_week' in data:
            normalized['dow_sin'] = np.sin(2 * np.pi * data['day_of_week'] / 7)
            normalized['dow_cos'] = np.cos(2 * np.pi * data['day_of_week'] / 7)
        
        if 'month' in data:
            normalized['month_sin'] = np.sin(2 * np.pi * data['month'] / 12)
            normalized['month_cos'] = np.cos(2 * np.pi * data['month'] / 12)
        
        return normalized
    
    @staticmethod
    def create_sequences(data: List[Dict], sequence_length: int = 24) -> tuple:
        """Create sequences for time series prediction"""
        sequences = []
        targets = []
        
        for i in range(len(data) - sequence_length):
            sequences.append(data[i:i + sequence_length])
            targets.append(data[i + sequence_length]['temperature'])
        
        return sequences, targets
    
    @staticmethod
    def extract_features(weather_data: MLEnhancedWeatherData) -> np.ndarray:
        """Extract feature vector from weather data"""
        data_dict = weather_data.to_dict()
        normalized = MLDataPreprocessor.normalize_features(data_dict)
        
        feature_vector = [
            normalized.get('temp_norm', 0),
            normalized.get('humidity_norm', 0),
            normalized.get('wind_norm', 0),
            normalized.get('pressure_norm', 0),
            normalized.get('visibility_norm', 0),
            normalized.get('cloudiness_norm', 0),
            normalized.get('hour_sin', 0),
            normalized.get('hour_cos', 0),
            normalized.get('dow_sin', 0),
            normalized.get('dow_cos', 0),
            normalized.get('month_sin', 0),
            normalized.get('month_cos', 0),
            data_dict.get('season', 0) / 3  # Normalize season
        ]
        
        return np.array(feature_vector)