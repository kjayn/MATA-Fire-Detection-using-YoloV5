import cv2
import torch
import numpy as np
from playsound import playsound
import os
import datetime
import time
import pygame

model = torch.hub.load(r"C:\Users\Bob\Downloads\yolov5\content\yolov5", 
                       'custom', path=r"C:\Users\Bob\Downloads\yolov5\content\yolov5\runs\train\results_3\weights\best.pt", 
                       source='local')

fire_frames_path = 'fire_frames/'

if not os.path.exists(fire_frames_path):
    os.makedirs(fire_frames_path)

class VideoCamera(object): 
    def __init__(self):
        self.frame_counter = 0
        self.last_save_time = 0  # Track the last time a frame was saved
        self.video = cv2.VideoCapture(0)
        self.play_sound = False
        pygame.mixer.init()
        self.sound = pygame.mixer.Sound('alarm.mp3')

    def play_sound_async(self):
        self.sound.play() 

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
                current_time = time.time()
                if current_time - self.last_save_time > 1:  # Check if 1 second has passed since the last save
                    self.last_save_time = current_time
                    # Replace the line results.save() with the following code:
                    a = cv2.cvtColor(a, cv2.COLOR_BGR2RGB)
                    self.frame_counter += 1
                    timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
                    frame_filename = os.path.join(fire_frames_path, f'fire_frame_{timestamp}.jpg')
                    cv2.imencode('.jpg', a)[1].tofile(frame_filename)

                    if not self.play_sound:
                        self.play_sound = True
                        self.play_sound_async()
            
                
        else:
            if self.play_sound:
                self.sound.stop() 
                self.play_sound = False
            print('No fire detected')
            
        cv2.waitKey(fps)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        ret, jpeg = cv2.imencode('.jpg', image)
        
        return jpeg.tobytes()

class VideoCamera2(object):
    def __init__(self):
        self.video = cv2.VideoCapture('fire.mp4')
        self.play_sound = False
        pygame.mixer.init() # initialize pygame.mixer
        self.sound = pygame.mixer.Sound('alarm.mp3') # load the sound file

    def play_sound_async(self):
        self.sound.play() # play the sound

    def get_frame(self):
        success, image = self.video.read()
        fps = int(self.video.get(cv2.CAP_PROP_FPS))
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = cv2.resize(image, (640,480))
        #results = model(image, size = 240)
            
        cv2.waitKey(fps)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        ret, jpeg = cv2.imencode('.jpg', image)
        
        return jpeg.tobytes()
