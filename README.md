# videoDoorBell
List of files:

camera_stream_face_detect.py => Grabs images from camera and runs face detection, displays frames with face roi highlighted

camera_stream_face_recognition.py => Grabs images from camera and runs face recognition

camera_stream_face_recognition_threading.py => Grabs images from camera and runs face recognition in multithreading

check_no_of_faces.py => Quick program to check no of faces present in image

rpi_camera_surveillance_system.py => Web streaming of rpi - can be viewed from the same network rpi is connected to by opening the IP address of Pi in browser.

save_known_faces.py => Use to save known faces images to ./refImages folder so that face recognition program can compare camera stream images with known faces to recognise (name of file saved = name of person)

socketserver.py => Library used in rpi_camera_surveillance_system.py => had difficulty installing by pip so copied the file to import into program

write_face_encodings.py => opens Images present in ./refImages folder and computes the face encodings using face_recognition library, and saves the encodings to ./refImages/encodings.pickle, these encodings are loaded
by face_recognition demo & compared with camera stream to recognise faces.

How to run face recognition demo?
In order to run face recognition demo you can either use: 
  1) camera_stream_face_recognition.py (face_recognition running in a single thread)
  2) camera_stream_face_recognition_threading.py (face_recognition running in multiple threads)
  
To run either of the above 2 face recognition programs with threading or without threading you can follow the below sequence:
1) Create a directory refImages inside the root directory (used to store the face encodings and known faces images)
2) Run the script save_known_faces.py to save known people images. Run the script as many times as the no of persons to recognise to save each persons image as a seperate file
3) Run script write_face_encodings.py to save face encodings of all the images saved in ./refImages folder.
4) Run camera_stream_face_recognition.py or camera_stream_face_recognition_threading.py to run face recognition demo.
