"""
ML Controller - Coordinates machine learning operations and integrates with UI
"""
from datetime import datetime
from typing import Dict, List, Optional
from services.ml_service import MLService
from models.ml_models import (
    MLEnhancedWeatherData, WeatherPrediction, WeatherPattern,
    WeatherAnomaly, PersonalizedRecommendation, WeatherInsights
)


class MLController:
    """Controller for machine learning features in the weather dashboard"""
    
    def __init__(self, log_file="data/weather_log.csv"):
        self.ml_service = MLService(log_file)
    
    def get_ml_enhanced_weather(self, weather_data: Dict) -> MLEnhancedWeatherData:
        """Get ML-enhanced weather data with predictions and insights"""
        try:
            return self.ml_service.enhance_weather_data(weather_data)
        except Exception as e:
            print(f"Error generating ML enhancements: {e}")
            # Return basic enhancement on error - create a simple MLEnhancedWeatherData
            city = weather_data.get("city", "Unknown")
            return MLEnhancedWeatherData(
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
                predicted_temperature_trend=[20.0],
                weather_pattern_score=0.5,
                anomaly_score=0.0,
                comfort_index=0.5,
                recommendations=["ML analysis unavailable"],
                seasonal_analysis={"season": "unknown"}
            )
    
    def get_temperature_prediction(self, city: str, hours_ahead: int = 24) -> WeatherPrediction:
        """Get temperature prediction for a specific city"""
        try:
            return self.ml_service.predict_temperature(city, hours_ahead)
        except Exception as e:
            print(f"Error predicting temperature: {e}")
            return WeatherPrediction(
                city=city,
                predicted_temperature=20.0,
                confidence_score=0.3,
                prediction_time=datetime.now(),
                trend_direction="unknown",
                prediction_horizon_hours=hours_ahead
            )
    
    def get_weather_patterns(self, city: str) -> List[WeatherPattern]:
        """Get detected weather patterns for a city"""
        try:
            return self.ml_service.detect_weather_patterns(city)
        except Exception as e:
            print(f"Error detecting patterns: {e}")
            return []
    
    def get_weather_anomalies(self, city: str) -> List[WeatherAnomaly]:
        """Get detected weather anomalies for a city"""
        try:
            return self.ml_service.detect_anomalies(city)
        except Exception as e:
            print(f"Error detecting anomalies: {e}")
            return []
    
    def get_personalized_recommendations(self, city: str, user_preferences: Dict = None) -> List[PersonalizedRecommendation]:
        """Get personalized recommendations based on weather"""
        try:
            return self.ml_service.generate_personalized_recommendations(city, user_preferences)
        except Exception as e:
            print(f"Error generating recommendations: {e}")
            return []
    
    def get_weather_insights(self, city: str) -> WeatherInsights:
        """Get comprehensive weather insights for a city"""
        try:
            return self.ml_service.generate_weather_insights(city)
        except Exception as e:
            print(f"Error generating insights: {e}")
            return WeatherInsights(
                city=city,
                analysis_period="error",
                temperature_stats={},
                humidity_stats={},
                wind_stats={},
                temperature_trend="unknown",
                seasonal_patterns=[],
                short_term_forecast=[],
                long_term_trends={},
                detected_anomalies=[],
                personalized_recommendations=[]
            )
    
    def format_prediction_for_display(self, prediction: WeatherPrediction) -> str:
        """Format temperature prediction for UI display"""
        confidence_pct = int(prediction.confidence_score * 100)
        time_str = prediction.prediction_time.strftime("%H:%M") if prediction.prediction_time else "N/A"
        
        return (f"🔮 Predicted Temperature: {prediction.predicted_temperature}°C\n"
                f"⏰ For: {time_str}\n"
                f"📊 Confidence: {confidence_pct}%\n"
                f"📈 Trend: {prediction.trend_direction}")
    
    def format_patterns_for_display(self, patterns: List[WeatherPattern]) -> str:
        """Format weather patterns for UI display"""
        if not patterns:
            return "📈 No significant patterns detected"
        
        formatted_patterns = []
        for pattern in patterns[:3]:  # Show top 3 patterns
            formatted_patterns.append(
                f"🔍 {pattern.pattern_name.replace('_', ' ').title()}\n"
                f"   {pattern.description}"
            )
        
        return "\n\n".join(formatted_patterns)
    
    def format_anomalies_for_display(self, anomalies: List[WeatherAnomaly]) -> str:
        """Format weather anomalies for UI display"""
        if not anomalies:
            return "✅ No weather anomalies detected"
        
        formatted_anomalies = []
        for anomaly in anomalies[:3]:  # Show top 3 anomalies
            severity_pct = int(anomaly.severity_score * 100)
            icon = "🔥" if "hot" in anomaly.anomaly_type else "🥶"
            formatted_anomalies.append(
                f"{icon} {anomaly.anomaly_type.replace('_', ' ').title()}\n"
                f"   {anomaly.description}\n"
                f"   Severity: {severity_pct}%"
            )
        
        return "\n\n".join(formatted_anomalies)
    
    def format_recommendations_for_display(self, recommendations: List[PersonalizedRecommendation]) -> str:
        """Format personalized recommendations for UI display"""
        if not recommendations:
            return "💡 No specific recommendations at this time"
        
        category_icons = {
            "clothing": "👔",
            "activity": "🎯",
            "comfort": "🏠",
            "health": "💊",
            "transportation": "🚗"
        }
        
        formatted_recs = []
        for rec in recommendations[:4]:  # Show top 4 recommendations
            icon = category_icons.get(rec.category, "💡")
            confidence_pct = int(rec.confidence * 100)
            formatted_recs.append(
                f"{icon} {rec.recommendation}\n"
                f"   Reason: {rec.reasoning} ({confidence_pct}% confidence)"
            )
        
        return "\n\n".join(formatted_recs)
    
    def format_insights_for_display(self, insights: WeatherInsights) -> str:
        """Format weather insights for UI display"""
        result = f"📊 Weather Insights for {insights.city}\n"
        result += f"Analysis Period: {insights.analysis_period}\n\n"
        
        if insights.temperature_stats:
            result += f"🌡️ Temperature Stats:\n"
            result += f"   Average: {insights.temperature_stats.get('mean', 0):.1f}°C\n"
            result += f"   Range: {insights.temperature_stats.get('min', 0):.1f}°C to {insights.temperature_stats.get('max', 0):.1f}°C\n"
            result += f"   Trend: {insights.temperature_trend}\n\n"
        
        if insights.detected_anomalies:
            result += f"⚠️ Anomalies: {len(insights.detected_anomalies)} detected\n"
        
        if insights.personalized_recommendations:
            result += f"💡 Recommendations: {len(insights.personalized_recommendations)} available\n"
        
        return result
    
    def get_ml_summary_for_city(self, city: str) -> str:
        """Get a comprehensive ML summary for a city"""
        try:
            prediction = self.get_temperature_prediction(city)
            patterns = self.get_weather_patterns(city)
            anomalies = self.get_weather_anomalies(city)
            recommendations = self.get_personalized_recommendations(city)
            
            summary = f"🤖 ML Analysis for {city.title()}\n"
            summary += "=" * 40 + "\n\n"
            
            summary += self.format_prediction_for_display(prediction) + "\n\n"
            
            if patterns:
                summary += "📊 Detected Patterns:\n"
                summary += self.format_patterns_for_display(patterns) + "\n\n"
            
            if anomalies:
                summary += "⚠️ Weather Anomalies:\n"
                summary += self.format_anomalies_for_display(anomalies) + "\n\n"
            
            if recommendations:
                summary += "💡 Recommendations:\n"
                summary += self.format_recommendations_for_display(recommendations)
            
            return summary
            
        except Exception as e:
            return f"❌ Error generating ML summary: {str(e)}"