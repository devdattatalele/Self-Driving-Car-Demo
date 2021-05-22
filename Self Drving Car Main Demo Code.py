import cv2
import numpy as np
from tensorflow.keras.models import load_model
import sys
import MotorModule as mM

######Stop sign recognition by Xml file-
detector = cv2.CascadeClassifier('stop_sign.xml')

# Steering Sensitivity-
steeringSen = 0.70
# Forward Speed %-
maxThrottle = 0.22
# Motor Pin To Raspberry pi GPIO-
motor = mM.Motor(2, 3, 4, 17, 22, 27)
# My Trained model-
model = load_model('model.h5')
# Camera input
##############################Change Value to "1" if you Are using Second camera
cap = cv2.VideoCapture(0)
print("Angle Prediction Started")
steeringangle3 = 0
steeringangle2 = 0
steeringangle1 = 0


def getImg(display=False, size=[480, 240]):
    _, img = cap.read()
    img = cv2.resize(img, (size[0], size[1]))
    if display:
        cv2.imshow('IMG', img)
    return img


def preProcess(img):
    img = img[54:120, :, :]
    img = cv2.cvtColor(img, cv2.COLOR_RGB2YUV)
    img = cv2.GaussianBlur(img, (3, 3), 0)
    img = cv2.resize(img, (200, 66))
    img = img / 255
    return img


def stopsign():
    # print("Stopsign model started")
    ret, img = cap.read()
    stop = False
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
    steeringangle = steering * steeringSen
    motor.move(maxThrottle, -steering * steeringSen)
    cv2.waitKey(1)
    ret, img = cap.read()
    stop = False
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = detector.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
        stop = False
        cv2.putText(img, str("stop"), (x, y + h), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA, )
        print("stop signal detected")
        motor.stop(10)
        stop == True
    cv2.imshow('frame', img)
