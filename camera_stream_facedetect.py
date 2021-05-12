import cv2
from datetime import datetime
cam = cv2.VideoCapture(0)
#cam.set(cv2.CAP_PROP_FRAME_WIDTH,1280)
#cam.set(cv2.CAP_PROP_FRAME_HEIGHT,720)

cv2.namedWindow("OV5647")
#cv2.setWindowProperty("OV5647",cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
frame_count = 0
face_cascade = cv2.CascadeClassifier("/usr/local/share/opencv4/haarcascades/haarcascade_frontalface_default.xml")
while True:
    start = datetime.now()
    ret, frame = cam.read()
    end = datetime.now()
    fps = 1/((end-start).total_seconds())
    print("fps for cam stream = %.2f"%fps)

    if not ret:
        print("failed to grab frame")
        break
    #cv2.imshow("OV5647",frame)
   
    start = datetime.now()
    gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray_image, 1.1, 4)
    end = datetime.now()
    fps = 1/((end-start).total_seconds())
    print("fps for face detect = %.2f"%fps)
    print(faces)

    #if not len(faces):
    #    print("No faces detected in image")
   # else:
    for (x,y,w,h) in faces:
        cv2.rectangle(frame,(x,y), (x+w,y+h), (255,255,0),2)

    cv2.imshow("OV5647",frame)
            
    k = cv2.waitKey(1)

    if k%256 == 27:
        #ESC pressed
        print("Escape hit, closing camera")
        break
    
cam.release()

cv2.destroyAllWindows()
