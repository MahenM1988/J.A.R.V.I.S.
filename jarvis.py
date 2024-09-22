import pygame
import datetime
import speech_recognition as sr
import pyttsx3
import requests
import platform
import psutil
import GPUtil

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
        
# Function to format capacity
def format_capacity(capacity_bytes):
    if capacity_bytes >= (1024 ** 4):  # 1 TB
        return f"{round(capacity_bytes / (1024 ** 4), 2)} TB"
    elif capacity_bytes >= (1024 ** 3):  # 1 GB
        return f"{round(capacity_bytes / (1024 ** 3), 2)} GB"
    elif capacity_bytes >= (1024 ** 2):  # 1 MB
        return f"{round(capacity_bytes / (1024 ** 2), 2)} MB"
    return f"{capacity_bytes} Bytes"

# Function to get GPU information
def get_gpu_info():
    gpus = GPUtil.getGPUs()
    if gpus:
        gpu_details = []
        for gpu in gpus:
            gpu_details.append(f"{gpu.name}, with {gpu.memoryTotal} MB of memory")
        return "an " + " and an ".join(gpu_details) + "."
    return "comes with onboard graphics."

# Function to get system information
def get_system_info():
    cpu_info = platform.processor()
    cpu_cores = psutil.cpu_count(logical=False)
    
    # Get RAM
    ram_bytes = psutil.virtual_memory().total
    ram_str = format_capacity(ram_bytes)

    disks = psutil.disk_partitions()
    
    total_capacity = 0

    # Calculate total disk capacity
    for d in disks:
        disk_usage = psutil.disk_usage(d.mountpoint)
        total_capacity += disk_usage.total

    # Convert total capacity to appropriate format
    total_capacity_str = format_capacity(total_capacity)

    # Get GPU information dynamically
    graphics_info = get_gpu_info()
    network_type = "LAN" if psutil.net_if_stats()['Ethernet'].isup else "WIFI"

    response = (f"I am currently running on a {cpu_info}, "
                f"with {cpu_cores} cores, clocked at {psutil.cpu_freq().current:.2f} Gigahertz. "
                f"This system has {ram_str} of RAM. "
                f"The total capacity of the disks is {total_capacity_str}. "
                f"This system {graphics_info} "
                f"The system is connected to a Local Area Network via {network_type}.")
    
    return response

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
    
    # Check for system info commands
        if any(keyword in user_input.lower() for keyword in ["system info", "system details", "system specifications"]):
            system_info = get_system_info()
            print(system_info)
            speak(system_info)
        else:
            # Add rule-based responses here
            print(f"Response to: {user_input}")

if __name__ == "__main__":
    main()
