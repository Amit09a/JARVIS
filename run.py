
import multiprocessing
import subprocess
import eel

def startJarvis():
    # Code for process 1
    print("Process 1 is running.")
    from main import start
    start()
    
    
# To run hotword
def listenHotword():
     # Code for process 2
    print("Process 2 is running.")
    from Engine.features import hotword
    hotword()
    
# Start both processes
if __name__ == '__main__':
    
    p1 = multiprocessing.Process(target=startJarvis)
    p2 = multiprocessing.Process(target=listenHotword)
    p1.start()
    subprocess.call(['/Users/amit/Desktop/JARVIS/device.sh'])
    p2.start()
    p1.join()

    if p2.is_alive():
        p2.terminate()
        p2.join()

        print("system stop")   