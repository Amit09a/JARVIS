# Engine/features.py

import hugchat
import pyttsx3
import platform
import speech_recognition as sr
import time
import os
import subprocess
import webbrowser
import sqlite3
import struct
import traceback
import eel
import pyaudio
import pvporcupine
import pyautogui
from shlex import quote
from playsound import playsound
import pywhatkit as kit

from Engine.helper import extract_yt_term, remove_words
from Engine.config import ASSISTANT_NAME
from Engine.command import speak

conn = sqlite3.connect('jarvis.db')
cursor = conn.cursor()

@eel.expose
def playAssistantSound():
    music_dir = "www/assets/audio/start_sound.mp3"
    playsound(music_dir)


def openCommand(query):
    system = platform.system()

    query = query.replace(ASSISTANT_NAME, "").replace("open", "").replace("app", "")
    app_name = ' '.join(query.lower().strip().split())

    if app_name == "":
        speak("I didn't understand what to open.")
        return

    try:
        cursor.execute("SELECT path FROM sys_command WHERE LOWER(name) LIKE ?", ('%' + app_name + '%',))
        results = cursor.fetchall()

        if results:
            speak("Opening " + app_name)
            if system == "Darwin":
                subprocess.call(['open', results[0][0]])
            elif system == "Windows":
                os.startfile(results[0][0])
            return

        cursor.execute("SELECT url FROM web_command WHERE LOWER(name) LIKE ?", ('%' + app_name + '%',))
        results = cursor.fetchall()

        if results:
            speak("Opening " + app_name)
            webbrowser.open(results[0][0])
            return

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
                f"{app_name}.exe"
            ]
            for path in possible_paths:
                if os.path.exists(path):
                    speak("Opening " + app_name)
                    os.startfile(path)
                    return

        if "." in app_name or app_name.startswith("http"):
            speak("Opening " + app_name)
            if not app_name.startswith("http"):
                app_name = "https://" + app_name
            webbrowser.open(app_name)
            return

        speak("Let me try opening " + app_name)
        if system == "Darwin":
            os.system(f'open -a "{app_name}"')
        elif system == "Windows":
            os.system(f'start "" "{app_name}"')

    except Exception as e:
        print("Error:", e)
        speak("Something went wrong while opening " + app_name)


def PlayYoutube(query):
    from Engine.helper import extract_yt_term
    search_term = extract_yt_term(query) or "something"
    speak("Playing " + search_term + " on YouTube")
    import pywhatkit as kit
    kit.playonyt(search_term)



@eel.expose
def hotword():
    access_key = "AcJZlmO1ioaLAXCnuSJ4sRW0Xg7wz8/cdgLfjrg+BCUEXuEuUkDVqQ=="
    porcupine = None
    paud = None
    audio_stream = None

    try:
        print("Initializing Porcupine...")
        porcupine = pvporcupine.create(
            access_key=access_key,
            keywords=["jarvis", "bumblebee"]
        )

        print("Opening microphone stream...")
        paud = pyaudio.PyAudio()
        audio_stream = paud.open(
            rate=porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=porcupine.frame_length
        )

        print("Listening for hotwords: 'jarvis', 'bumblebee'...")
        while True:
            pcm = audio_stream.read(porcupine.frame_length, exception_on_overflow=False)
            pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)
            keyword_index = porcupine.process(pcm)

            if keyword_index >= 0:
                print("Hotword detected!")

    except Exception as e:
        print("Error occurred:")
        traceback.print_exc()

    finally:
        print("Shutting down...")
        if audio_stream is not None:
            audio_stream.close()
        if paud is not None:
            paud.terminate()
        if porcupine is not None:
            porcupine.delete()


@eel.expose
def findContact(query):
    words_to_remove = [ASSISTANT_NAME, 'make', 'a', 'to', 'phone', 'call', 'send', 'message', 'wahtsapp', 'video']
    query = remove_words(query, words_to_remove).strip().lower()

    try:
        cursor.execute("SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))
        results = cursor.fetchall()

        if results:
            mobile_number_str = str(results[0][0])
            if not mobile_number_str.startswith('+91'):
                mobile_number_str = '+91' + mobile_number_str

            return mobile_number_str, query
        else:
            speak('Contact not found in database.')
            return 0, 0

    except Exception as e:
        print("Database error:", e)
        speak('An error occurred while searching for the contact.')
        return 0, 0



# Replace with real coordinates from pyautogui.position()
PHONE_ICON_X, PHONE_ICON_Y = 1179, 81
VIDEO_ICON_X, VIDEO_ICON_Y = 1135, 86
SEND_BUTTON_X, SEND_BUTTON_Y = 1221, 800  # 👉 Replace with actual send button coordinates

def whatsApp(mobile_no, message, flag, name):
    system_platform = platform.system()

    if flag == 'message':
        if not message.strip():
            speak("I didn't catch the message. Please try again.")
            return
        encoded_message = quote(message)
        whatsapp_url = f"whatsapp://send?phone={mobile_no}&text={encoded_message}"
        jarvis_message = f"Message sent successfully to {name}"

    else:
        whatsapp_url = f"whatsapp://send?phone={mobile_no}"
        if flag == 'call':
            jarvis_message = f"Calling {name}"
        else:
            jarvis_message = f"Starting video call with {name}"

    if system_platform == 'Windows':
        subprocess.run(f'start "" "{whatsapp_url}"', shell=True)
    elif system_platform == 'Darwin':
        subprocess.run(f'open "{whatsapp_url}"', shell=True)
    else:
        subprocess.run(f'xdg-open "{whatsapp_url}"', shell=True)

    time.sleep(5)  # Wait for WhatsApp to open

    if flag == 'call':
        pyautogui.click(PHONE_ICON_X, PHONE_ICON_Y)  # Voice Call
    elif flag == 'video call':
        pyautogui.click(VIDEO_ICON_X, VIDEO_ICON_Y)  # Video Call
    elif flag == 'message':
        pyautogui.click(SEND_BUTTON_X, SEND_BUTTON_Y)  # ✅ Send button click

    speak(jarvis_message)


def makeCall(name, mobileNo):
    mobileNo =mobileNo.replace(" ", "")
    speak("Calling "+name)
    command = 'adb shell am start -a android.intent.action.CALL -d tel:'+mobileNo
    os.system(command)


# to send message
def sendMessage(message, mobileNo, name):
    from Engine.helper import replace_spaces_with_percent_s, goback, keyEvent, tapEvents, adbInput
    message = replace_spaces_with_percent_s(message)
    mobileNo = replace_spaces_with_percent_s(mobileNo)
    speak("sending message")
    goback(4)
    time.sleep(1)
    keyEvent(3)
    # open sms app
    tapEvents(425,1968)
    #start chat
    tapEvents(846, 2202)
    # search mobile no
    adbInput(mobileNo)
    #tap on name
    tapEvents(543, 548)
    # tap on input
    tapEvents(235, 1396)
    #message
    adbInput(message)
    #send
    tapEvents(1001, 1351)
    speak("message send successfully to "+name)