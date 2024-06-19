
from django.shortcuts import render
import json
import urllib.request
import os

# Function to get weather data from OpenWeatherMap API
def get_weather_data(city):
    api_key = os.getenv('OPENWEATHERMAP_API_KEY')  # Get API key from environment variable
    if not api_key:
        raise ValueError('API key not found. Set OPENWEATHERMAP_API_KEY environment variable.')

    # Construct the API URL
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'

    try:
        # Make the API request
        response = urllib.request.urlopen(url)
        data = json.loads(response.read())

        # Extract relevant data from the API response
        weather_data = {
            "country_code": data['sys']['country'],
            "coordinate": f"{data['coord']['lon']} {data['coord']['lat']}",
            "temp": f"{data['main']['temp']}k",
            "pressure": data['main']['pressure'],
            "humidity": data['main']['humidity'],
        }
        return weather_data

    except urllib.error.HTTPError as e:
        # Handle HTTP errors from API request
        print(f"HTTPError: {e.code} - {e.reason}")
        return None
    except urllib.error.URLError as e:
        # Handle URL errors (e.g., connection refused)
        print(f"URLError: {e.reason}")
        return None
    except json.JSONDecodeError as e:
        # Handle JSON decoding errors
        print(f"JSONDecodeError: {str(e)}")
        return None

# View function for rendering the index page
def index(request):
    if request.method == 'POST':
        city = request.POST.get('city', '')  # Get city name from POST data
        if city:
            weather_data = get_weather_data(city)
            if weather_data:
                return render(request, "main/index.html", weather_data)
            else:
                error_message = "Failed to fetch weather data. Please try again later."
                return render(request, "main/index.html", {"error_message": error_message})
        else:
            error_message = "Please enter a city name."
            return render(request, "main/index.html", {"error_message": error_message})
    else:
        return render(request, "main/index.html")
