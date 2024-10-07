import os
import subprocess
import pygame
import datetime
import speech_recognition as sr
import pyttsx3
import requests
import platform
import psutil
import GPUtil
import webbrowser
import configparser
import threading
import webbrowser

# Set environment variable to hide the support prompt
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
pygame.init()

# Initialize Text-to-Speech with Windows Zira
engine = pyttsx3.init()
voices = engine.getProperty('voices')
for voice in voices:
    if "Zira" in voice.name:
        engine.setProperty('voice', voice.id)

# Load configuration from config.ini
config = configparser.ConfigParser()
config.read('config.ini')

# Replace with your actual API keys and URLs from config
NEWS_API_KEY = config['API']['NEWS_API_KEY']
WEATHER_API_KEY = config['API']['WEATHER_API_KEY']
NEWS_BASE_URL = config['API']['NEWS_BASE_URL']
WEATHER_BASE_URL = config['API']['WEATHER_BASE_URL']

# Get directory from config
directory_to_check = config['Settings']['DIRECTORY']

# Flag to control TTS
tts_running = False

def speak(text):
    global tts_running
    tts_running = True
    engine.say(text)
    engine.runAndWait()
    tts_running = False

def stop_tts_on_space():
    global tts_running
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and tts_running:
                    engine.stop()
                    tts_running = False
                    print("TTS stopped.")

# Start the key press listener in a separate thread
threading.Thread(target=stop_tts_on_space, daemon=True).start()

def get_time_greeting():
    current_hour = datetime.datetime.now().hour
    return f"Good {'morning' if current_hour < 12 else 'afternoon' if current_hour < 16 else 'evening'},"

def get_day_suffix(day):
    if 10 <= day % 100 <= 20:
        return "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")
        return suffix


def current_date():
    now = datetime.datetime.now()
    day = now.day
    day_suffix = get_day_suffix(day)
    return now.strftime(f"%A, the {day}{day_suffix} of %B, %Y")


def current_time():
    return datetime.datetime.now().strftime("%I:%M %p")


def speak(text):
    engine.say(text)
    engine.runAndWait()


def get_top_headlines():
    params = {
        'apiKey': NEWS_API_KEY,
        'language': 'en',
    }
    try:
        response = requests.get(NEWS_BASE_URL, params=params)
        response.raise_for_status()  # Raise an error for bad responses
        news_headlines = response.json()['articles']
        return news_headlines
    except requests.RequestException as e:
        print(f"Error fetching news: {e}")
        return []


def get_weather(city='Colombo', country='LK'):
    params = {
        'q': f'{city},{country}',
        'appid': WEATHER_API_KEY,
        'units': 'metric'
    }
    try:
        response = requests.get(WEATHER_BASE_URL, params=params)
        response.raise_for_status()  # Raise an error for bad responses
        data = response.json()
        return {
            'temperature': data['main']['temp'],
            'humidity': data['main']['humidity'],
            'pressure': data['main']['pressure'],
            'description': data['weather'][0]['description']
        }
    except requests.RequestException as e:
        print(f"Error fetching weather: {e}")
        return None


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


def list_files_and_folders(directory):
    items = []
    try:
        for root, dirs, files in os.walk(directory):
            items.extend([os.path.join(root, d) for d in dirs])
            items.extend([os.path.join(root, f) for f in files])
        return items
    except Exception as e:
        print(f"Error listing files: {e}")
        return []


def play_file(file_path):
    try:
        if file_path.lower().endswith(('.mp4', '.mp3', '.wav', '.avi', '.mkv', '.wmv')):
            os.startfile(file_path)
            print(f"Playing: {file_path}")
        else:
            print(f"Unsupported file type: {file_path}")
    except Exception as e:
        print(f"Failed to play {file_path}: {str(e)}")


def get_processor_name():
    try:
        output = subprocess.check_output("wmic cpu get name", shell=True)
        return output.decode().split('\n')[1].strip()
    except Exception as e:
        return str(e)


def get_motherboard_name():
    try:
        output = subprocess.check_output("wmic baseboard get product, manufacturer", shell=True)
        lines = output.decode().strip().split('\n')
        if len(lines) > 1:
            return lines[1].strip()
        return "Unknown"
    except Exception as e:
        return str(e)


def get_gpu_info():
    try:
        gpus = GPUtil.getGPUs()
        if gpus:
            return gpus[0].name
        else:
            output = subprocess.check_output("wmic path win32_VideoController get name", shell=True)
            lines = output.decode().strip().split('\n')
            if len(lines) > 1:
                return lines[1].strip()
            return "Unknown"
    except Exception as e:
        return str(e)


def get_system_info():
    processor = get_processor_name()
    motherboard = get_motherboard_name()

    ram_info = psutil.virtual_memory()
    ram_total = ram_info.total / (1024 ** 3)  # Convert to GB

    disk_info = psutil.disk_usage('/')
    disk_total = disk_info.total / (1024 ** 3)  # Convert to GB

    gpu_name = get_gpu_info()

    os_info = platform.system() + " " + platform.release()

    return (processor, motherboard, ram_total, disk_total, gpu_name, os_info)


