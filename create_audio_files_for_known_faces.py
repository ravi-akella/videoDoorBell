import gtts
import os
import glob

os.chdir("/home/pi/videoDoorBell/refImages")
names = []
#identify list of known names of faces
for file in glob.glob("*.jpg"):
	name = file.split(".")[0]
	names.append(name)

#create audio files for each namee
for name in names:
	text = "Recognised " + name + " in image."
	tts = gtts.gTTS(text)
	file_name = name + ".mp3"
	tts.save(file_name)



