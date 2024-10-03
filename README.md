# J.A.R.V.I.S.

## Overview

This Python script serves as a personal assistant inspired by J.A.R.V.I.S. from the Marvel Cinematic Universe. It combines weather information, voice recognition, and media management into a cohesive tool that allows users to interact with their environment in a more intuitive way.

## Features

- **Weather Updates:** Fetch real-time weather data for Colombo, Sri Lanka, using the OpenWeatherMap API.
- **Time-Based Greetings:** Provides personalized greetings based on the time of day.
- **Text-to-Speech (TTS):** Communicates information using the Windows Zira voice for a more human-like interaction.
- **Voice Recognition:** Allows users to issue commands verbally for a hands-free experience.
- **Media Management:** Lists and plays media files from a specified directory, acting as a simple entertainment library.

## Requirements

- Python 3.x
- Required libraries:
  - `pygame` (for audio support)
  - `requests` (for HTTP requests)
  - `speech_recognition` (for recognizing spoken commands)
  - `pyttsx3` (for text-to-speech functionality)

Install the necessary libraries using pip:

```bash
pip install pygame requests SpeechRecognition pyttsx3
```

## Setup Instructions

1. **Obtain an API Key:**
   - Register on [OpenWeatherMap](https://openweathermap.org/api) to receive your API key.

2. **Set Up Environment Variable:**
   - Set the `WEATHER_API_KEY` environment variable with your API key:
     - On Windows:
       ```cmd
       set WEATHER_API_KEY=your_api_key_here
       ```
     - On macOS/Linux:
       ```bash
       export WEATHER_API_KEY=your_api_key_here
       ```

3. **Configure Media Directory:**
   - Update the `directory_to_check` variable in the script to point to your preferred media folder.

## How to Use

1. **Run the Assistant:**
   Execute the script from your command line:
   ```bash
   python your_script_name.py
   ```

2. **Select Interaction Method:**
   - Choose between console input (C) or speech recognition (S) when prompted.

3. **Voice Commands:**
   - Speak or type commands such as:
     - "Access entertainment library" to browse files.
     - "Play [file name]" to play a specific media file.

4. **Terminate the Assistant:**
   - Type `exit` or say `exit` to close the application.

## Core Functions

- **get_weather(api_key):** Retrieves weather information for Colombo based on the API key.
- **get_time_greeting():** Generates a greeting based on the current hour.
- **current_date():** Formats and returns the current date with proper suffix.
- **speak(text):** Utilizes TTS to verbalize text messages.
- **recognize_speech():** Captures and converts spoken words into text commands.
- **list_files_and_folders(directory):** Gathers a list of all files and folders in a specified directory.
- **play_file(file_path):** Opens and plays media files with the appropriate application.

## Responsible Use

- Ensure you have the right to access and play all media files in your library.
- Consider your surroundings when using voice commands, as background noise can affect recognition accuracy.

## Future Enhancements

This assistant can be further developed to include:
- Integration with smart home devices for enhanced control.
- Natural language processing for more sophisticated command recognition.
- Scheduling features for reminders and calendar management.
- Customizable settings for voice preferences and responses.

## Conclusion

This J.A.R.V.I.S.-like personal assistant combines functionality and entertainment, providing a seamless interaction experience through voice commands and real-time information. Feel free to modify and expand upon this foundation to create your ultimate personal assistant!
