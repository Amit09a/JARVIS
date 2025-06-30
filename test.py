# Required libraries for hotword detection and audio input
import pvporcupine        # Porcupine library for hotword detection (e.g. "jarvis", "alexa")
import time               # Used for delays
import struct             # Used to unpack raw audio data from the microphone
import pyaudio            # To access microphone audio input
import pyautogui as autogui  # To simulate key presses
import platform           # To check operating system

def hotword():
    # Step 1: Initialize all components to None
    porcupine = None           # Will hold the hotword detection engine
    paud = None                # Will hold the PyAudio object
    audio_stream = None        # Will hold the live microphone stream

    try:
        # Step 2: Create the hotword detector with pre-trained keywords
        porcupine = pvporcupine.create(keywords=["jarvis", "alexa"])

        # Step 3: Initialize PyAudio (microphone input)
        paud = pyaudio.PyAudio()

        # Step 4: Open microphone stream using settings required by Porcupine
        audio_stream = paud.open(
            rate=porcupine.sample_rate,            # Use sample rate recommended by Porcupine
            channels=1,                             # Mono channel
            format=pyaudio.paInt16,                 # 16-bit audio format
            input=True,                             # We are using it for input (microphone)
            frames_per_buffer=porcupine.frame_length  # Size of each chunk to read from mic
        )

        # Step 5: Start a loop to constantly listen for hotwords
        while True:
            # Read a chunk of audio from the mic
            keyword = audio_stream.read(porcupine.frame_length, exception_on_overflow=False)

            # Convert the raw audio bytes to integers (required by Porcupine)
            keyword = struct.unpack_from("h" * porcupine.frame_length, keyword)

            # Send audio data to Porcupine for hotword detection
            keyword_index = porcupine.process(keyword)

            # If a hotword is detected (returns 0 or 1), take action
            if keyword_index >= 0:
                print("hotword detected")  # Print to console

                # Step 6: Simulate pressing shortcut key depending on OS
                os_type = platform.system().lower()
                if os_type == "darwin":  # macOS
                    autogui.keyDown("command")
                    autogui.press("j")
                    time.sleep(2)
                    autogui.keyUp("command")
                elif os_type == "windows":
                    autogui.keyDown("win")
                    autogui.press("j")
                    time.sleep(2)
                    autogui.keyUp("win")
                else:
                    print("OS not supported for hotkey simulation")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Step 7: Cleanup (whether error or normal stop)
        if porcupine is not None:
            porcupine.delete()         # Properly delete the Porcupine engine

        if audio_stream is not None:
            audio_stream.close()       # Close the audio stream

        if paud is not None:
            paud.terminate()           # Terminate PyAudio instance


# Step 8: Call the hotword function to start listening
hotword()