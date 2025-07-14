# WeatherApp: A simple weather application using OpenWeatherMap API


## 🧪 Testing with Pytest
# To add basic tests:

# Create `test_weather.py` inside a `tests/` folder:
import os
import pytest
from dotenv import load_dotenv
import requests
import os
import pytest
from dotenv import load_dotenv
import requests

load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def test_api_key():
    assert API_KEY is not None and API_KEY != ""

def test_weather_fetch():
    city = "London"
    response = requests.get(BASE_URL, params={"q": city, "appid": API_KEY, "units": "metric"})
    assert response.status_code == 200
    data = response.json()
    assert "main" in data and "temp" in data["main"]
import os
import pytest
from dotenv import load_dotenv
import requests

load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def test_api_key():
    assert API_KEY is not None and API_KEY != ""

def test_weather_fetch():
    city = "London"
    response = requests.get(BASE_URL, params={"q": city, "appid": API_KEY, "units": "metric"})
    assert response.status_code == 200
    data = response.json()
    assert "main" in data and "temp" in data["main"]
import os
import pytest
from dotenv import load_dotenv
import requests
import os
import pytest
from dotenv import load_dotenv
import requests

load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def test_api_key():
    assert API_KEY is not None and API_KEY != ""

def test_weather_fetch():
    city = "London"
    response = requests.get(BASE_URL, params={"q": city, "appid": API_KEY, "units": "metric"})
    assert response.status_code == 200
    data = response.json()
    assert "main" in data and "temp" in data["main"]

