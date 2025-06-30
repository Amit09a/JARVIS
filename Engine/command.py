import pyttsx3
import platform
import speech_recognition as sr
import time
import eel

def speak(text):
    system = platform.system()
    if system == 'Windows':
        engine = pyttsx3.init('sapi5')
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[1].id)
        engine.setProperty('rate', 180)  # Try adjusting this

        # if your system is linux, you can use 'espeak'
    elif system == 'Linux':
        engine = pyttsx3.init('espeak')
        voices = engine.getProperty('voices')
        engine.setProperty('rate', 180)  # Try adjusting this
        # Choose a specific better-sounding voice if available
        for voice in voices:
            if 'english' in voice.id.lower():  # or "en-us", etc.
                engine.setProperty('voice', voice.id)
                break


        # if your system is macOS, you can use 'nsss'
    elif system == 'Darwin': 
        flac_converter = "/opt/homebrew/bin/flac"
        engine = pyttsx3.init('nsss')
        voices = engine.getProperty('voices')
        engine.setProperty('rate', 180)  # Try adjusting this
        # Choose a specific better-sounding voice if available
        eel.DisplayMessage(text)
        for voice in voices:
            if 'samantha' in voice.id.lower():  # or "alex", etc.
                engine.setProperty('voice', voice.id)
                break


    else:
        engine = pyttsx3.init()  # fallback
    engine.say(text)
    engine.runAndWait()




def takeCommand():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        speak("welcome, I am your assistant, how can I help you?")
        print("Listening...")
        eel.DisplayMessage("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source,10,10)
    
    try:
        print("Recognizing...")
        eel.DisplayMessage("Recognizing...")
        command = recognizer.recognize_google(audio, language='en-in')
        print(f"User said: {command}\n")
        eel.DisplayMessage(command)
        time.sleep(2)
       
    except sr.UnknownValueError:
        print("Sorry, I did not understand that.")
        eel.DisplayMessage("Sorry, I did not understand that.")
        speak("Sorry, I did'nt understand that.")
        return ""
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
        return ""
    
    return command.lower()


@eel.expose
def allCommands():

    try:
        
        query = takeCommand()
        
        print(query)
        
        if 'open' in query:
            
           print("i run")
           from Engine.features import openCommand
           openCommand(query)

        elif 'on youtube':
           from Engine.features import PlayYoutube
           PlayYoutube(query)
        else:
           print("not run")
           
    except:
        print("error")

    eel.ShowHood()
