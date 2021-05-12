import os
import pickle
import face_recognition
import cv2

img = cv2.imread("/home/pi/videoDoorBell/refImages/murty.jpg")
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
face_cascade = cv2.CascadeClassifier("/usr/local/share/opencv4/haarcascades/haarcascade_frontalface_default.xml")
faces = face_cascade.detectMultiScale(gray, 1.1, 4)
print("No of faces detected = %s"%len(faces))