import pickle
import os
import cv2
import glob
import face_recognition
os.chdir("/home/pi/videoDoorBell/refImages")

knownEncodings = []
knownNames = []

for file in glob.glob("*.jpg"):
    name = file.split(".")[0]
    image = cv2.imread(file)
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    boxes = face_recognition.face_locations(rgb,model='hog')
    encoding = face_recognition.face_encodings(rgb,boxes)
    knownNames.append(name)
    knownEncodings.append(encoding)

data = {"encodings":knownEncodings,"names":knownNames}
f = open("encodings.pickle","wb")
f.write(pickle.dumps(data))
f.close()
