import cv2
import face_recognition

cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FRAME_WIDTH,1280)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT,720)

cv2.namedWindow("OV5647")
#cv2.setWindowProperty("OV5647",cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
frame_count = 0
face_cascade = cv2.CascadeClassifier("/usr/local/share/opencv4/haarcascades/haarcascade_frontalface_default.xml")
while True:
    ret, frame = cam.read()

    if not ret:
        print("failed to grab frame")
        break
    #cv2.imshow("OV5647",frame)
   

    gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray_image, 1.1, 4)
    print(faces)

    if not len(faces):
        print("No faces detected in image")
        print("Trying again")
        continue

    if len(faces)>1:
        
        for (x,y,w,h) in faces:
            cv2.rectangle(frame,(x,y), (x+w,y+h), (255,255,0),2) 

        cv2.imshow("OV5647",frame)
        text = input("More than 1 face in image, please have only 1 person in front of camera and press enter")
        continue
    
    if len(faces)==1:
        print("Detected person by opencv, now checking using face_recognition for detected face")
        boxes = face_recognition.face_locations(frame,model = 'hog')
        if len(boxes)==1:
            
        #for (x,y,w,h) in faces:
         #   cv2.rectangle(frame,(x,y), (x+w,y+h), (255,255,0),2)
            text = input("Detected person in image using opencv & also face_recognition, to save image enter name of person")
            if text=="n":
                print("Not saving image")
                continue
            else:
                file = "/home/pi/videoDoorBell/refImages/"+text+".jpg"
                cv2.imwrite(file,frame)
                print("File saved to location %s"%file)
                print("Exiting program")
                cam.release()
                exit()

        

    cv2.imshow("OV5647",frame)
            
    k = cv2.waitKey(1)
    
    if k%256 == 27:
        #ESC pressed
        print("Escape hit, closing camera")
        break
    
cam.release()

cv2.destroyAllWindows()
