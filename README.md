# Voice Assistant Program

This Python program implements a voice-controlled assistant that can perform various tasks using voice commands. It uses the Google Calendar API to fetch upcoming events from the user's Google Calendar, interacts with web services like YouTube and Google Maps, tells jokes, plays music, captures photos, and provides weather information.

## Features

- Greet the user based on the time of day (morning, afternoon, evening).
- Recognize and remember the user's name.
- Perform actions based on voice commands, such as:
  - Opening YouTube or Google.
  - Telling a joke.
  - Showing the current time.
  - Taking notes and displaying them.
  - Playing music.
  - Capturing photos.
  - Displaying the latest news.
  - Providing weather information for a specific city.
  - Fetching and displaying upcoming events from the user's Google Calendar.

## Prerequisites

Before running the program, make sure you have the following prerequisites:

- Python 3.x installed.
- Required Python libraries (use `pip install`):
  - google-api-python-client
  - google-auth-httplib2
  - google-auth-oauthlib
  - opencv-python
  - pyttsx3
  - pytz
  - speech_recognition
  - tkinter
  - PIL
  - requests

## Setup

1. Clone or download the repository.
2. Obtain the `credentials.json` file by setting up a Google Cloud project and enabling the Google Calendar API. Place the `credentials.json` file in the same directory as the script.
3. Run the `voice_assistant.py` script using a Python interpreter (`python voice_assistant.py`).

## Usage

- The program launches a graphical user interface (GUI) where you can see instructions and interact with the assistant.
- Click the "Speak" button to activate the voice recognition and issue commands.
- Use voice commands like "Open YouTube," "What time is it," "Tell me a joke," "Play music," etc.

## Note

- The program will prompt you for permissions to access your Google Calendar.
- Ensure that you have a working microphone for voice commands.
- Some features (e.g., Google Calendar, weather) may require an internet connection.


## Screenshots

![User Interface](/Screenshots/Picture1.gif)


## Author

Created by Kypros Andreou.


