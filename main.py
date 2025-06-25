import os
import eel

eel.init("www")
# open in app mode
os.system('start msedge.exe --app="http://localhost:8000/index.html"')
#telling to open this index.html file

eel.start('index.html',mode=None,host='localhost',block=True)