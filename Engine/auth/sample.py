import cv2
import os

# Open the camera using AVFOUNDATION for Mac
cam = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)
cam.set(3, 640)
cam.set(4, 480)

# Check if the camera opened successfully
if not cam.isOpened():
    print("❌ Error: Cannot open camera")
    exit()

# Load the Haar Cascade correctly (single forward slashes)
cascade_path = '/Users/amit/Desktop/JARVIS/Engine/auth/haarcascade_frontalface_default.xml'
detector = cv2.CascadeClassifier(cascade_path)

face_id = input("Enter a Numeric user ID here: ")

print("📸 Taking samples, look at the camera...")
count = 0

# Ensure the samples directory exists
samples_dir = 'Engine/auth/samples'
os.makedirs(samples_dir, exist_ok=True)

while True:
    ret, img = cam.read()

    if not ret or img is None:
        print("❌ Failed to capture frame")
        continue  # Skip this loop iteration

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = detector.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        count += 1

        face_img = gray[y:y + h, x:x + w]
        img_filename = f"{samples_dir}/face.{face_id}.{count}.jpg"
        cv2.imwrite(img_filename, face_img)

        cv2.imshow('Face Capture', img)

    k = cv2.waitKey(100) & 0xff
    if k == 27 or count >= 100:
        break

print("✅ Samples taken. Closing program...")
cam.release()
cv2.destroyAllWindows()
