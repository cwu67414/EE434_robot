import cv2

# Initialize the camera capture
left_camera = cv2.VideoCapture(0)  # Assuming left camera is index 0
right_camera = cv2.VideoCapture(1)  # Assuming right camera is index 1

# Set camera properties
# Adjust these parameters according to your camera specifications
left_camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
left_camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
right_camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
right_camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

while True:
    # Capture frames from the left and right cameras
    _, left_frame = left_camera.read()
    _, right_frame = right_camera.read()

    # Perform stereo vision processing here if needed
    # For example, calculate disparity map using stereo matching algorithms

    # Display stereo frames
    cv2.imshow('Left Camera', left_frame)
    cv2.imshow('Right Camera', right_frame)

    # Break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera resources
left_camera.release()
right_camera.release()
cv2.destroyAllWindows()