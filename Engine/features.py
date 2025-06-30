import re
import platform
import struct
import time
from playsound import playsound
import eel
import pvporcupine
import pyaudio
from Engine import command
from Engine.config import ASSISTANT_NAME
import os 
from Engine.command import speak
import pywhatkit as kit
from Engine.db import cursor
import webbrowser   
import sqlite3
import subprocess

from Engine.helper import extract_yt_term

conn = sqlite3.connect('jarvis.db')
cursor = conn.cursor()


@eel.expose
def playAssistantSound():
    music_dir = "www/assets/audio/start_sound.mp3"
    playsound(music_dir)  


def openCommand(query):
    system = platform.system()  # Detect OS: 'Darwin', 'Windows', 'Linux'

    # Clean the spoken query
    query = query.replace(ASSISTANT_NAME, "")
    query = query.replace("open", "")
    query = query.replace("app", "")
    app_name = ' '.join(query.lower().strip().split())  # Normalize spaces

    if app_name == "":
        speak("I didn't understand what to open.")
        return

    try:
        # Try system command from DB
        cursor.execute(
            "SELECT path FROM sys_command WHERE LOWER(name) LIKE ?",
            ('%' + app_name + '%',)
        )
        results = cursor.fetchall()

        if results:
            speak("Opening " + app_name)
            if system == "Darwin":  # macOS
                subprocess.call(['open', results[0][0]])
            elif system == "Windows":
                os.startfile(results[0][0])
            return

        # Try web command from DB
        cursor.execute(
            "SELECT url FROM web_command WHERE LOWER(name) LIKE ?",
            ('%' + app_name + '%',)
        )
        results = cursor.fetchall()

        if results:
            speak("Opening " + app_name)
            webbrowser.open(results[0][0])
            return

        # Try default system app location
        if system == "Darwin":
            app_path = f"/Applications/{app_name}.app"
            if os.path.exists(app_path):
                speak("Opening " + app_name)
                subprocess.call(["open", app_path])
                return
        elif system == "Windows":
            possible_paths = [
                f"C:\\Program Files\\{app_name}\\{app_name}.exe",
                f"C:\\Program Files (x86)\\{app_name}\\{app_name}.exe",
                f"{app_name}.exe"  # If it's just in PATH or same folder
            ]
            for path in possible_paths:
                if os.path.exists(path):
                    speak("Opening " + app_name)
                    os.startfile(path)
                    return

        # Try as URL if it looks like one
        if "." in app_name or app_name.startswith("http"):
            speak("Opening " + app_name)
            if not app_name.startswith("http"):
                app_name = "https://" + app_name
            webbrowser.open(app_name)
            return

        # ✅ Final fallback: try OS-level name resolution
        speak("Let me try opening " + app_name)
        if system == "Darwin":
            os.system(f'open -a "{app_name}"')
        elif system == "Windows":
            os.system(f'start "" "{app_name}"')

    except Exception as e:
        print("Error:", e)
        speak("Something went wrong while opening " + app_name)


def PlayYoutube(query):
    search_term = extract_yt_term(query)
    speak("Playing " + search_term + " on YouTube")
    kit.playonyt(search_term)


def hotword():
    porcupine=None
    paud=None
    audio_stream=None
    try:
       
        # pre trained keywords    
        porcupine=pvporcupine.create(keywords=["jarvis","alexa","Bumblebee"]) 
        paud=pyaudio.PyAudio()
        #stream microphone in background
        audio_stream=paud.open(rate=porcupine.sample_rate,channels=1,format=pyaudio.paInt16,input=True,frames_per_buffer=porcupine.frame_length)
        
        # loop for streaming of microphone continuously
        while True:
            keyword=audio_stream.read(porcupine.frame_length)
            keyword=struct.unpack_from("h"*porcupine.frame_length,keyword)

            # processing keyword comes from mic 
            keyword_index=porcupine.process(keyword)

            # checking first keyword detetcted for not
            if keyword_index>=0:
                print("hotword detected")

                # pressing shorcut key win+j
                import pyautogui as autogui
                autogui.keyDown("win")
                autogui.press("j")
                time.sleep(2)
                autogui.keyUp("win")
                
    except:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if paud is not None:
            paud.terminate()