from imutils.video 
import VideoStream
from pyzbar import pyzbar
from firebase import firebase
import datetime
import imutils
import cv2
import RPi.GPIO as GPIO
import time

# GPIO Setup
GPIO.setmode(GPIO.BCM)

# Firebase Setup
firebase = firebase.FirebaseApplication('https://scenic-doodad-255320.firebaseio.com')
lockers = firebase.get('/Locker', None)

# Video Stream Setup
print ("Webcam Turning On")
vs = VideoStream(usePicamera=True).start()
time.sleep(2.0)

p = True

# QR Code Scanning Loop
while p:
    # Grabbing the fram from the Video Stream
    frame = vs.read()
    frame = imutils.resize(frame, width=400)

    # Detecting the QR codes in the frame and decode each of them
    barcodes = pyzbar.decode(frame)

    # Iterating through the detected QR codes
    for barcode in barcodes:
        (x, y, w, h) = barcode.rect
        cv2.rectangle(frame, (x,y,), (x+w, y+h), (0, 0, 255), 2)

        barcodeData = barcode.data.decode("utf-8")
        barcodeType = barcode.type

        # change the QR code to be in a string format
        text = "{}".format(barcodeData)
        cv2.putText(frame, text, (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        # Iterating through all the lockers from the Firebase
        for locker in lockers:
            # Get QR string value of the locker
            qr_string = '/Locker/' + str(locker) + '/qr'
            qr = firebase.get(qr_string, None)
            # compare with the detected QR code
            if (text == qr):
                # unlock the lock
                GPIO.setup(14, GPIO.OUT)
                GPIO.output(14, GPIO.HIGH)
                print("unlocked successfully")
                # update the lock status to be '1'
                firebase.post('/Locker/' + str(locker) + '/lockStatus', 1)
                time.sleep(5)
                # lock the lock again after 5 seconds
                GPIO.output(14, GPIO.LOW)
                print("locked successfully")
                GPIO.cleanup()           
                p = False
                break
            else:
                print("checking next qr code")

        print("No corresponding code found")
        p = False
        break
        
# Stop Video
print("Webcam turning off")
vs.stop()
cv2.destroyAllWindows()


