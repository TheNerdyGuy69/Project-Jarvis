import speech_recognition as sr
import pyttsx3
import webbrowser
from musicLibrary import music
import os
import requests
import openai

# Initialize recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Fetch API keys from environment variables
NEWS_API_KEY = os.getenv('NEWS_API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Check if the API keys are loaded
if not NEWS_API_KEY:
    raise ValueError("NEWS_API_KEY environment variable not set.")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable not set.")

openai.api_key = OPENAI_API_KEY

def speak(text):
    engine.say(text)
    engine.runAndWait()

def open_website(command):
    websites = {
        "google": "https://google.com",
        "youtube": "https://youtube.com",
        "facebook": "https://facebook.com",
        "linkedin": "https://linkedin.com",
        "x": "https://x.com",
        "chatgpt": "https://chatgpt.com"
    }
    for site in websites:
        if f"open {site}" in command.lower():
            webbrowser.open(websites[site])
            return

def play_song(command):
    songs = {
        "wanna be yours": music["i wanna be yours"],
        "skyfall": music["skyfall"],
        "houdini": music["houdini"],
        "die for you": music["die for you"]
    }
    for song in songs:
        if f"play {song}" in command.lower():
            webbrowser.open(songs[song])
            return

def fetch_news(command):
    try:
        url = f'https://newsapi.org/v2/top-headlines?country=us&apiKey={NEWS_API_KEY}'
        response = requests.get(url)
        news_data = response.json()

        if news_data['status'] == 'ok':
            if news_data['totalResults'] > 0:
                for article in news_data['articles']:
                    speak(article['title'])
            else:
                speak("I couldn't find any news articles at the moment.")
        else:
            speak("I couldn't fetch the news at the moment.")
    except Exception as e:
        print(f"Error fetching news: {e}")
        speak("I couldn't fetch the news at the moment.")

def ai(command):
    try:
        client = openai.OpenAI(
        # This is the default and can be omitted
        api_key=os.environ.get("OPENAI_API_KEY"),
        )

        response= client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"{command}",
            }
        ],
        model="gpt-3.5-turbo",
        )
        response_text =  response.choices[0].message['content'].strip()
        speak(response_text)
    except Exception as e:
        print(f"Error interacting with OpenAI: {e}")
        speak("I couldn't process your request at the moment.")

if __name__ == "__main__":
    speak("Initializing Jarvis...")

    while True:
        try:
            with sr.Microphone() as source:
                print("Listening...")
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source, timeout=5)
                word = recognizer.recognize_google(audio)
                
            if word.lower() == "jarvis":
                speak("Hello Sir, Jarvis at your service")
                
                with sr.Microphone() as source:
                    print("Speak...")
                    recognizer.adjust_for_ambient_noise(source)
                    audio = recognizer.listen(source, timeout=5)
                    print("Recognizing...")
                    command = recognizer.recognize_google(audio)
                    
                    if "open" in command.lower():
                        open_website(command)
                    elif "play" in command.lower():
                        play_song(command)
                    elif "news" in command.lower():
                        fetch_news(command)
                    else:
                        ai(command)
        
        except sr.UnknownValueError:
            print("Jarvis could not understand the audio")
        except sr.RequestError as e:
            print(f"Could not request results from Jarvis service; {e}")
        except Exception as e:
            print(f"Error: {e}")
