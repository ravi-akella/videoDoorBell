import cv2
import face_recognition
import pickle
import numpy as np
from datetime import datetime
import threading
from threading import Thread
import queue as Queue
import copy

BUF_SIZE = 5
q = Queue.Queue(BUF_SIZE)
new_q = Queue.Queue(BUF_SIZE)

class FPS:
    def __init__(self):
        self._start = None
        self._end = None
        self._numFrames = 0
        
    def start(self):
        self._start = datetime.now()
        
    def stop(self):
        self._end = datetime.now()
        
    def update(self):
        self._numFrames+=1
        
    def elapsed(self):
        return (self._end - self._start).total_seconds()
    
    def fps(self):
        return self._numFrames/self.elapsed()
    
    
class CamVideoStream:
    def __init__(self,index = 0):
        self.stream = cv2.VideoCapture(index)
        (self.grabbed, self.frame) = self.stream.read()
        #initialize the variable used to indicate if the thread should be stopped
        self.stopped = False
        self.camData = CamData()
        self.face_cascade = cv2.CascadeClassifier("/usr/local/share/opencv4/haarcascades/haarcascade_frontalface_default.xml")
        self.face_roi = None
    def start(self):
        Thread(target=self.update, args=()).start()
        return self
    
    def update(self):
        while True:
            if self.stopped:
                return
            start = datetime.now()
            (self.grabbed, self.frame) = self.stream.read()
            if not self.grabbed:
                print("Failed to grab frame")
            else:
                if not q.full():
                    #self.camData.img = copy.deepcopy(self.frame)
                    gray_image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
                    self.camData.rgb = cv2.cvtColor(self.frame,cv2.COLOR_BGR2RGB)
                    self.face_roi = self.face_cascade.detectMultiScale(gray_image, 1.3, 4)
                    self.camData.faces_rect = copy.deepcopy(self.face_roi)
                    
                    #print("(Producer):sent frame")
                    q.put(self.camData)
                else:
                    print("Camera queue (q) full")
            end = datetime.now()
            fps = 1/((end-start).total_seconds())
            print("fps cam stream = %.2f"%fps)
            
    def read(self):
        return (self.grabbed, self.frame)
    
    def stop(self):
        self.stopped = True
        self.stream.release()
        
class FaceData:
    def __init__(self):
        self.img = None
        self.names = []
        self.counts = {}
        self.boxes = []
        
class CamData:
    def __init__(self):
        self.img = None
        self.rgb = None
        self.faces_rect = []
        
class FaceRecognition:
    def __init__(self):
        self.data = None
        self.rgb = None
        self.boxes = None
        self.unknown_encodings = []
        self.names = []
        self.counts = {}
        self.data = self.get_known_encodings()
        self.face_cascade = cv2.CascadeClassifier("/usr/local/share/opencv4/haarcascades/haarcascade_frontalface_default.xml")
        self.face_data = FaceData()
        self.faces_rect = []
        self.stopped = False
        
    def start(self):
        Thread(target=self.update, args=()).start()
        return self
    
    def update(self):
        while True:
            if self.stopped:
                return
            start = datetime.now()
            
            if q.empty():
                pass
                # print("No frames to run face recognition")
            else:
                
                camData = q.get()
                
                #print("(Consumer): received frame")
                #gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                #self.faces_rect = self.face_cascade.detectMultiScale(gray_image, 1.1, 4)
                self.faces_rect = camData.faces_rect
                #print("No of faces detected = %s"%len(self.faces_rect))
                #run face_recognition steps only if face detected
                if len(self.faces_rect):
                    #rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                    #update self.boxes
                    self.get_face_roi_in_boxes()
                    self.compute_unknown_face_encodings(camData.rgb,self.boxes)
                    self.analyze_unknown_face()

                    if not new_q.full():
                        #self.face_data.img = img
                        self.face_data.boxes = self.boxes
                        self.face_data.names = self.names
                        self.face_data.counts = self.counts
                        new_q.put(self.face_data)
                        end = datetime.now()
                        fps = 1/((end-start).total_seconds())
                        #print("face recognition fps = %.2f"%fps)
                else:
                    #self.face_data.img = img
                    self.face_data.boxes = []
                    self.face_data.names = []
                    self.face_data.counts = {}
                    new_q.put(self.face_data)
