import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import wikipedia
import requests
import smtplib
import time

# ================== INITIAL SETUP ==================
engine = pyttsx3.init()
engine.setProperty('rate', 170)

recognizer = sr.Recognizer()

ASSISTANT_NAME = "Nova"
USER_NAME = "User"

# ================== SPEAK FUNCTION ==================
def speak(text):
    print(f"{ASSISTANT_NAME}: {text}")
    engine.say(text)
    engine.runAndWait()

# ================== LISTEN FUNCTION ==================
def listen():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio)
        print(f"{USER_NAME}: {command}")
        return command.lower()
    except sr.UnknownValueError:
        speak("Sorry, I didn't understand that.")
        return ""
    except sr.RequestError:
        speak("Network error.")
        return ""

# ================== TIME & DATE ==================
def tell_time():
    time_now = datetime.datetime.now().strftime("%I:%M %p")
    speak(f"The time is {time_now}")

def tell_date():
    date_today = datetime.date.today().strftime("%B %d, %Y")
    speak(f"Today's date is {date_today}")

# ================== WEB SEARCH ==================
def search_web(query):
    speak("Searching the web")
    webbrowser.open(f"https://www.google.com/search?q={query}")

# ================== WIKIPEDIA SEARCH ==================
def wiki_search(query):
    try:
        result = wikipedia.summary(query, sentences=2)
        speak(result)
    except:
        speak("I couldn't find information on that.")

# ================== WEATHER ==================
def get_weather(city):
    API_KEY = "YOUR_API_KEY"  # OpenWeather API
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    
    try:
        data = requests.get(url).json()
        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"]
        speak(f"The temperature in {city} is {temp} degrees with {desc}")
    except:
        speak("Unable to fetch weather data")

# ================== EMAIL ==================
def send_email(to_email, message):
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login("YOUR_EMAIL@gmail.com", "YOUR_APP_PASSWORD")
        server.sendmail("YOUR_EMAIL@gmail.com", to_email, message)
        server.quit()
        speak("Email sent successfully")
    except:
        speak("Failed to send email")

# ================== REMINDER ==================
def set_reminder(seconds, message):
    speak(f"Reminder set for {seconds} seconds")
    time.sleep(seconds)
    speak(message)

# ================== COMMAND PROCESSING ==================
def process_command(command):

    if "hello" in command or "hi" in command:
        speak("Hello! How can I help you?")

    elif "time" in command:
        tell_time()

    elif "date" in command:
        tell_date()

    elif "search" in command:
        query = command.replace("search", "")
        search_web(query)

    elif "wikipedia" in command:
        query = command.replace("wikipedia", "")
        wiki_search(query)

    elif "weather" in command:
        speak("Which city?")
        city = listen()
        get_weather(city)

    elif "send email" in command:
        speak("Tell me the message")
        message = listen()
        send_email("receiver@gmail.com", message)

    elif "set reminder" in command:
        speak("After how many seconds?")
        seconds = int(listen())
        speak("What should I remind you?")
        msg = listen()
        set_reminder(seconds, msg)

    elif "your name" in command:
        speak(f"My name is {ASSISTANT_NAME}")

    elif "change my name to" in command:
        global USER_NAME
        USER_NAME = command.replace("change my name to", "").strip()
        speak(f"Okay, I will call you {USER_NAME}")

    elif "stop" in command or "bye" in command:
        speak("Goodbye! Have a great day.")
        exit()

    else:
        speak("Sorry, I can't do that yet.")

# ================== MAIN LOOP ==================
def run_assistant():
    speak(f"{ASSISTANT_NAME} is now online")
    while True:
        command = listen()
        if command:
            process_command(command)

# ================== START ==================
run_assistant()
