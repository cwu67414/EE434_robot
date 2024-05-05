import cv2
import subprocess
import math
import signal

arm_length = 17

def convert_to_angles(a, b, c):
    angle1 = math.atan2(a, b) * (180 / math.pi)
    angle2 = math.atan2(c, b) + math.acos(math.sqrt(b**2 + c**2) / (2 * arm_length))
    angle3 = 2 * angle2 - 180
    
    return angle1, angle2, angle3

# Run GStreamer command to capture video
cmd0 = "gst-launch-1.0 nvarguscamerasrc sensor_id=0 ! 'video/x-raw(memory:NVMM),width=1920, height=1080, framerate=30/1' ! nvvidconv flip-method=0 ! 'video/x-raw,width=960, height=540' ! nvvidconv ! nvegltransform ! nveglglessink -e"
cmd1 = "gst-launch-1.0 nvarguscamerasrc sensor_id=1 ! 'video/x-raw(memory:NVMM),width=1920, height=1080, framerate=30/1' ! nvvidconv flip-method=0 ! 'video/x-raw,width=960, height=540' ! nvvidconv ! nvegltransform ! nveglglessink -e"

# Open subprocesses to run the commands
proc0 = subprocess.Popen(cmd0, shell=True)
proc1 = subprocess.Popen(cmd1, shell=True)

try:
    while True:
        # Read frames from the OpenCV capture objects
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

finally:
    # Terminate the subprocesses
    proc0.terminate()
    proc1.terminate()

    # Close OpenCV windows
    cv2.destroyAllWindows()