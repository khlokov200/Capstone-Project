# 🌤️ Advanced Weather Dashboard

A professional-grade weather dashboard built with Python and Tkinter, featuring real-time and local weather data, advanced analytics, interactive charts, and a modern multi-tab interface.

---

## 🛠️ Setup Instructions

### Requirements
- Python 3.8+
- Tkinter (usually included with Python)
- matplotlib
- requests
- python-dotenv

### Installation
```bash
git clone <repository-url>
cd Capstone-Project
pip install -r requirements.txt
```

### Environment Setup
1. Register at [OpenWeatherMap](https://openweathermap.org/api) and get your API key.
2. Create a `.env` file in the project root:
   ```
   WEATHER_API_KEY=your_api_key_here
   ```
3. (Optional) To use local JSON data, set:
   ```
   DATA_SOURCE_MODE=json
   ```
   By default, the app uses live API data.

### Running the App
```bash
python main.py
```

---

## 📖 Usage Guide

- Launch the app to access a multi-tabbed dashboard with real-time or local weather data.
- Use the Quick Actions dashboard for instant access to major features.
- Switch between tabs for current weather, forecasts, analytics, health & wellness, and more.
- Toggle between live API and local JSON data by setting the `DATA_SOURCE_MODE` environment variable.
- All features are available offline in JSON mode using the `data/team_cities.json` file.

---

## ✨ Feature Summary

- **Dual Data Source**: Live API or local JSON (`team_cities.json`) for all weather data.
- **15+ Tabs**: Current weather, forecasts, analytics, health, and more.
- **Quick Actions Dashboard**: 9 instant-access weather tools.
- **Advanced Charts**: 6+ chart types with interactive controls.
- **Health & Wellness**: UV index, air quality, and activity recommendations.
- **Professional UI**: Modern split-panel layout, theme toggle, and legends.
- **Offline Mode**: Full functionality using local data for demos or testing.
- **Personalization**: Weather journal, poetry generator, and history tracking.
- **Robust Error Handling**: Graceful error messages and guidance.

---

## 📄 License

MIT License - See LICENSE file for details

---

## 👨‍💻 Developer

**Capstone Project** - Advanced Weather Dashboard  
*Demonstrating comprehensive software development skills and modern application architecture*

**Contact**: [Your Contact Information]  
**Project Repository**: [Repository Link]

---

*This project represents a complete software development lifecycle from conception to deployment, showcasing technical skills in Python development, API integration, data visualization, UI/UX design, and software engineering best practices.*
- **🌡️ Quick Weather** - Instant current conditions
- **📅 Today's Plan** - Weather-based daily planning  
- **🎯 Best Times** - Activity timing optimization
- **📱 Share Weather** - Social media content generation
- **⚠️ Weather Alerts** - Safety warnings and notifications
- **🔄 Refresh All** - System optimization and refresh
- **📊 Quick Stats** - Usage and performance statistics
- **🌍 Multi-City** - Global weather overview

### **🌤️ Weather Information Tabs**
- **Current Weather**: Real-time conditions with detailed metrics
- **Forecast**: Short-term weather predictions with hourly details
- **5-Day Forecast**: Extended weather outlook with planning tools
- **Live Weather**: Real-time weather animations and radar (when available)

### **📊 Analysis & Comparison**
- **Analytics & Trends**: Weather pattern analysis with correlation studies
- **City Comparison**: Multi-city weather comparison with charts
- **Severe Weather**: Weather alert monitoring and safety information

### **🏥 Health & Wellness**
- **Health Monitoring**: UV index, air quality, pollen forecasts
- **Activity Recommendations**: Weather-based outdoor activity suggestions
- **Wellness Dashboard**: Comprehensive health metrics visualization

### **🤖 Advanced Features**
- **Smart Alerts**: Intelligent weather notification system
- **Activity Suggestions**: AI-powered activity recommendations
- **Weather Camera**: Visual weather documentation (when available)

### **📝 Personal Features**
- **Weather Journal**: Personal weather logging and mood tracking
- **Poetry Generator**: Creative weather-inspired content creation
- **History Tracking**: Long-term weather data analysis

---

## 🛠️ **Technical Architecture**

### **Clean Code Structure**
```
Capstone-Project/
├── main.py                     # Application entry point
├── controllers/
│   ├── weather_controller.py   # Main business logic controller
│   └── ml_controller.py        # Machine learning features
├── ui/
│   ├── main_window.py          # Main application window
│   ├── tabs.py                 # Individual tab components
│   ├── tab_helpers.py          # Chart helpers and utilities
│   └── components.py           # Reusable UI components
├── services/
│   ├── live_weather_service.py # Real-time weather services
│   ├── weather_service.py      # API integration services
│   └── json_data_service.py    # JSON data loading service
├── models/
│   └── weather_models.py       # Data models and structures
├── core/
│   ├── api.py                  # API handling
│   ├── processor.py            # Data processing
│   └── storage.py              # Data persistence
└── data/                       # Data storage and logs
```

### **Technology Stack**
- **Frontend**: Python Tkinter with custom styling and components
- **Charts**: matplotlib with professional chart generation
- **Data**: CSV-based storage with export capabilities  
- **API**: OpenWeatherMap integration with error handling
- **Architecture**: MVC pattern with clean separation of concerns

### **Key Technical Features**
- **Error Handling**: Comprehensive error management throughout
- **Code Organization**: Modular design with helper classes
- **Performance**: Optimized chart generation and data processing
- **Extensibility**: Plugin-ready architecture for future enhancements
- **Testing**: Comprehensive testing and validation

---

## 🎨 **User Interface Highlights**

### **Professional Design**
- **Modern Split-Panel Layout**: Dashboard-style interface design
- **Consistent Styling**: Professional button styles and color schemes
- **Responsive Components**: Adaptive layouts for different content types
- **Visual Hierarchy**: Clear organization and intuitive navigation

### **Chart Integration**
- **Interactive Charts**: Click-to-generate chart system
- **Multiple Chart Types**: 6+ different visualization options
- **Professional Styling**: Color-coded charts with legends and annotations
- **Error Graceful Degradation**: Fallback when charts unavailable

### **User Experience**
- **Intuitive Navigation**: Tab-based interface with logical organization
- **Quick Access**: Instant access to all features via Quick Actions
- **Error Guidance**: Helpful error messages and user tips
- **Professional Appearance**: Commercial-quality interface design

---

## 🔧 **Setup & Installation**

### **Requirements**
- Python 3.8+
- Tkinter (usually included with Python)
- matplotlib for charts
- requests for API calls
- python-dotenv for environment management

### **Installation**
```bash
# Clone the repository
git clone <repository-url>
cd Capstone-Project

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
echo "WEATHER_API_KEY=your_openweather_api_key" > .env
```

### **API Setup**
1. Register at [OpenWeatherMap](https://openweathermap.org/api)
2. Get your free API key
3. Add it to your `.env` file:
   ```
   WEATHER_API_KEY=your_api_key_here
   ```

### **Running the Application**
```bash
python main.py
```

---

## 🧪 **Testing & Quality Assurance**

### **Comprehensive Testing**
- **✅ All UI Components**: Every tab and button tested
- **✅ Chart Generation**: All 6 chart types working correctly
- **✅ Error Handling**: Graceful error management verified
- **✅ API Integration**: Weather data fetching tested
- **✅ No Critical Bugs**: Application runs stably without crashes

### **Quality Metrics**
- **31+ Interactive Buttons** across all tabs
- **15 Functional Tabs** with comprehensive features
- **6+ Chart Types** with professional visualization
- **Zero Critical Errors** in core functionality
- **Professional Code Quality** with clean architecture

---

## 🎯 **Capstone Project Milestones**

### **✅ Milestone 1: Foundation**
- Basic weather API integration
- Simple Tkinter GUI
- Data storage implementation

### **✅ Milestone 2: Enhancement** 
- Multi-tab interface development
- Chart integration with matplotlib
- Advanced weather features

### **✅ Milestone 3: Professional Features**
- Quick Actions dashboard implementation
- Health & wellness monitoring
- Advanced analytics and trends

### **✅ Milestone 4: Completion**
- Bug fixes and testing
- UI/UX improvements
- Documentation and final polish

### **🎉 Final Result**
A professional-grade weather dashboard application demonstrating:
- **Full-stack development skills**
- **API integration and data management**
- **Modern UI/UX design principles**
- **Software engineering best practices**
- **Problem-solving and debugging abilities**

---

## 🚀 **Future Enhancement Opportunities**

- **Mobile Responsiveness**: Adapt interface for mobile devices
- **Database Integration**: Migrate from CSV to SQL database
- **Machine Learning**: Weather prediction algorithms
- **Real-time Notifications**: Push notifications for weather alerts
- **Cloud Integration**: Weather data backup and sync
- **Multi-language Support**: Internationalization features
- **Weather Station Integration**: IoT weather sensor data
- **Advanced Mapping**: Interactive weather maps

---

## 📄 **License**

MIT License - See LICENSE file for details

---

## 👨‍💻 **Developer**

**Capstone Project** - Advanced Weather Dashboard  
*Demonstrating comprehensive software development skills and modern application architecture*

**Contact**: [Your Contact Information]  
**Project Repository**: [Repository Link]

---

*This project represents a complete software development lifecycle from conception to deployment, showcasing technical skills in Python development, API integration, data visualization, UI/UX design, and software engineering best practices.*

---

## Dual Data Source Support

This application supports two modes for weather and forecast data:
- **API Mode**: Uses live weather APIs (default)
- **JSON Mode**: Loads data from local JSON files (see `services/json_data_service.py`)

### How to Use JSON Data Mode
1. Place your weather/forecast JSON files in the `data/` directory (see [exports](https://github.com/StrayDogSyn/New_Team_Dashboard/tree/main/exports) for sample data).
2. Set the data source mode in `main.py` (see comments in code):
   - `data_source = "json"` for local JSON
   - `data_source = "api"` for live API
3. The controller (`weather_controller.py`) will use the appropriate service based on this setting.

### Benefits
- **Offline development**: No API keys or network required
- **Testing**: Use static, repeatable data
- **Demo**: Showcase features without live API

### Architecture Overview
- `WeatherService`/`ForecastService`: Live API data
- `JSONDataService`: Loads local JSON data
- `weather_controller.py`: Delegates to the correct service
- `main.py`: Sets the data source mode

See `ARCHITECTURE.md` for more details on the system structure and data flow.