#             end = datetime.now()
#             fps = 1/((end-start).total_seconds())
#             print("face recognition fps = %.2f"%fps)
                    
    def stop(self):
        self.stopped = True
                    
                    
    def compute_unknown_face_encodings(self,rgb, boxes):
        self.unknown_encodings = face_recognition.face_encodings(rgb,boxes)
        return self.unknown_encodings
    
    def get_known_encodings(self):
        self.data = pickle.loads(open('./refImages/encodings.pickle',"rb").read())
        return self.data
    
    def get_face_roi_in_boxes(self):
        self.boxes = [(y,x+w,y+h,x) for (x,y,w,h) in self.faces_rect]
    
    def analyze_unknown_face(self):
        self.names = []
        #returns the names of faces recognised in the image stream
        for encoding in self.unknown_encodings:
            matches = face_recognition.compare_faces(self.data['encodings'],encoding,tolerance = 0.06)
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
                for (index,known_name) in enumerate(self.data['names']):
                    counts[known_name] = np.count_nonzero(matches[index])
                    
                print(counts)
                #get max of counts, find index of max count, find key of that index to get name of person with max match
                counts_values = list(counts.values())
                counts_keys = list(counts.keys())
                #we found a good match
                if max(counts_values)>100:
                    
                    name = counts_keys[counts_values.index(max(counts_values))]
            self.names.append(name)
            
        return self.names
                
#knownEncodings = {}
#knownNames = []
#Get known face encodings from pickle dump
#data = pickle.loads(open('./refImages/encodings.pickle',"rb").read())
face_recog = FaceRecognition()
#start face recognition thread
face_recog.start()
cam = CamVideoStream(index = 0)
cam.start()
# fps = FPS()
# fps.start()
cv2.namedWindow("OV5647")
   
#cv2.setWindowProperty("OV5647",cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
#face_cascade = cv2.CascadeClassifier("/usr/local/share/opencv4/haarcascades/haarcascade_frontalface_default.xml")

face_data = None
names_to_display = None
non_analyzed_frames = 0
while True:
    start = datetime.now()
    if not new_q.empty():
        face_data = new_q.get()
        names_to_display = face_data.names
        print("non analyzed frames = %s"%non_analyzed_frames)
        non_analyzed_frames = 0
        
    else:
        #print("No face_recognition frames to display recognised faces")
        non_analyzed_frames+=1

    # we will use the names of previous face_data,
    #but run the face detection again to identify roi of faces
    #this hopefully will reduce latency when No frames are available from face_recognition queue (new_q)
    _,img_to_display = cam.read()
    #add roi, names if data available
    if face_data is not None:
        
        faces_roi = cam.camData.faces_rect
        #gray = cv2.cvtColor(img_to_display, cv2.COLOR_BGR2GRAY)
        #faces_roi = face_recog.face_cascade.detectMultiScale(gray, 1.1, 4)
        print("No of faces detected = %s"%len(faces_roi))
        for ((x,y,w,h),name) in zip(faces_roi,names_to_display):
            cv2.rectangle(img_to_display,(x,y), (x+w,y+h), (255,255,0),2)
            ynew=y-15 if y-15>15 else y+15
            if not name == "Unknown":
                cv2.putText(img_to_display,name,(x,ynew),cv2.FONT_HERSHEY_SIMPLEX,0.75,(0,255,0),2)
        
        cv2.imshow("OV5647",img_to_display) 
        k = cv2.waitKey(1)
        
        if k%256 == 27:
            #ESC pressed
            print("Escape hit, closing camera")
            break
        end = datetime.now()
        fps = 1/((end-start).total_seconds())
        print("display fps = %.2f"%fps)

cam.stop()
face_recog.stop()
cv2.destroyAllWindows()

        
        
