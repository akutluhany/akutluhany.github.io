import bluetooth 
from imutils.video import VideoStream
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

# Bluetooth Connection Setup
serverMAC = 'DC:A6:32:0A:1F:58'
port = 3
size = 1024
s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
s.connect((serverMAC, port))

# QR recognition function
def qr_rec():  
    # Return value
    ret = 0

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

        # 1) quit message detected
        if (text == 'quit'):
            ret = -2
            return ret

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
                firebase.put('/Locker/' + str(locker) +'/lockStatus', 1)
                GPIO.cleanup()
                return ret                
            else:
                print("checking next qr code")
                            
    ret = -1
    return ret
    
# Receiving message from the host
def get_msg():
        #try:
        d = s.recv(size)
        return d.decode()

p = True
q = True

# Bluetooth Connection Loop
while q:
    # QR Code Scanning Loop
    while p:
        # Start Video Stream
        print("Starting Video Stream ...")
        vs = VideoStream(usePicamera=True).start()
        time.sleep(2.0)
        status = qr_rec()
        # 1) if QR recognition is successful
        if (status == 0):            
            # send a signal to the object recognition Pi
            s.send('scan')
            # get a message back 
            d = get_msg()
            # if the message is 0, lock again & update the lock status
            if (str(d) == 0):                 
                GPIO.output(14, GPIO.LOW)       
                firebase.post('/Locker/' + str(locker) + '/lockStatus', 0)
        # 2) if QR recognition fails,
        elif (status == -1):
            print("QR recognition failed")
        # 3) if quit message is detected, breaks the connection
        elif (status == -2):
            s.send('quit') 
            q = False            
        vs.stop()
        cv2.destroyAllWindows()
        time.sleep(2.0)    

s.close()

