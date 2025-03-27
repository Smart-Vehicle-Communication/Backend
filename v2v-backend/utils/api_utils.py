import requests

# Fetch weather data from OpenWeatherMap API
def get_weather_data(lat, lon, api_key):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {
            "temperature": data["main"]["temp"],
            "weather": data["weather"][0]["description"],
            "wind_speed": data["wind"]["speed"]
        }
    return {"error": "Unable to fetch weather data"}

# Fetch traffic data (placeholder - can be integrated later)
def get_traffic_data(lat, lon):
    # Implement real traffic API logic here if needed
    return {"traffic_status": "Moderate", "incident_count": 2}
