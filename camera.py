import cv2
import torch
import numpy as np
from playsound import playsound
import pygame

#if you dont have a yolov5 folder use this line (need internet to use this):
#model = torch.hub.load('ultralytics/yolov5', 'custom','best.pt', force_reload=True)

model = torch.hub.load(r"C:\Users\Bob\Downloads\yolov5\content\yolov5", 'custom', path="best.pt", source='local') #paste the folder of yolov5 in the first double qoutation
model.conf = 0.6
model.classes = 0

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        self.play_sound = False
        pygame.mixer.init() # initialize pygame.mixer
        self.sound = pygame.mixer.Sound('alarm.mp3') # load the sound file

    def play_sound_async(self):
        self.sound.play() # play the sound

    def get_frame(self):
        success, image = self.video.read()
        fps = int(self.video.get(cv2.CAP_PROP_FPS))
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = model(image, size = 240)
        
        a = np.squeeze(results.render())
        if len(results.xyxy[0]):
            labels = results.pandas().xyxy[0]['name']
            if 'fire' in labels.values:
                print('Fire detected!')

                if not self.play_sound:
                    # Play the sound asynchronously
                    self.play_sound = True
                    self.play_sound_async()
            
                
        else:
            if self.play_sound:
                # Stop the sound if it's playing
                self.sound.stop()
                self.play_sound = False
            print('no fire detected')
            
        cv2.waitKey(fps)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        ret, jpeg = cv2.imencode('.jpg', image)
        
        return jpeg.tobytes()
