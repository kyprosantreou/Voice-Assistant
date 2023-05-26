#Βιβλιοθήκες Googole Calendar
from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import datetime #Βιβλιοθήκη για ημερομηνία και ώρα
import os       #Βιβλιοθήκη για άνοιγμα εφαρμογών
import random   #Βιβλιοθήκη για αναπαραγωγή τυχαίων
import shutil   #Βιβλιοθήκη για αρχέια
import webbrowser #Βιβλιοθήκη για άνοιγμα url
from time import ctime  # Βιβλιοθήκη για ημερομηνία και ώρα
import cv2              #Βιβλιοθήκξξη για ανοιγμα κάμερας

import pyjokes #βιβλιοθήκη για ανέκδοτα
import pyttsx3 #Βιβλιοθήκη μετατροπής ομιλίας σε κείμενο
import pytz
import speech_recognition as sr #Βιβλιοθήκη για αναγνώριση φωνής

#βιβλιοθήκες για το GUI
import tkinter as tk
from tkinter import *
from PIL import Image

import requests
import math

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

MONTHS = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]
DAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
DAY_EXTENTIONS = ["rd", "th", "st", "nd"]

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)



#Συνάρτηση για την φωνή του προγράμματος
def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning !")

    elif hour >= 12 and hour < 18:
        speak("Good Afternoon !")

    else:
        speak("Good Evening !")

    assname = "Notis the lord"
    speak("I am your Assistant")
    speak(assname)

#Συνάρτηση για να δώσει ο χρήστης Username
def username():
    speak("What should i call you sir")
    uname = takeCommand()#Το uname παίρνει το όνομα που θα πει ο χρήστης
    speak("Welcome ")
    speak(uname)
    columns = shutil.get_terminal_size().columns

    print("#####################".center(columns))
    print("Welcome.",uname.center(columns))
    print("#####################".center(columns))

    speak("How can i Help you? ")

#Συνάρτηση για άνοιγμα της κάμερας και λήψης φωτογραφίας
def capture_image():
    cam = cv2.VideoCapture(0)
    count =0
    while True:
        ret, img = cam.read()
        cv2.imshow("Notis Camera", img)

        if not ret:
            break

        k = cv2.waitKey(1)

        if k % 256 == 27: #Οταν πατήσει ο χρήστης το esc η κάμερα κλέινει
            break
        elif k % 256 == 32: #Οταν πατήσει ο χρήστης το space η κάμερα κλέινει
            file="My_photo" + str(count)+'.jpg'
            cv2.imwrite(file, img)
            count +=1
    cam.release()
    cv2.destroyAllWindows()

def takeCommand(): #Συνάρτηση η οποία πέρνει την ομιλία του χρήστη απο το μικρόφωνο και το μετατρέπει σε γραπτό κείμενο για να μπορεί να το αναγνωρίσει το πρόγραμμα
    r = sr.Recognizer()

    with sr.Microphone() as source:

        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en')
        print(f"User said: {query}\n")

    except Exception as e: #Σε περίπτωση που δεν αναγνωρίσει την φωνή εκτυπώνει στην οθώνη το πάρακατω μύνημα
        print(e)
        print("Unable to Recognize your voice.")
        return "None"

    return query

#Συνάρτηση για την αυτόματη σύνδεση στον λογαριασμό google τον οποίο χρησημοποιεί το ημερολόγιο
def authenticate_google():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    return service

#Συνάρτηση η οποία παίρνει και εμφανίζει τα events απο το google calendar μετα την κατάλληλη φωνιτηκή εντολή
def get_events(day, service):
    date = datetime.datetime.combine(day, datetime.datetime.min.time())
    end_date = datetime.datetime.combine(day, datetime.datetime.max.time())
    utc = pytz.UTC
    date = date.astimezone(utc)
    end_date = end_date.astimezone(utc)

    events_result = service.events().list(calendarId='primary', timeMin=date.isoformat(), timeMax=end_date.isoformat(),singleEvents=True,orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        speak('No upcoming events found.')
    else:
        speak(f"You have {len(events)} events on this day.")

        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])
            start_time = str(start.split("T")[1].split("-")[0])
            if int(start_time.split(":")[0]) < 12:
                start_time = start_time + "am"
            else:
                start_time = str(int(start_time.split(":")[0]) - 12)
                start_time = start_time + "pm"

            speak(event["summary"] + " at " + start_time)

