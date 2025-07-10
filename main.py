import os
import eel
from Engine.features import *
from Engine.command import *
from Engine.auth import recoganize


def start():
    eel.init("www")
    playAssistantSound()
    
    @eel.expose
    def init():
        eel.hideLoader()()
        speak("Ready for face Authentication")
        flag = recoganize.AuthenticateFace()
        if flag == 1:
            eel.hideFaceAuth()
            speak("Face Authentication Successful")
            eel.hideFaceAuthSuccess()
            speak("Hello, welcome sir How can I help you today?")
            # Here you can call any function to start the main functionality of JARVIS
            # For example, you can call a function to listen for commands or start a conversation
            # listenForCommands()  # Uncomment this line if you have a function to listen for commands
            eel.hideStart()
            playAssistantSound()
        else:
            speak("Face Authentication Failed")
            speak("Please try again")
            init()

    # open in app mode
    os.system('open -a "Google Chrome" http://localhost:8000/index.html')
    #telling to open this index.html file

    eel.start('index.html',mode=None,host='localhost',block=True)