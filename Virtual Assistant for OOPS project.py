import pyttsx3
import speech_recognition as sr
import webbrowser
import datetime
import wikipedia
import tkinter as tk
from tkinter import scrolledtext
import threading

# Global variable to control the listening state
listening = True

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening...')
        r.pause_threshold = 0.7
        audio = r.listen(source)
        try:
            print("Recognizing...")
            Query = r.recognize_google(audio, language='en-in')
            print("the command is printed=", Query)
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
            response_area.insert(tk.END, "Network error. Please check your connection.\n")
            return "None"
        except sr.UnknownValueError:
            print("Could not understand audio")
            response_area.insert(tk.END, "Could not understand the audio. Please try again.\n")
            return "None"
        except Exception as e:
            print(e)
            response_area.insert(tk.END, "An error occurred. Please try again.\n")
            return "None"
        return Query

def speak(audio):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.say(audio)
    engine.runAndWait()

def tellDay():
    day = datetime.datetime.today().weekday() + 1
    Day_dict = {1: 'Monday', 2: 'Tuesday', 3: 'Wednesday', 4: 'Thursday', 5: 'Friday', 6: 'Saturday', 7: 'Sunday'}
    if day in Day_dict.keys():
        day_of_the_week = Day_dict[day]
        print(day_of_the_week)
        speak("The day is " + day_of_the_week)
        response_area.insert(tk.END, "The day is " + day_of_the_week + "\n")

def tellTime():
    time = str(datetime.datetime.now())
    hour = time[11:13]
    min = time[14:16]
    speak("The time is " + hour + " Hours and " + min + " Minutes")
    response_area.insert(tk.END, "The time is " + hour + " Hours and " + min + " Minutes\n")

def Hello():
    speak("I am Oracle. Your desktop Assistant. Tell me how may I help you")
    response_area.insert(tk.END, "I am Oracle. Your desktop Assistant. Tell me how may I help you\n")

def Take_query():
    global listening
    Hello()
    while listening:
        query = takeCommand().lower()
        if query == "None":
            continue
        if "open youtube" in query:
            speak("Opening YouTube")
            webbrowser.open("www.youtube.com")
            continue
        elif "open google" in query:
            speak("Opening Google")
            webbrowser.open("www.google.com")
            continue
        elif "which day is it" in query:
            tellDay()
            continue
        elif "tell me the time" in query:
            tellTime()
            continue
        elif "thank" in query:
            speak("Bye sir, have a good day")
            exit()
        elif "from wikipedia" in query:
            speak("Checking the wikipedia")
            query = query.replace("wikipedia", "")
            result = wikipedia.summary(query, sentences=4)
            speak("According to wikipedia")
            speak(result)
            response_area.insert(tk.END, "According to Wikipedia: " + result + "\n")
        elif "hello" in query:
            speak("I am Oracle. Your desktop Assistant")
            response_area.insert(tk.END, "I am Oracle. Your desktop Assistant\n")

def start_query():
    global listening
    listening = True
    t = threading.Thread(target=Take_query)
    t.start()

def stop_query():
    global listening
    listening = False
    speak("Stopping listening")
    response_area.insert(tk.END, "Stopping listening\n")

# Tkinter setup
app = tk.Tk()
app.title("Oracle - Your Desktop Assistant")
app.geometry("500x600")

# Adding vibrant styles
app.configure(bg='#282c34')

# Title Label
title_label = tk.Label(app, text="Oracle - Your Desktop Assistant", font=("Helvetica", 16, "bold"), fg='#61dafb', bg='#282c34')
title_label.pack(pady=10)

# Scrollable text area for displaying responses
response_area = scrolledtext.ScrolledText(app, wrap=tk.WORD, width=50, height=15, font=("Helvetica", 12), bg='#1c1e22', fg='white')
response_area.pack(pady=10, padx=10)

# Button for starting query
start_button = tk.Button(app, text="Start Listening", font=("Helvetica", 14), bg='#61dafb', fg='#282c34', command=start_query)
start_button.pack(pady=10)

# Button for stopping query
stop_button = tk.Button(app, text="Stop Listening", font=("Helvetica", 14), bg='#ff6f61', fg='#282c34', command=stop_query)
stop_button.pack(pady=10)

# Run the app
app.mainloop()