#Συνάρτηση η οποία αναγνωρίζει μέσα απο τα λόγια του χρήστη την ημερομηνία, μέρα , μήνα για να εμφανίσει τα ανάλογα events του ημερολογίου
def get_date(text):
    text = text.lower()
    today = datetime.date.today()

    if text.count("today") > 0:
        return today

    day = -1
    day_of_week = -1
    month = -1
    year = today.year

    for word in text.split():
        if word in MONTHS:
            month = MONTHS.index(word) + 1
        elif word in DAYS:
            day_of_week = DAYS.index(word)
        elif word.isdigit():
            day = int(word)
        else:
            for ext in DAY_EXTENTIONS:
                found = word.find(ext)
                if found > 0:
                    try:
                        day = int(word[:found])
                    except:
                        pass

    if month < today.month and month != -1:
        year = year + 1

    if month == -1 and day != -1:
        if day < today.day:
            month = today.month + 1
        else:
            month = today.month

    if month == -1 and day == -1 and day_of_week != -1:
        current_day_of_week = today.weekday()
        dif = day_of_week - current_day_of_week

        if dif < 0:
            dif += 7
            if text.count("next") >= 1:
                dif += 7

        return today + datetime.timedelta(dif)

    if day != -1:
        return datetime.date(month=month, day=day, year=year)


