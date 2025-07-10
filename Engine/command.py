import pyttsx3
import platform
import speech_recognition as sr
import time
import eel
from Engine.chat_module import chatBot


def speak(text):
    system = platform.system()

    if system == 'Windows':
        engine = pyttsx3.init('sapi5')
    elif system == 'Linux':
        engine = pyttsx3.init('espeak')
    elif system == 'Darwin':
        engine = pyttsx3.init('nsss')
    else:
        engine = pyttsx3.init()

    voices = engine.getProperty('voices')
    engine.setProperty('rate', 180)

    for voice in voices:
        if any(name in voice.id.lower() for name in ['english', 'samantha', 'alex']):
            engine.setProperty('voice', voice.id)
            break
    eel.DisplayMessage(text) 

    eel.receiverText(text)  # ✅ Ensure response is shown on screen
    engine.say(text)
    engine.runAndWait()


def takeCommand():
    recognizer = sr.Recognizer()
    recognizer.energy_threshold = 500
    recognizer.pause_threshold = 1.0

    with sr.Microphone() as source:
        print("Listening...")
        eel.DisplayMessage("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=4)

        try:
            audio = recognizer.listen(source, timeout=8, phrase_time_limit=10)
        except sr.WaitTimeoutError:
            speak("I didn't hear anything. Please try again.")
            return ""

    try:
        print("Recognizing...")
        eel.DisplayMessage("Recognizing...")
        command = recognizer.recognize_google(audio, language='en-in')
        print(f"User said: {command}")
        eel.DisplayMessage(command)
        time.sleep(1)
        return command.lower()
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that. Could you please repeat?")
        return ""
    except sr.RequestError:
        speak("Network issue. Please check your internet.")
        return ""


@eel.expose
def allCommands(message=1):
    if message == 1:
        query = takeCommand()
        print(query)
        eel.senderText(query)
    else:
        query = str(message).lower().strip()
        eel.senderText(query)

    try:
        if not query:
            speak("I didn't hear anything. Please try again.")
            eel.receiverText("I didn't hear anything. Please try again.")  # ✅ Added to show text
            eel.ShowHood()
            return

        if any(word in query for word in ['open', 'launch', 'start']):
            from Engine.features import openCommand
            openCommand(query)
            eel.receiverText(f"Opening: {query}")  # ✅ Added feedback
            eel.ShowHood()
            return

        elif 'on youtube' in query:
            from Engine.features import PlayYoutube
            PlayYoutube(query)
            eel.receiverText(f"Playing on YouTube: {query}")  # ✅ Added feedback
            eel.ShowHood()
            return

        elif any(kw in query for kw in ["send message", "phone call", "video call", "call"]):
            from Engine.features import findContact, whatsApp, makeCall, sendMessage
            contact_no, name = findContact(query)

            if contact_no != 0:
                speak("Which mode do you want to use? WhatsApp or Mobile?")
                eel.receiverText("Which mode do you want to use? WhatsApp or Mobile?")  # ✅ Added
                preference = takeCommand()
                print(preference)

                if "mobile" in preference:
                    if "send message" in query or "send sms" in query:
                        speak("What message should I send?")
                        eel.receiverText("What message should I send?")  # ✅ Added
                        msg = takeCommand()
                        sendMessage(msg, contact_no, name)
                        eel.receiverText("Message sent.")
                        eel.ShowHood()
                    elif "phone call" in query or "call" in query:
                        makeCall(name, contact_no)
                        eel.receiverText("Calling now.")
                        eel.ShowHood()
                    else:
                        speak("Please try again.")
                        eel.receiverText("Please try again.")  # ✅ Added
                elif "whatsapp" in preference:
                    msg_type = ''
                    msg_content = ''
                    if "send message" in query:
                        msg_type = 'message'
                        speak("What message should I send?")
                        eel.receiverText("What message should I send?")  # ✅ Added
                        msg_content = takeCommand()
                    elif "phone call" in query:
                        msg_type = 'call'
                    elif "video call" in query:
                        msg_type = 'video call'
                    whatsApp(contact_no, msg_content, msg_type, name)
                    eel.receiverText("WhatsApp action completed.")  # ✅ Added
                else:
                    speak("I couldn't understand your preference.")
                    eel.receiverText("I couldn't understand your preference.")  # ✅ Added
                    eel.ShowHood()
            else:
                speak("I couldn't find the contact you mentioned.")
                eel.receiverText("Contact not found.")  # ✅ Added
                eel.ShowHood()

        else:
            reply = chatBot(query)
            speak(reply)
            eel.receiverText(reply)  # ✅ Already present
            eel.ShowHood()

    except Exception as e:
        print("Error:", e)
        speak("An error occurred while processing your command.")
        eel.receiverText("An error occurred.")
        eel.ShowHood()
