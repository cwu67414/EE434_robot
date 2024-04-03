import cv2
#print(cv2.__version__)

cap = cv2.VideoCapture(0)

while True:
    # Capture frames from the left and right cameras
    ret, frame = cap.read()

    # Perform stereo vision processing here if needed
    

    # Display the resulting frame
    cv2.imshow('Camera Feed', frame)

    # Break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera resources
cap.release()
cv2.destroyAllWindows()