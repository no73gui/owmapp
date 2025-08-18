import network
import urequests
import time
from machine import Pin
import secrets

# --- Wi-Fi and API credentials ---
ssid = secrets.ssid
password = secrets.password
api_key = secrets.api_key
city_name = secrets.zip
# Replace with your city
# connect to the mysql/http server
server_url = 'http://192.168.1.76:5000/weather_data'

# --- Connect to Wi-Fi ---
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

print('Connecting to Wi-Fi...')
max_retry = 20
while not wlan.isconnected() and max_retry > 0:
    print("...")
    time.sleep(1)
    max_retry -= 1
if wlan.isconnected():
    print("Connected to Wi-Fi")
    print('IP Address:', wlan.ifconfig()[0])
else:
    print("Failed to connect to Wi-Fi...")
    while True:
        led.value(1)
        time.sleep(0.1)
        led.value(0)
        time.sleep(0.4)
# --- Fetch and parse weather data ---
loop_interval_ms = 86000
while True:
    start_ms = time.ticks_ms()

    try:
    # Construct the API URL. Note: OpenWeatherMap free API works best with city names.
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=imperial"
        response = urequests.get(url)
    
    # Check if the request was successful
        if response.status_code == 200:
            data = response.json()
            temp_farenheit = data['main']['temp']
            humidity = data['main']['humidity']
            wind_speed = data['wind']['speed']
            zip_code = "72758" # Using static zip code
            print(f"Fetched data from OpenWeatherMap. Temp(F): {temp_farenheit}, Humidity: {humidity}%")
            payload = {
                'zipCode': zip_code,
                'temperature': temp_farenheit,
                'humidity': humidity,
                'wind_speed': wind_speed        
                }
            post_res = urequests.post(server_url, json=payload)
            if post_res.status_code == 200:
                print("Data posted to local server successfully!")
            else:
                print(f"Failed to post data. Status code: {post_res.status_code}")
                print("Response:", post_res.text)
            post_res.close()
        else:
            print(f"Error fetching weather data. Status code: {response.status_code}")
    
        response.close() # Always close the response object

    except Exception as e:
        print('An error occurred:', e) 
    
    end_time = time.ticks_ms()
    elapsedT = time.ticks_diff(end_time, start_ms)
    sleepT = loop_interval_ms - elapsedT

    if sleepT > 0: 
        time.sleep_ms(int(sleepT))
    led = Pin("LED", Pin.OUT)

    led.value(1) # Turn the LED on
    time.sleep(0.5) # Wait for half a second
    led.value(0) # Turn the LED off
    time.sleep(0.5) # Wait for half a second
    
