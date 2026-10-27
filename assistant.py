import speech_recognition as sr
import pyttsx3
import webbrowser
import os
import time
import re
import threading

# ------------------- Text-to-Speech ------------------- #
def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# ------------------- Listen to User ------------------- #
def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎧 Listening...")
        audio = r.listen(source)
        try:
            command = r.recognize_google(audio).lower()
            print(f"🗣️ You said: {command}")
            return command
        except:
            return ""

# ------------------- Websites Dictionary ------------------- #
WEBSITES = {
    "youtube": "https://www.youtube.com",
    "google": "https://www.google.com",
    "gmail": "https://mail.google.com",
    "instagram": "https://www.instagram.com",
    "facebook": "https://www.facebook.com",
    "twitter": "https://twitter.com",
    "linkedin": "https://www.linkedin.com",
    "whatsapp_web": "https://web.whatsapp.com",
    "cuims": "https://cuims.cuchd.in",
    "amazon": "https://www.amazon.in",
    "flipkart": "https://www.flipkart.com",
    "meesho": "https://www.meesho.com",
    "canva": "https://www.canva.com",
    "myntra": "https://www.myntra.com",
    "ilovepdf": "https://www.ilovepdf.com",
}

# ------------------- Installed Apps Dictionary ------------------- #
INSTALLED_APPS = {
    "whatsapp": "5319275A.WhatsAppDesktop_cv1g1gvanyjgm!App",  # Microsoft Store WhatsApp
    "chrome": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
    "notepad": "notepad.exe",
    "calculator": "calc.exe",
}

# ------------------- Assistant Control ------------------- #
assistant_active = True  # Control variable to pause/resume listening

# ------------------- Open any website dynamically ------------------- #
def open_website(command):
    url_match = re.search(r'(https?://\S+|www\.\S+|\S+\.(com|in|org|net|edu|gov))', command)
    
    if url_match:
        url = url_match.group(0)
        if not url.startswith("http"):
            url = "https://" + url
        webbrowser.open(url)
        speak(f"Opening {url}")
        return True
    else:
        query = command.replace("open ", "").replace("start ", "")
        search_url = f"https://www.google.com/search?q={query}"
        webbrowser.open(search_url)
        speak(f"Searching online for {query}")
        return True

# ------------------- Open installed apps ------------------- #
def open_app(app_name):
    app_name = app_name.lower()
    if app_name in INSTALLED_APPS:
        path = INSTALLED_APPS[app_name]
        speak(f"Opening {app_name}")
        if "!" in path:
            os.system(f'explorer.exe shell:AppsFolder\\{path}')  # Microsoft Store App
        else:
            os.startfile(path)  # Normal exe
        return True
    return False

# ------------------- Main Assistant Function ------------------- #
def run_assistant():
    global assistant_active
    speak("Voice Assistant activated. How can I help?")
    while True:
        command = listen()  # always listen

        if command == "":
            continue

        # --------- Stop / Resume Assistant --------- #
        if "close assistant" in command:
            assistant_active = False
            speak("Assistant paused. Say 'open assistant' to resume.")
            continue
        elif "open assistant" in command:
            assistant_active = True
            speak("Assistant resumed. Listening now.")
            continue

        # If paused, skip all other commands
        if not assistant_active:
            continue

        # --------- Stop completely --------- #
        if "stop" in command or "exit" in command:
            speak("Goodbye!")
            break

        # --------- Open installed apps --------- #
        opened = False
        for app in INSTALLED_APPS:
            if app in command and ("start" in command or "open" in command):
                open_app(app)
                opened = True
                break
        if opened:
            continue

        # --------- Open predefined websites --------- #
        opened = False
        for site, url in WEBSITES.items():
            if site in command and ("open" in command or "start" in command):
                webbrowser.open(url)
                speak(f"Opening {site}")
                opened = True
                break
        if opened:
            continue

        # --------- Open any dynamic website --------- #
        if "open" in command or "start" in command:
            open_website(command)
            continue

        # --------- Check time --------- #
        elif "time" in command:
            current_time = time.strftime("%I:%M %p")
            speak(f"The time is {current_time}")

        # --------- Unknown command --------- #
        else:
            speak("Sorry, I didn't understand that command.")
