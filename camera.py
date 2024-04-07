import cv2

for index in range(4):  # Try indices from 0 to 3 (or higher if needed)
    cap = cv2.VideoCapture(index)
    if not cap.isOpened():
        print(f"Camera {index} not available")
    else:
        print(f"Camera {index} is available")
cap.release()  # Release the camera
break  # Exit loop if a camera is found
    