def load_entertainment_library(directory):
    print("Loading Content...")
    speak("Loading Content...")
    files_and_folders = list_files_and_folders(directory)
    print("Files and Folders:")
    for item in files_and_folders:
        print(item)

    current_index = 0
    while True:
        command = input("Type 'next' for next item, 'play [file name]' to play, or 'exit' to leave: ")
        if command.lower() == "next":
            current_index += 1
            if current_index >= len(files_and_folders):
                current_index = 0
            print(files_and_folders[current_index])
        elif command.lower().startswith("play "):
            file_name = command[5:].strip()  # Get the name after "play "
            file_path = os.path.join(directory, file_name)
            if os.path.isfile(file_path):
                play_file(file_path)
            else:
                print(f"File not found: {file_name}")
        elif command.lower() == "exit":
            break


def report_current_datetime():
    date = current_date()
    current_time_str = current_time()
    response_text = (f"The current date and time in Colombo, Sri Lanka, is {date}, {current_time_str}.")
    print(response_text)
    speak(response_text)


def report_weather():
    weather = get_weather()
    if weather:
        temperature = weather['temperature']
        humidity = weather['humidity']
        pressure = weather['pressure']
        weather_description = weather['description']
        response_text = (f"The temperature is {temperature} degrees Celsius, "
                         f"with a humidity of {humidity}%, "
                         f"an atmospheric pressure of {pressure} hPa, "
                         f"and {weather_description}.")
        print(response_text)
        speak(response_text)
    else:
        print("Could not fetch weather data.")


def fetch_news_headlines():
    news_headlines = get_top_headlines()
    if news_headlines:
        headlines_text = "Here are the top news headlines:\n"
        for article in news_headlines[:10]:  # Limit to 10 headlines
            headlines_text += f"{article['title']}\n"
        print(headlines_text)
        speak(headlines_text)
    else:
        print("Unable to fetch news headlines at the moment.")

def perform_search(user_input):
    user_input_lower = user_input.lower()  # Convert input to lower case
    parts = user_input_lower.split("search", 1)
    if len(parts) > 1:
        query = parts[1].strip()
        webbrowser.open(f"https://www.duckduckgo.com/{query}")
        speak(f"Searching for {query}")
    else:
        print("No search query entered.")

def look_up(user_input):
    user_input_lower = user_input.lower()  # Convert input to lower case
    parts = user_input_lower.split("look up", 1)
    if len(parts) > 1:
        query = parts[1].strip()
        webbrowser.open(f"https://en.wikipedia.org/wiki/{query}")
        speak(f"Looking up: {query}")
    else:
        print("Nothing to look up.")

def report_system_specs():
    processor, motherboard, ram_total, disk_total, gpu_name, os_info = get_system_info()
    sys_info_text = (f"I am currently running on an {processor}. The motherboard is {motherboard}. "
                     f"The GPU is {gpu_name}. There is {ram_total:.2f} GB RAM installed, "
                     f"and the total disk space is {disk_total:.2f} GB. The operating system is {os_info}.")
    print(sys_info_text)
    speak(sys_info_text)


def handle_command(user_input, directory):
    if "access entertainment library" in user_input.lower():
        load_entertainment_library(directory)
    elif "current date and time" in user_input.lower():
        report_current_datetime()
    elif "current weather update" in user_input.lower():
        report_weather()
    elif "news headlines" in user_input.lower():
        fetch_news_headlines()
    elif "search" in user_input.lower():
        perform_search(user_input)
    elif "look up" in user_input.lower():
        look_up(user_input)
    elif "system specifications" in user_input.lower():
        report_system_specs()
    else:
        print(f"User input: {user_input}")


def main():
    use_console = input("Would you like to use the console (C) or speech recognition (S)? ").strip().upper()

    greeting = get_time_greeting()
    date = current_date()
    current_time_str = current_time()

    # Initial response with weather update
    weather = get_weather()
    temperature = humidity = pressure = weather_description = "N/A"
    
    if weather:
        temperature = weather['temperature']
        humidity = weather['humidity']
        pressure = weather['pressure']
        weather_description = weather['description']

    response_text = (f"{greeting} the current date and time in Colombo, Sri Lanka, is {date}, {current_time_str}. "
                     f"The temperature is {temperature} degrees Celsius, with a humidity of {humidity}%, "
                     f"an atmospheric pressure of {pressure} hPa, and with {weather_description}.")
    
    print(response_text)
    speak(response_text)

    # Conversation loop
    while True:
        if use_console == "C":
            user_input = input("You: ")
        elif use_console == "S":
            user_input = recognize_speech()
        
        if user_input.lower() == "exit":
            confirm_exit = input("Are you sure you want to exit? (yes/no): ").strip().lower()
            if confirm_exit == "yes":
                break
        
        handle_command(user_input, directory_to_check)

if __name__ == "__main__":
    main()