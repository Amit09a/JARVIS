import cv2
import time
import os

def AuthenticateFace():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    model_path = 'Engine/auth/trainer/trainer.yml'
    cascade_path = 'Engine/auth/haarcascade_frontalface_default.xml'

    if not os.path.exists(model_path):
        print("❌ Trained model not found. Please run the training script first.")
        return 0

    recognizer.read(model_path)
    faceCascade = cv2.CascadeClassifier(cascade_path)

    font = cv2.FONT_HERSHEY_SIMPLEX
    names = ['', 'Amit']  # Adjust names as needed

    cam = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)
    cam.set(3, 640)
    cam.set(4, 480)

    if not cam.isOpened():
        print("❌ Cannot open camera.")
        return 0

    minW = 0.1 * cam.get(3)
    minH = 0.1 * cam.get(4)

    flag = 0

    print("🔍 Face authentication started...")

    while True:
        ret, img = cam.read()
        if not ret or img is None:
            print("❌ Failed to capture frame.")
            continue

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(int(minW), int(minH)))

        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

            id, confidence = recognizer.predict(gray[y:y + h, x:x + w])

            if confidence < 100:
                name = names[id] if id < len(names) else "Unknown"
                accuracy = f"{round(100 - confidence)}%"
                flag = 1
            else:
                name = "Unknown"
                accuracy = f"{round(100 - confidence)}%"
                flag = 0

            cv2.putText(img, str(name), (x + 5, y - 5), font, 1, (255, 255, 255), 2)
            cv2.putText(img, str(accuracy), (x + 5, y + h - 5), font, 1, (255, 255, 0), 1)

        cv2.imshow('Face Authentication', img)

        # Exit only when face is recognized
        if flag == 1:
            print("✅ Face recognized! Closing in 2 seconds...")
            cv2.waitKey(2000)  # Wait 2 seconds to let user see
            break

    cam.release()
    cv2.destroyAllWindows()

    if flag == 1:
        print("✅ Authentication successful.")
    else:
        print("❌ Authentication failed.")

    return flag

