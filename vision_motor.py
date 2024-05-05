import cv2
import math

arm_length = 17

def convert_to_angles(a, b, c):
    angle1 = math.atan2(a, b) * (180 / math.pi)
    angle2 = math.atan2(c, b) + math.acos(math.sqrt(b**2 + c**2) / (2 * arm_length))
    angle3 = 2 * angle2 - 180
    
    return angle1, angle2, angle3

# Initialize camera capture
cap0 = cv2.VideoCapture("nvarguscamerasrc sensor_id=0 ! video/x-raw(memory:NVMM), width=(int)1920, height=(int)1080, format=(string)NV12, framerate=(fraction)30/1 ! nvvidconv ! video/x-raw, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink")
cap1 = cv2.VideoCapture("nvarguscamerasrc sensor_id=1 ! video/x-raw(memory:NVMM), width=(int)1920, height=(int)1080, format=(string)NV12, framerate=(fraction)30/1 ! nvvidconv ! video/x-raw, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink")

while True:

    ret0, frame0 = cap0.read()
    ret1, frame1 = cap1.read()

    x0, y0, z0 = 10, 20, 30
    x1, y1, z1 = 15, 25, 35

    angles = convert_to_angles((x0+x1)/2, (y0+y1)/2, (z0+z1)/2)
    print("Angle 1:", angles[0])
    print("Angle 2:", angles[1])
    print("Angle 3:", angles[2])

    cv2.imshow('Frame0', frame0)
    cv2.imshow('Frame1', frame1)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap0.release()
cap1.release()
cv2.destroyAllWindows()


gst-launch-1.0 nvarguscamerasrc sensor_id=0 ! \
   'video/x-raw(memory:NVMM),width=1920, height=1080, framerate=30/1' ! \
   nvvidconv flip-method=0 ! 'video/x-raw,width=960, height=540' ! \
   nvvidconv ! nvegltransform ! nveglglessink -e
