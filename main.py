import speech_recognition as sr
import webbrowser
import pyttsx3 
import time
import pywhatkit
import requests
from gtts import gTTS
# import pygame
# import os
import cohere
import re
import feedparser
import random
import google.generativeai as genai

#pip install pocketsphinx

#ye speech recognition functionality lene me help karti hai:
recognizer = sr.Recognizer()
engine = pyttsx3.init()  #To initialize pyttsx
engine.setProperty('rate', 180)  # Speech speed (try 160–200)
engine.setProperty('volume', 1)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


cohere_api_key = "knQOUXLgJ07R9DKhLGCTA9MUuOBeXK4pbPkmlOfP"
co = cohere.Client(cohere_api_key)

def speak(text):
    engine.say(text)
    engine.runAndWait()
    
def processCommand(c):
   
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open instagram" in c.lower():
        webbrowser.open("https://instagram.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    elif "open leetcode" in c.lower():
        webbrowser.open("https://leetcode.com")
    elif "open chatgpt" in c.lower():
        webbrowser.open("https://chatgpt.com")
    elif "open browser" in c.lower():
        webbrowser.open("https://chrome.com")

    elif "play" in c.lower():
        parts = c.lower().split("play", 1)
        song = parts[1].replace("song", "").strip() if len(parts) > 1 else ""
        print(f"Extracted song name: {song}")  # Debug
        if song:
            speak(f"Playing {song} from YouTube")
            pywhatkit.playonyt(song)
        else:
            speak("Please say the name of the song after 'play'")  

    elif "news" in c.lower():
        speak("Fetching the latest news headlines...")
        try:
            NewsFeed = feedparser.parse("http://feeds.bbci.co.uk/news/rss.xml")
            entries = NewsFeed.entries
            if not entries:
                speak("Sorry, I couldn't find any news at the moment.")
            else:
                for entry in entries[:5]:  # Only top 5 news
                    print("📰", entry.title)
                    speak(entry.title)
                    time.sleep(0.5)
        except Exception as e:
            print("⚠️ Error fetching or speaking news:", e)
            speak("Sorry, something went wrong while fetching the news.")
    
    elif "weather" in c.lower():
        match = re.search(r"weather (in|at|of)?\s*(.*)", c.lower())
        if match:
            city = match.group(2).strip()
            if city:
                get_weather(city)
            else:
                speak("Please say the name of the city after 'weather'.")
        else:
            speak("Sorry, I couldn't understand the city name.")

    elif "ask ai" in c.lower() or "explain" in c.lower() or "what is" in c.lower():
        ask_text = c.replace("ask ai", "").replace("explain", "").replace("what is", "").strip()
        if ask_text:
            ask_ai(ask_text)
        else:
            speak("Please say the question after saying 'ask AI' or 'explain'.")

    elif "i'm bored" in c.lower() or "talk to me" in c.lower():
        prompt = "Let's have a fun and casual conversation. Say something interesting or funny."
        response = ask_ai(prompt)
        speak(response)

    
    elif "exit" in c.lower() or "quit" in c.lower() or "shutdown" in c.lower() or "shut up" in c.lower() or "thank you" in c.lower() or "bye" in c.lower():
        goodbyes = [
            "Goodbye! Have a nice day!",
            "See you soon!",
            "Mission complete. Shutting down.",
            "Bye boss! Stay awesome!",
            "Jarvis signing off."
        ]
        farewell = random.choice(goodbyes)
        speak(farewell)
        print(f"👋 {farewell}")
        exit()


    
def get_weather(city_name):
    api_key = "679c6fc16f4f8165500630227dd1f92e"  
    base_url = "http://api.openweathermap.org/data/2.5/weather?"

 
    print(f"Checking weather for: {city_name}")
    # Adding country code (IN for India) along with city name
    country_code = "IN" 
    full_url = base_url + "appid=" + api_key + "&q=" + city_name + "," + country_code + "&units=metric" 
    response = requests.get(full_url)
    data = response.json()

    print("Weather API response:", data)

    if response.status_code == 200 and "main" in data:
        main = data["main"]
        weather = data["weather"][0]
        temperature = main["temp"]
        description = weather["description"]

        weather_report = f"The current temperature in {city_name.title()} is {temperature}°C with {description}."
        print(weather_report)
        speak(weather_report)
    elif data.get("message"):
        error_msg = f"Error: {data['message']}"
        print(error_msg)
        speak(f"Sorry, I couldn't fetch weather data. {data['message']}")

    elif data["cod"] != "404":
        main = data["main"]
        weather = data["weather"][0]
        temperature = main["temp"]
        description = weather["description"]

        weather_report = f"The current temperature in {city_name} is {temperature}°C with {description}."
        print(weather_report)
        speak(weather_report)
    else:
        print("❌ Unexpected response format.")
        speak("Sorry, something went wrong while fetching the weather.")


def ask_ai(question):
    try:
        response = co.generate(
            model='command-r-plus',
            prompt=question,
            max_tokens=100,
            temperature=0.7
        )
        reply = response.generations[0].text.strip()
        print("AI says:", reply)
        speak(reply)
    except Exception as e:
        print("Error using Cohere:", e)
        speak("Sorry, I couldn't reach the AI right now.")


def run_jarvis():
    print("JARVIS: Hello, how can I help you?")
    speak("Hello mam, how may I help you")
    

    while True:
        #Listen for the wake word Jarvis
        # obtain audio from the microphone
        # recognize speech using Sphinx

        print("Recognizing...")
        try:
            r = sr.Recognizer()
            with sr.Microphone() as source:
                print("🎤Listening...")
                r.adjust_for_ambient_noise(source, duration=0.5)
                audio = r.listen(source, timeout=7, phrase_time_limit=10)

            word = r.recognize_google(audio)
            print(f"You said : {word}")

            if "jarvis" in word.lower():
                speak("Yaa")
                # time.sleep(1)  #Give TTS time to speak
                command = word.lower().replace("jarvis", "").strip()
                if command:
                    processCommand(command)
                else:
                    speak("What can I do for you?")

            else:
                print("Wake word 'Jarvis' not found.")

        except Exception as e:
            import traceback
            print("Error:", e)
            traceback.print_exc()


if __name__ == "__main__":
    run_jarvis()

        
