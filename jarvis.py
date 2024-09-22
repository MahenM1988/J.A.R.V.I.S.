import pygame
import datetime
import speech_recognition as sr
import pyttsx3
import requests

# Initialize Pygame
pygame.init()

# Initialize Text-to-Speech with Windows Zira
engine = pyttsx3.init()
voices = engine.getProperty('voices')
# Set the voice to Zira
for voice in voices:
    if "Zira" in voice.name:
        engine.setProperty('voice', voice.id)

# Function to get weather data
def get_weather(api_key):
    city = "Colombo"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Function to determine greeting based on time
def get_time_greeting():
    current_hour = datetime.datetime.now().hour
    if current_hour < 12:
        return "Good morning"
    elif current_hour < 16:
        return "Good afternoon"
    else:
        return "Good evening"

# Function to get the appropriate suffix for the day
def get_day_suffix(day):
    if 10 <= day % 100 <= 20:
        return "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")
        return suffix

# Function to speak text
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function for speech recognition
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command
        except sr.UnknownValueError:
            return "Sorry, I did not understand that."
        except sr.RequestError:
            return "Could not request results."

# Main function
def main():
    api_key = "e36d7c17f13269895f55267fe99a743a"  # Replace with your OpenWeatherMap API Key
    use_console = input("Would you like to use the console (C) or speech recognition (S)? ").strip().upper()

    weather_data = get_weather(api_key)
    
    if weather_data:
        temperature = weather_data['main']['temp']
        humidity = weather_data['main']['humidity']
        pressure = weather_data['main']['pressure']
        weather_description = weather_data['weather'][0]['description']
    else:
        temperature = "unknown"
        humidity = "unknown"
        pressure = "unknown"
        weather_description = "unknown"

    greeting = get_time_greeting()
    now = datetime.datetime.now()
    day = now.day
    day_suffix = get_day_suffix(day)
    current_time = now.strftime(f"%A, the {day}{day_suffix} of %B, %Y")

    response_text = (f"{greeting}, the current date and time in Colombo, Sri Lanka is {current_time}. "
                     f"The temperature is {temperature} degrees Celsius, with a humidity of {humidity}%, "
                     f"an atmospheric pressure of {pressure} hPa, and with {weather_description}. "
                     "How may I assist you today?")
    
    print(response_text)
    speak(response_text)

    # Conversation loop
    while True:
        if use_console == "C":
            user_input = input("You: ")
        elif use_console == "S":
            user_input = recognize_speech()
        
        if user_input.lower() == "exit":
            break
        # Add rule-based responses here
        print(f"Response to: {user_input}")

if __name__ == "__main__":
    main()
