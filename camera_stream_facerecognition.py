import cv2
import face_recognition
import pickle
import numpy as np
from datetime import datetime
import threading

cam = cv2.VideoCapture(0)
#cam.set(cv2.CAP_PROP_FRAME_WIDTH,1280)
#cam.set(cv2.CAP_PROP_FRAME_HEIGHT,720)

#cv2.namedWindow("OV5647")
#cv2.setWindowProperty("OV5647",cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
frame_count = 0
face_cascade = cv2.CascadeClassifier("/usr/local/share/opencv4/haarcascades/haarcascade_frontalface_default.xml")
#Get known face encodings from pickle dump
knownEncodings = {}
knownNames = []
data = pickle.loads(open('./refImages/encodings.pickle',"rb").read())

#knownEncodings[data['names']] = data['encodings']


while True:
    start = datetime.now()
    ret, frame = cam.read()

    if not ret:
        print("failed to grab frame")
        break
    #cv2.imshow("OV5647",frame)
   

    gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces_rect = face_cascade.detectMultiScale(gray_image, 1.1, 4)
    print("No of faces detected = %s"%len(faces_rect))
   
    unknown_encodings = []
    names = []
    
    rgb = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    #boxes = face_recognition.face_locations(rgb,model='hog')
   
   #Opencv detectMultiscale returns bounding box coordinates in (x,y,w,h) order
   #but we need them in (top,right,bottom,left) order, so need to do reordering
    boxes = [(y,x+w,y+h,x) for (x,y,w,h) in faces_rect]

    unknown_encodings = face_recognition.face_encodings(rgb,boxes)
       
    #create a 2D list with no_of_rows = len(unknown_encodings) 
    #i.e. no of faces detected in image stream
    # no_of_cols = len(data['encodings'] i.e. no of known faces loaded from pickle dump
    # -1 in matches => search not done/match not found for person from image stream, value in matches[r][c] indicates index of person with whom match found from data['encodings'] 128-d vector. 
    #rows = len(unknown_encodings)
    #ols = len(data['encodings'])
    #matches = [[-1]*cols]*rows
    
    for encoding in unknown_encodings:
        matches = face_recognition.compare_faces(data['encodings'],encoding,tolerance = 0.1)
#         if True in matches:
#             names.append('ravi')
#         else:
#             names.append('Unknown')

        name = "Unknown"
        #check to see if we have found a match based on output of face_compare
        face_known = False
        for match in matches:
            if True in match:
                face_known = True
        #Identify which face is it based on output of face_compare 128d result
        if face_known:
            counts = {}
            for (index,known_name) in enumerate(data['names']):
                counts[known_name] = np.count_nonzero(matches[index])
                
            print(counts)
            name = max(counts, key = counts.get)
        names.append(name)
       
    for ((top,right,bottom,left),name) in zip(boxes,names):
        #draw face roi on image
        cv2.rectangle(frame,(left,top),(right,bottom),(0,255,0),2)
        y=top-15 if top-15>15 else top+15
        if not name == 'Unknown':
            cv2.putText(frame,name,(left,y),cv2.FONT_HERSHEY_SIMPLEX,0.75,(0,255,0),2)

    #cv2.imshow("OV5647",frame)
            
    k = cv2.waitKey(1)

    if k%256 == 27:
        #ESC pressed
        print("Escape hit, closing camera")
        break
    end = datetime.now()
    fps = 1/((end-start).total_seconds())
    print("fps = %.2f"%fps)
    
cam.release()

cv2.destroyAllWindows()
