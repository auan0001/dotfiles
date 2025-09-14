#!/usr/bin/env python
import json
import requests
from datetime import datetime
from zoneinfo import ZoneInfo

WEATHER_ICONS = {
    "113": "☀️",
    "116": "⛅",
    "119": "☁️",
    "122": "☁️",
    "143": "☁️",
    "176": "🌧️",
    "179": "🌧️",
    "182": "🌧️",
    "185": "🌧️",
    "200": "⛈️",
    "227": "🌨️",
    "230": "🌨️",
    "248": "☁️",
    "260": "☁️",
    "263": "🌧️",
    "266": "🌧️",
    "281": "🌧️",
    "284": "🌧️",
    "293": "🌧️",
    "296": "🌧️",
    "299": "🌧️",
    "302": "🌧️",
    "305": "🌧️",
    "308": "🌧️",
    "311": "🌧️",
    "314": "🌧️",
    "317": "🌧️",
    "320": "🌨️",
    "323": "🌨️",
    "326": "🌨️",
    "329": "❄️",
    "332": "❄️",
    "335": "❄️",
    "338": "❄️",
    "350": "🌧️",
    "353": "🌧️",
    "356": "🌧️",
    "359": "🌧️",
    "362": "🌧️",
    "365": "🌧️",
    "368": "🌧️",
    "371": "❄️",
    "374": "🌨️",
    "377": "🌨️",
    "386": "🌨️",
    "389": "🌨️",
    "392": "🌧️",
    "395": "❄️",
}

# Get weather data
weather = requests.get("https://wttr.in/Stockholm?format=j1").json()
current = weather["current_condition"][0]
current_hour = datetime.now(ZoneInfo("Europe/Stockholm")).hour

# Format main text
temp = int(current["FeelsLikeC"])
temp_str = f"+{temp}" if 0 < temp < 10 else str(temp)
icon = WEATHER_ICONS.get(current["weatherCode"], "❓")

data = {
    "text": f"{icon}{temp_str}°C",
    "tooltip": f"<b>{current['weatherDesc'][0]['value']} {current['temp_C']}°C</b>\n"
    f"Feels like: {current['FeelsLikeC']}°C\n"
    f"Wind: {current['windspeedKmph']} Km/h\n"
    f"Humidity: {current['humidity']}%\n",
}

# Add forecast
for i, day in enumerate(weather["weather"][:2]):  # Only today and tomorrow
    day_name = "Today" if i == 0 else "Tomorrow"
    data["tooltip"] += f"\n<b>{day_name}, {day['date']}</b>\n"
    data["tooltip"] += f"⬆️ {day['maxtempC']}°C ⬇️ {day['mintempC']}°C "
    data["tooltip"] += (
        f"🌅 {day['astronomy'][0]['sunrise']} 🌇 {day['astronomy'][0]['sunset']}\n"
    )

    # Show relevant hours only
    for hour in day["hourly"]:
        hour_time = int(hour["time"].replace("00", "") or "0")
        if i == 0 and hour_time < current_hour - 2:  # Skip past hours for today
            continue

        icon = WEATHER_ICONS.get(hour["weatherCode"], "❓")
        data["tooltip"] += (
            f"{hour_time:02d} {icon} {hour['FeelsLikeC']}°C {hour['weatherDesc'][0]['value']}\n"
        )

print(json.dumps(data))
