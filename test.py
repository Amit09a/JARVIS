import cv2

cap = cv2.VideoCapture(0)  # try 1 or 2 if this doesn't work

if not cap.isOpened():
    print("❌ Could not open camera")
else:
    print("✅ Camera opened successfully")

ret, frame = cap.read()

if not ret:
    print("❌ Failed to grab frame")
else:
    cv2.imshow('Camera Test', frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

cap.release()
