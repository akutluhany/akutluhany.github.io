
There are two versions of the final code: 1) code with Bluetooth connection (final-blue.py) and 2) without Bluetooth connection (final-noblue.py).

The first version requires Brian's code to be running simultaneously, which serves as a host side of the service. The code is nested inside a while-loop that looks for the connection with Brian's laptop, so the code will stuck in that loop if two devices are not operating at the same time.

The second version does not require the Bluetooth connection and therefore can be run individually. It will start the webcam and will look for any QR code. Once the QR code is evaluated correctly, it will print out 'unlocked successfully' on the console. In the real setting, it will actually unlock the solenoid. It should then update the lockStatus of the locker to be '1' on the Firebase database and will print out 'update successful'. Once updated, the console will print out 'locked successfully'. Again, the lock will be actually locked. The program ends when all the processes are complete.

All the required libraries:
    1. Firebase Realtime Database
    2. cv2 
    3. Raspberry Pi GPIO -> locking & unlocking solenoid 
    4. pyzbar (Python zbar library) -> barcode detecting
    5. imutils VideoStream
    6. Bluetooth 

To run the code, you need to create a virtual environment. Here are the command line arguments for creating a virtual environment: 

    mkvirtualenv your_environment_name -p python3
    workon your_environment_name
    
Next, you need to download all the neccessary libraries inside this virtual environment by typing in:

    pip install pyzbar
    pip install opencv-python
    pip install RPi.GPIO
    pip install PyBluez
    pip install imutils
    pip install python-firebase    

Once you download all the libraries and are inside the virtual environment, you can run the program by typing in 'python final-blue.py' or 'python final-noblue.py' 




