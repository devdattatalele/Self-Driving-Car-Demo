print("Stop Sign module imported")
import cv2
import numpy as np
from tensorflow.keras.models import load_model
import sys
import blynklib
import time
import subprocess
from time import sleep

def run_again(cmd):
    subprocess.call(["bash", "-c", "source ~/.profile; " + cmd])
BLYNK_AUTH = '1feaa62e2a13485683b3974a215f521a'
blynk = blynklib.Blynk(BLYNK_AUTH)

detector = cv2.CascadeClassifier('stop_sign.xml')

steeringSen = 0.70  # Steering Sensitivity
maxThrottle = 0.22  # Forward Speed %
#motor = mM.Motor(2, 3, 4, 17, 22, 27) # Pin Numbers
model = load_model('model.h5')
cap = cv2.VideoCapture(1)
print("started")
steerinangle3 = 0
steerinangle2 = 0
steerinangle1 = 0

def getImg(display= False,size=[480,240]):
    _, img = cap.read()
    img = cv2.resize(img,(size[0],size[1]))
    if display:
        cv2.imshow('IMG',img)
    return img

def preProcess(img):
    img = img[54:120, :, :]
    img = cv2.cvtColor(img, cv2.COLOR_RGB2YUV)
    img = cv2.GaussianBlur(img, (3, 3), 0)
    img = cv2.resize(img, (200, 66))
    img = img / 255
    return img
def stopsign():
    #print("doo")
        ret, img = cap.read()
        stop=False
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = detector.detectMultiScale(gray, 1.3, 5)


        if cv2.waitKey(1) == ord('q'):
            sys.exit()


while True:

    img = getImg(True, size=[240, 120])
    img = np.asarray(img)
    img = preProcess(img)
    img = np.array([img])
    steering = float(model.predict(img))
    steerinangle=steering*steeringSen*100
    if(steerinangle<-3):
        steerinangle1=1
    elif (steerinangle>3):
        steerinangle2=1
    elif (steerinangle==-3<0>3):
            steerinangle3= 1
    #print("steering collected")
    #motor.move(maxThrottle,-steering*steeringSen)
    #print(steering*steeringSen*100)

    #print(steerinangle)
    cv2.waitKey(1)
    #stop1 = stopsign()
    ret, img = cap.read()
    stop = False
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = detector.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
        stop=False
        cv2.putText(img,str("stop"), (x,y+h),cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA,)
        print("stop")
        print("stop signal detected")
        # motor.stop(10)
        stop == True
    cv2.imshow('frame', img)
    blynk.run()
    blynk.virtual_write(1, steerinangle1)
    blynk.virtual_write(2, steerinangle2)
    blynk.virtual_write(3, steerinangle3)
    print(steerinangle1, steerinangle2, steerinangle3)

    sleep(1)
    blynk.virtual_write(1, 0)
    blynk.virtual_write(2, 0)
    blynk.virtual_write(3, 0)


    #if (stop1 == True):
    #    print("stop signal detected")
        #motor.stop(10)
    #if (stop1 == False):
    #    exit