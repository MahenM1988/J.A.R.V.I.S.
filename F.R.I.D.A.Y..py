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

# Initialize Pygame
pygame.init()

# Initialize Text-to-Speech with Windows Zira
engine = pyttsx3.init()
voices = engine.getProperty('voices')
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
    return f"Good {'morning' if current_hour < 12 else 'afternoon' if current_hour < 16 else 'evening'},"

# Function to get the appropriate suffix for the day
def get_day_suffix(day):
    if 10 <= day % 100 <= 20:
        return "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")
        return suffix

# Function to get the current date
def current_date():
    now = datetime.datetime.now()
    day = now.day
    day_suffix = get_day_suffix(day)
    return now.strftime(f"%A, the {day}{day_suffix} of %B, %Y")

# Function to get the current time
def current_time():
    return datetime.datetime.now().strftime("%I:%M %p")

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
    if capacity_bytes >= (1024 ** 4):
        return f"{round(capacity_bytes / (1024 ** 4), 2)} TB"
    elif capacity_bytes >= (1024 ** 3):
        return f"{round(capacity_bytes / (1024 ** 3), 2)} GB"
    elif capacity_bytes >= (1024 ** 2):
        return f"{round(capacity_bytes / (1024 ** 2), 2)} MB"
    return f"{capacity_bytes} Bytes"

# Function to get GPU information
def get_gpu_info():
    gpus = GPUtil.getGPUs()
    if gpus:
        gpu_details = []
        for gpu in gpus:
            gpu_details.append(f"{gpu.name}, with {gpu.memoryTotal} MB of memory")
        return " and ".join(gpu_details)
    return "Onboard Graphics"

# Function to get system information
def get_system_info():
    cpu_info = platform.processor()
    cpu_cores = psutil.cpu_count(logical=False)
    ram_bytes = psutil.virtual_memory().total
    ram_str = format_capacity(ram_bytes)

    # Get all disk partitions
    partitions = psutil.disk_partitions()
    disk_info_list = []

    for partition in partitions:
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            disk_free = format_capacity(usage.free)
            disk_total = format_capacity(usage.total)
            disk_info_list.append(f"{partition.mountpoint} {disk_free} free of {disk_total}")
        except PermissionError:
            continue  # Skip partitions that are not ready or accessible

    disk_info = "\n".join(disk_info_list)

    graphics_info = get_gpu_info()
    network_type = "LAN" if psutil.net_if_stats().get('Ethernet', False).isup else "WIFI"

    return (f"Processor: {cpu_info}, {cpu_cores} cores, @ {psutil.cpu_freq().current:.2f} GHz\n"
            f"Available RAM: {ram_str}\n"
            f"Disk Drives Online: {disk_info}\n"
            f"Display Adapter: {graphics_info}\n"
            f"Network Connectivity: {network_type}")

# Function to list all files and folders recursively
def list_files_and_folders(directory):
    items = []
    try:
        for root, dirs, files in os.walk(directory):
            items.extend([os.path.join(root, d) for d in dirs])
            items.extend([os.path.join(root, f) for f in files])
        return items
    except Exception as e:
        return []

# Function to play a file
def play_file(file_path):
    try:
        # Check if the file is an audio/video file
        if file_path.lower().endswith(('.mp4', '.mp3', '.wav', '.avi', '.mkv', '.wmv')):
            os.startfile(file_path)  # Execute the file with the associated application
            print(f"Playing: {file_path}")
        else:
            print(f"Unsupported file type: {file_path}")
    except Exception as e:
        print(f"Failed to play {file_path}: {str(e)}")


# Main function
def main():
    api_key = "e36d7c17f13269895f55267fe99a743a"  # Replace with your OpenWeatherMap API Key
    use_console = input("Would you like to use the console (C) or speech recognition (S)? ").strip().upper()

    # Hardcoded directory
    directory_to_check = r"C:\Users\Mahen Mahindaratne\Desktop\Entertainment"  # Change to your desired directory

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
    date = current_date()
    time = current_time()

    response_text = (f"{greeting} the current date and time in Colombo, Sri Lanka, is {date}, {time}. "
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
        
        if "access entertainment library" in user_input.lower():
            print("Loading Content...")
            speak("Loading Content...")
            files_and_folders = list_files_and_folders(directory_to_check)
            print("Files and Folders:")
            for item in files_and_folders:
                print(item)

            current_index = 0
            while True:
                command = input("Type 'next' for next item, 'play [file name]' to play, or 'exit' to leave: ")
                if command.lower() == "next":
                    current_index += 1
                    if current_index >= len(files_and_folders):
                        current_index = 0  # Loop back to the start
                    print(files_and_folders[current_index])
                elif command.lower().startswith("play "):
                    file_name = command[5:].strip()  # Get the name after "play "
                    file_path = os.path.join(directory_to_check, file_name)
                    if os.path.isfile(file_path):
                        play_file(file_path)
                    else:
                        print(f"File not found: {file_name}")
                elif command.lower() == "exit":
                    break

        elif any(keyword in user_input.lower() for keyword in ["system info", "system details", "system specifications"]):
            print("Bringing up the system details now:")
            speak("Bringing up the system details now:")
            system_info = get_system_info()
            print(system_info)
        else:
            print(f"Response to: {user_input}")

if __name__ == "__main__":
    main()
