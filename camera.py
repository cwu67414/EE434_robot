import cv2
#print(cv2.__version__)

cap = cv2.VideoCapture("nvarguscamerasrc ! video/x-raw(memory:NVMM), width=(int)1920, height=(int)1080, format=(string)NV12, framerate=(fraction)30/1 ! nvvidconv ! video/x-raw, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink")

while True:
    # Capture frames from the left and right cameras
    ret, frame = cap.read()

    # Perform stereo vision processing here if needed
    

    # Display the resulting frame
    cv2.imshow('Frame', frame)

    # Break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera resources
cap.release()
cv2.destroyAllWindows()