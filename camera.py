import cv2

# Initialize camera capture
cap_left = cv2.VideoCapture(0)
cap_right = cv2.VideoCapture(1)

while True:

    ret_left, frame_left = cap_left.read()
    ret_right, frame_right = cap_right.read()

    if not ret_left or not ret_right:
        print("Error: Failed to capture frame from one or both cameras")
        break

     cv2.imshow('Left Frame', frame_left)
    cv2.imshow('Right Frame', frame_right)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap_left.release()
cap_right.release()
cv2.destroyAllWindows()