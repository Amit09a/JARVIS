import cv2
import numpy as np
from PIL import Image
import os

samples_path = 'Engine/auth/samples'
trainer_path = 'Engine/auth/trainer/trainer.yml'
cascade_path = '/Users/amit/Desktop/JARVIS/Engine/auth/haarcascade_frontalface_default.xml'

recognizer = cv2.face.LBPHFaceRecognizer_create()
detector = cv2.CascadeClassifier(cascade_path)

def Images_And_Labels(path):
    if not os.path.exists(path):
        print(f"❌ Samples folder not found: {path}")
        return [], []

    imagePaths = [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.jpg')]
    if not imagePaths:
        print("❌ No images found in the samples folder.")
        return [], []

    faceSamples = []
    ids = []

    for imagePath in imagePaths:
        gray_img = Image.open(imagePath).convert('L')
        img_arr = np.array(gray_img, 'uint8')

        try:
            id = int(os.path.split(imagePath)[-1].split(".")[1])
        except (IndexError, ValueError):
            print(f"⚠️ Skipping invalid file: {imagePath}")
            continue

        faces = detector.detectMultiScale(img_arr)

        for (x, y, w, h) in faces:
            faceSamples.append(img_arr[y:y + h, x:x + w])
            ids.append(id)

    return faceSamples, ids

print("📢 Training faces. It will take a few seconds. Please wait...")

faces, ids = Images_And_Labels(samples_path)

if faces and ids:
    os.makedirs(os.path.dirname(trainer_path), exist_ok=True)
    recognizer.train(faces, np.array(ids))
    recognizer.write(trainer_path)
    print("✅ Model trained successfully. Ready for face recognition.")
else:
    print("❌ Training aborted: No valid faces or IDs found.")