#Κλάση για να μπορεί να λειτουργήσει το GUI της εφαρμογής
class Widget:
    def __init__(self):
        root = tk.Tk() #δημιουργία παραθήρου
        file = 'djmix3.gif' #η φωτογραφία που χρησημοποιείται
        root.geometry('700x570')#οι διαστάσεις του παραθήρου
        root.title("Voice assistant")#το όνομα του παραθήρου
        root.iconbitmap('favicon.ico')#το εικονίδιο του παραθήρου
        root.configure(bg='black')#το χρώμα του φόντου

        info = Image.open(file) # εντολή ανοίγματος της φωτογραφίας
        frames = info.n_frames # δίαβασμα του ρυθμού ανανέωσης της εικόνας(frames)

        im = [tk.PhotoImage(file=file, format=f'gif -index {i}') for i in range(frames)]

        anim = None
        count = 0

        def animation(count): #συνάρτηση η οποία κάνει το gif(εικόνα) να κινήται
            global anim
            im2 = im[count]
            gif_label.configure(image=im2)

            count += 1
            if count == frames:
                count = 0

            anim = root.after(150, lambda: animation(count))

        gif_label = tk.Label(image="")
        gif_label.pack(side=RIGHT)

        compText = StringVar()
        userText = StringVar()
        #αριστερό μμέρος παραθήρου με τις οδηγίες
        userText.set('QUESTIONS / COMMANDS:\n--------------------------------\nTell me a joke\nCoin\nWhat time is it?\nTake a note\nOpen google\nOpen youtube\nLocate\nSearch\nShow notes\nPlay music\nTake photo\nNews\nWhat do i have?\nDo i have any plans?\nAm i busy?\nWeather\n')
        userFrame = LabelFrame(root, text='Notis The Lord', font=('Railways', 24, 'bold'))

        top = Message(userFrame, textvariable=userText, bg='black', fg='white')
        top.config(font=("Century Gothic", 15, 'bold'))
        #κουμπί speak
        btn = Button(root, text='Speak', font=('railways', 15, 'bold'), bg='blue', fg='white', command=self.clicked)
        #κουμπί exit
        btn2 = Button(root, text='Close', font=('railways', 15, 'bold'), bg='red', fg='white', command=exit)

        btn2.pack(side=BOTTOM)
        btn.pack(side=BOTTOM)

        userFrame.pack(fill='both', expand=1, side=RIGHT)
        top.pack(side='top', fill='both', expand=1)

        animation(count)

        wishMe()
        username()
        root.mainloop()

    #συνάρτηση η οπία ενεργοποιεί το κουμπί speak και λαμβάνει τις φωνιτηκές εντολες του χρήστη για την εκτέλεση τους
    def clicked(self):
        query = takeCommand().lower()

        if 'open youtube' in query:
            speak("Here you go to Youtube\n")
            webbrowser.open("youtube.com")

        elif 'what time is it' in query:
            speak(ctime())

        elif 'tell me a joke' in query:
            speak(pyjokes.get_joke())

        elif 'i love you' in query:
            speak("I love you too")
            webbrowser.open("https://www.youtube.com/watch?v=KYV7PyULmrM")

        elif "hi" in query:
            wishMe()
            speak("Notis the lord in your service ")

        elif 'what is your name' in query:
            speak('My name is Bond, James  bond')

        elif 'play music' in query:
            speak('Sit back and relax')
            n = random.randint(0, 643)
            music = "C:\\Users\\kypro\\Documents\\Python Programs\\pythonProject\\music"
            songs = os.listdir(music)
            print(songs)
            os.startfile(os.path.join(music, songs[n]))

        elif 'open google' in query:
            speak('Here you go to google')
            webbrowser.open("https://www.google.com/")

        elif 'coin' in query:
            moves = ['head', 'tails']
            cmove = random.choice(moves)
            speak('The computer chose' + cmove)

        elif 'search' in query:
            speak('What do you want to search for ?')
            search = takeCommand()
            url = 'https://google.com/search?q=' + search
            webbrowser.get().open(url)
            speak('Here is what i found' + search)

        elif 'take a note' in query:
            speak('What i should write?')
            note = takeCommand()
            file = open('Mynote.txt', 'w')
            file.write(note)

        elif 'show notes' in query:
            speak('Showing your notes')
            file = open('Mynote.txt', 'r')
            speak(file.read(100000))
            os.startfile('Mynote.txt')

        elif 'show my notes' in query:
            speak('Showing your notes')
            file = open('Mynote.txt', 'r')
            speak(file.read(100000))
            os.startfile('Mynote.txt')

        elif 'show my note' in query:
            speak('Showing your notes')
            file = open('Mynote.txt', 'r')
            speak(file.read(100000))
            os.startfile('Mynote.txt')

        elif 'show note' in query:
            speak('Showing your notes')
            file = open('Mynote.txt', 'r')
            speak(file.read(100000))
            os.startfile('Mynote.txt')

        elif 'locate' in query:
            location = takeCommand()
            speak("User asked to Locate")
            speak(location)
            webbrowser.open("https://www.google.com/maps/place/" + location + "")

        elif 'take photo' in query:
            speak("Press escape to exit,or space to take photo")
            capture_image()

        elif 'news' in query:
            speak("Here are the latest news!")
            webbrowser.open("https://www.bbc.com/news")

        elif "weather" in query:

            api_key = "004ca73d6e1481faa9258db49ddda417"

            speak("In which city? ")

            city_name = takeCommand()

            base_url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}"

            response = requests.get(base_url)

            x = response.json()

            if x["cod"] != "404":

                y = x["main"]

                current_temperature = y["temp"]
                current_temperature = math.floor(current_temperature - 273.15)

                current_humidiy = y["humidity"]

                z = x["weather"]

                weather_description = z[0]["description"]

                speak("The current temperature is")
                speak(current_temperature)
                speak("celsius")
                speak(" And The current humidity level is")
                speak(current_humidiy)
                speak("percent")
            else:
                speak(" City Not Found ")

        elif "calendar" in query:

            SERVICE = authenticate_google()
            text = takeCommand()
            date = get_date(text)
            if date:
                get_events(date, SERVICE)
            else:
                speak("Please Try Again")

        elif 'exit' or 'close' in query:
            speak("Have a nice day")
            exit()
        else:
            speak("Try again")
            takeCommand()


if __name__ == '__main__':
    widget = Widget()


