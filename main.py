import os
import eel
from Engine.features import *
from Engine.command import *


eel.init("www")
    
playAssistantSound()

# open in app mode
os.system('open -a "Google Chrome" http://localhost:8000/index.html')
#telling to open this index.html file

eel.start('index.html',mode=None,host='localhost',block=True)