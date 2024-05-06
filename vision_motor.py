import subprocess
import math
import cv2
import numpy as np

arm_length = 17

def convert_to_angles(a, b, c):
    if math.sqrt(b**2 + a**2) > 2 * arm_length or math.sqrt(a**2 + c**2) > 2 * arm_length:
        print("Object is too far away from the arm.")
        return None
    angle1 = math.atan2(a, b) * (180 / math.pi)
    angle2 = math.atan2(c, b) + math.acos(math.sqrt(b**2 + c**2) / (2 * arm_length))
    angle3 = - 2 * angle2
    
    return angle1, angle2, angle3

# Run GStreamer command to capture video
cmd0 = "gst-launch-1.0 nvarguscamerasrc sensor_id=0 ! 'video/x-raw(memory:NVMM),width=1920, height=1080, framerate=30/1' ! nvvidconv flip-method=0 ! 'video/x-raw,width=960, height=540' ! nvvidconv ! nvegltransform ! nveglglessink -e"
cmd1 = "gst-launch-1.0 nvarguscamerasrc sensor_id=1 ! 'video/x-raw(memory:NVMM),width=1920, height=1080, framerate=30/1' ! nvvidconv flip-method=0 ! 'video/x-raw,width=960, height=540' ! nvvidconv ! nvegltransform ! nveglglessink -e"

# Open subprocesses to run the commands
proc0 = subprocess.Popen(cmd0, shell=True)
proc1 = subprocess.Popen(cmd1, shell=True)

def detect_object(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, thresholded = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        M = cv2.moments(largest_contour)
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])
        return cx, cy
    else:
        print("Didn't detect the object.")
        return None
    
try:
    while True:
        print("Enter the loop.")
        ret0, frame0 = proc0.stderr.read(), proc0.stderr.read()
        ret1, frame1 = proc1.stderr.read(), proc1.stderr.read()

        if ret0 and ret1:
            print("Have the videos.")
            # Convert the byte data to numpy array
            frame0 = cv2.imdecode(np.frombuffer(frame0, np.uint8), -1)
            frame1 = cv2.imdecode(np.frombuffer(frame1, np.uint8), -1)
            
            # Detect object coordinates in each frame
            object_coords0 = detect_object(frame0)
            object_coords1 = detect_object(frame1)
            
            if object_coords0 and object_coords1:
                # Calculate the average coordinates from both sensors
                avg_coords = ((object_coords0[0] + object_coords1[0]) / 2, 
                              (object_coords0[1] + object_coords1[1]) / 2, 
                              0)
                
                # Convert object coordinates to angles
                angles = convert_to_angles(avg_coords[0], avg_coords[1], avg_coords[2])
                if angles is not None:
                    print("Angle 1:", angles[0])
                    print("Angle 2:", angles[1])
                    print("Angle 3:", angles[2])

finally:
    # Wait for the subprocesses to terminate
    proc0.wait()
    proc1.wait()