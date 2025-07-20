"""
ML Service - Handles machine learning predictions and analysis
"""
import os
import csv
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
from models.ml_models import (
    MLEnhancedWeatherData, WeatherPrediction, WeatherPattern, 
    WeatherAnomaly, PersonalizedRecommendation, WeatherInsights,
    MLDataPreprocessor
)


class MLService:
    """Machine Learning service for weather predictions and insights"""
    
    def __init__(self, log_file="data/weather_log.csv"):
        self.log_file = log_file
        self.preprocessor = MLDataPreprocessor()
        self._ensure_data_dir()
    
    def _ensure_data_dir(self):
        """Ensure data directory exists"""
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
    
    def load_historical_data(self, limit: int = 100) -> List[Dict]:
        """Load historical weather data from CSV"""
        try:
            if not os.path.exists(self.log_file):
                return []
            
            with open(self.log_file, "r") as file:
                reader = list(csv.DictReader(file))
                return reader[-limit:] if reader else []
        except Exception as e:
            print(f"Error loading historical data: {e}")
            return []
    
    def predict_temperature(self, city: str, hours_ahead: int = 24) -> WeatherPrediction:
        """Predict temperature using simple trend analysis"""
        historical_data = self.load_historical_data(limit=50)
        
        if len(historical_data) < 3:
            # Not enough data for prediction
            return WeatherPrediction(
                city=city,
                predicted_temperature=20.0,
                confidence_score=0.3,
                prediction_time=datetime.now() + timedelta(hours=hours_ahead),
                trend_direction="unknown",
                prediction_horizon_hours=hours_ahead
            )
        
        # Extract temperatures for the city
        city_temps = []
        for record in historical_data:
            if record.get("City", "").lower() == city.lower():
                try:
                    temp = float(record.get("Temperature", 0))
                    city_temps.append(temp)
                except (ValueError, TypeError):
                    continue
        
        if len(city_temps) < 2:
            # Use global average if no city-specific data
            city_temps = [float(record.get("Temperature", 20)) for record in historical_data[-10:]]
        
        # Simple trend-based prediction
        recent_temps = city_temps[-5:]  # Last 5 readings
        avg_temp = np.mean(recent_temps)
        temp_trend = np.mean(np.diff(recent_temps)) if len(recent_temps) > 1 else 0
        
        # Predict based on trend
        predicted_temp = avg_temp + (temp_trend * (hours_ahead / 24))
        
        # Calculate confidence based on data consistency
        temp_variance = np.var(recent_temps) if len(recent_temps) > 1 else 10
        confidence = max(0.4, min(0.9, 1 / (1 + temp_variance / 10)))
        
        return WeatherPrediction(
            city=city,
            predicted_temperature=round(predicted_temp, 1),
            confidence_score=confidence,
            prediction_time=datetime.now() + timedelta(hours=hours_ahead),
            trend_direction="stable",
            prediction_horizon_hours=hours_ahead
        )
    
    def detect_weather_patterns(self, city: str) -> List[WeatherPattern]:
        """Detect recurring weather patterns"""
        historical_data = self.load_historical_data(limit=100)
        patterns = []
        
        # Group data by city
        city_data = [record for record in historical_data 
                    if record.get("City", "").lower() == city.lower()]
        
        if len(city_data) < 10:
            return patterns
        
        # Analyze temperature patterns
        temperatures = []
        descriptions = []
        
        for record in city_data:
            try:
                temp = float(record.get("Temperature", 0))
                desc = record.get("Description", "").lower()
                temperatures.append(temp)
                descriptions.append(desc)
            except (ValueError, TypeError):
                continue
        
        if temperatures:
            # Temperature trend pattern
            avg_temp = np.mean(temperatures)
            temp_std = np.std(temperatures)
            
            if temp_std < 3:
                pattern_type = "stable_temperature"
                description = f"Temperature remains stable around {avg_temp:.1f}°C"
                confidence = 0.8
            elif temp_std > 8:
                pattern_type = "variable_temperature"
                description = f"Highly variable temperatures (±{temp_std:.1f}°C)"
                confidence = 0.7
            else:
                pattern_type = "moderate_variation"
                description = f"Moderate temperature variation around {avg_temp:.1f}°C"
                confidence = 0.6
            
            patterns.append(WeatherPattern(
                pattern_name=pattern_type,
                description=description,
                frequency=len(city_data),
                typical_conditions={"temperature_std": temp_std},
                associated_cities=[city]
            ))
        
        # Weather condition patterns
        if descriptions:
            from collections import Counter
            desc_counts = Counter(descriptions)
            most_common = desc_counts.most_common(3)
            
            for desc, count in most_common:
                if count >= 3:  # At least 3 occurrences
                    frequency = count / len(descriptions)
                    patterns.append(WeatherPattern(
                        pattern_name="weather_condition",
                        description=f"Frequent {desc} weather ({count} times)",
                        frequency=frequency,
                        typical_conditions={"weather_type": desc},
                        associated_cities=[city]
                    ))
        
        return patterns
    
    def detect_anomalies(self, city: str) -> List[WeatherAnomaly]:
        """Detect weather anomalies"""
        historical_data = self.load_historical_data(limit=50)
        anomalies = []
        
        city_data = [record for record in historical_data 
                    if record.get("City", "").lower() == city.lower()]
        
        if len(city_data) < 5:
            return anomalies
        
        temperatures = []
        for record in city_data:
            try:
                temp = float(record.get("Temperature", 0))
                temperatures.append((temp, record))
            except (ValueError, TypeError):
                continue
        
        if len(temperatures) < 5:
            return anomalies
        
        # Calculate temperature statistics
        temps_only = [t[0] for t in temperatures]
        mean_temp = np.mean(temps_only)
        std_temp = np.std(temps_only)
        
        # Detect temperature anomalies (outside 2 standard deviations)
        for temp, record in temperatures[-10:]:  # Check last 10 readings
            z_score = abs(temp - mean_temp) / (std_temp + 1e-6)  # Avoid division by zero
            
            if z_score > 2:  # Significant anomaly
                anomaly_type = "extreme_hot" if temp > mean_temp else "extreme_cold"
                severity = min(1.0, z_score / 3)
                
                anomalies.append(WeatherAnomaly(
                    city=city,
                    datetime=datetime.now(),
                    anomaly_type=anomaly_type,
                    severity_score=severity,
                    description=f"Temperature {temp}°C is {z_score:.1f} standard deviations from normal ({mean_temp:.1f}°C)",
                    expected_value=mean_temp,
                    actual_value=temp
                ))
        
        return anomalies
    
    def generate_personalized_recommendations(self, city: str, user_preferences: Dict = None) -> List[PersonalizedRecommendation]:
        """Generate personalized weather-based recommendations"""
        recommendations = []
        historical_data = self.load_historical_data(limit=20)
        
        # Get latest weather for the city
        latest_weather = None
        for record in reversed(historical_data):
            if record.get("City", "").lower() == city.lower():
                latest_weather = record
                break
        
        if not latest_weather:
            return recommendations
        
        try:
            temp = float(latest_weather.get("Temperature", 20))
            description = latest_weather.get("Description", "").lower()
            humidity = float(latest_weather.get("Humidity", 50)) if latest_weather.get("Humidity") else 50
        except (ValueError, TypeError):
            return recommendations
        
        # Temperature-based recommendations
        if temp < 5:
            recommendations.append(PersonalizedRecommendation(
                category="clothing",
                recommendation="Wear warm winter clothing and layers",
                confidence=0.9,
                reasoning=f"Very cold temperature: {temp}°C",
                weather_conditions={"temperature": temp, "description": description}
            ))
        elif temp < 15:
            recommendations.append(PersonalizedRecommendation(
                category="clothing",
                recommendation="Wear a jacket or sweater",
                confidence=0.8,
                reasoning=f"Cool temperature: {temp}°C",
                weather_conditions={"temperature": temp, "description": description}
            ))
        elif temp > 30:
            recommendations.append(PersonalizedRecommendation(
                category="clothing",
                recommendation="Wear light, breathable clothing",
                confidence=0.9,
                reasoning=f"Hot temperature: {temp}°C",
                weather_conditions={"temperature": temp, "description": description}
            ))
        
        # Weather condition recommendations
        if "rain" in description:
            recommendations.append(PersonalizedRecommendation(
                category="activity",
                recommendation="Plan indoor activities or bring an umbrella",
                confidence=0.8,
                reasoning="Rainy weather conditions",
                weather_conditions={"temperature": temp, "description": description}
            ))
        elif "clear" in description or "sun" in description:
            recommendations.append(PersonalizedRecommendation(
                category="activity",
                recommendation="Great day for outdoor activities",
                confidence=0.9,
                reasoning="Clear, sunny weather",
                weather_conditions={"temperature": temp, "description": description}
            ))
        
        # Humidity-based recommendations
        if humidity > 80:
            recommendations.append(PersonalizedRecommendation(
                category="comfort",
                recommendation="Stay hydrated and find air-conditioned spaces",
                confidence=0.7,
                reasoning=f"High humidity: {humidity}%",
                weather_conditions={"temperature": temp, "humidity": humidity}
            ))
        
        return recommendations
    
    def generate_weather_insights(self, city: str) -> WeatherInsights:
        """Generate comprehensive weather insights"""
        historical_data = self.load_historical_data(limit=100)
        city_data = [record for record in historical_data 
                    if record.get("City", "").lower() == city.lower()]
        
        if not city_data:
            return WeatherInsights(
                city=city,
                analysis_period="last 100 records",
                temperature_stats={"mean": 0, "min": 0, "max": 0},
                humidity_stats={"mean": 0, "min": 0, "max": 0},
                wind_stats={"mean": 0, "min": 0, "max": 0},
                temperature_trend="insufficient data",
                seasonal_patterns=[],
                short_term_forecast=[],
                long_term_trends={},
                detected_anomalies=[],
                personalized_recommendations=[]
            )
        
        # Calculate statistics
        temperatures = []
        humidities = []
        wind_speeds = []
        
        for record in city_data:
            try:
                temp = float(record.get("Temperature", 0))
                temperatures.append(temp)
                
                if record.get("Humidity"):
                    humidity = float(record.get("Humidity", 50))
                    humidities.append(humidity)
                
                if record.get("WindSpeed"):
                    wind = float(record.get("WindSpeed", 0))
                    wind_speeds.append(wind)
            except (ValueError, TypeError):
                continue
        
        # Temperature statistics
        temp_stats = {}
        if temperatures:
            temp_stats = {
                "mean": np.mean(temperatures),
                "min": min(temperatures),
                "max": max(temperatures),
                "std": np.std(temperatures)
            }
        
        # Humidity statistics
        humidity_stats = {}
        if humidities:
            humidity_stats = {
                "mean": np.mean(humidities),
                "min": min(humidities),
                "max": max(humidities)
            }
        
        # Wind statistics
        wind_stats = {}
        if wind_speeds:
            wind_stats = {
                "mean": np.mean(wind_speeds),
                "min": min(wind_speeds),
                "max": max(wind_speeds)
            }
        
        # Determine temperature trend
        if len(temperatures) >= 3:
            recent_avg = np.mean(temperatures[-5:])
            overall_avg = np.mean(temperatures)
            
            if recent_avg > overall_avg + 2:
                temp_trend = "warming"
            elif recent_avg < overall_avg - 2:
                temp_trend = "cooling"
            else:
                temp_trend = "stable"
        else:
            temp_trend = "insufficient data"
        
        return WeatherInsights(
            city=city,
            analysis_period=f"last {len(city_data)} records",
            temperature_stats=temp_stats,
            humidity_stats=humidity_stats,
            wind_stats=wind_stats,
            temperature_trend=temp_trend,
            seasonal_patterns=self.detect_weather_patterns(city),
            short_term_forecast=[self.predict_temperature(city, 24)],
            long_term_trends={"trend": temp_trend},
            detected_anomalies=self.detect_anomalies(city),
            personalized_recommendations=self.generate_personalized_recommendations(city)
        )
    
    def enhance_weather_data(self, weather_data: Dict) -> MLEnhancedWeatherData:
        """Enhance basic weather data with ML predictions and insights"""
        city = weather_data.get("city", "Unknown")
        
        # Generate ML enhancements
        prediction = self.predict_temperature(city, hours_ahead=24)
        patterns = self.detect_weather_patterns(city)
        anomalies = self.detect_anomalies(city)
        recommendations = self.generate_personalized_recommendations(city)
        insights = self.generate_weather_insights(city)
        
        # Create enhanced weather data with all required fields
        enhanced_data = MLEnhancedWeatherData(
            city=city,
            temperature=weather_data.get("temperature", 20.0),
            description=weather_data.get("description", "Unknown"),
            humidity=int(weather_data.get("humidity", 50)),
            wind_speed=weather_data.get("wind_speed", 0.0),
            pressure=weather_data.get("pressure", 1013.25),
            visibility=weather_data.get("visibility", 10.0),
            cloudiness=int(weather_data.get("cloudiness", 0)),
            unit_system=weather_data.get("unit", "metric"),
            datetime=datetime.now(),
            # ML enhancements
            predicted_temperature_trend=[prediction.predicted_temperature],
            weather_pattern_score=0.7,  # Calculate based on patterns
            anomaly_score=max([a.severity_score for a in anomalies], default=0.0),
            comfort_index=self._calculate_comfort_index(weather_data),
            recommendations=[rec.recommendation for rec in recommendations],
            seasonal_analysis={"season": self._get_current_season()}
        )
        
        return enhanced_data
    
    def _calculate_comfort_index(self, weather_data: Dict) -> float:
        """Calculate a simple comfort index based on temperature and humidity"""
        temp = weather_data.get("temperature", 20)
        humidity = weather_data.get("humidity", 50)
        
        # Simple comfort calculation (0-1 scale)
        temp_comfort = 1.0 - abs(temp - 22) / 30  # Optimal around 22°C
        humidity_comfort = 1.0 - abs(humidity - 45) / 55  # Optimal around 45%
        
        return max(0.0, min(1.0, (temp_comfort + humidity_comfort) / 2))
    
    def _get_current_season(self) -> str:
        """Get current season"""
        month = datetime.now().month
        if month in [12, 1, 2]:
            return "winter"
        elif month in [3, 4, 5]:
            return "spring"
        elif month in [6, 7, 8]:
            return "summer"
        else:
            return "fall"