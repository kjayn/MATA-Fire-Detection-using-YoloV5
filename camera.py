import cv2
import torch
import numpy as np
import telebot
import datetime
import threading
from playsound import playsound


model = torch.hub.load(r"C:\Users\Bob\Downloads\yolov5\content\yolov5", 'custom', path=r"C:\Users\Bob\Downloads\yolov5\content\yolov5\runs\train\results_3\weights\best.pt", source='local')
model.conf = 0.6
model.classes = 0

# Create a Telegram bot instance with the API token
bot = telebot.TeleBot('5935952245:AAHAaJ1ri9N5BJsq8nE7Pbw-TTYchiVieWA')

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture('fire2.mp4')
        self.play_sound = False
        
    def play_sound_async(self):
        playsound('alarm.mp3')

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
                
                labels, cord_thres = results.xyxyn[0][:, -1].numpy(), results.xyxyn[0][:, :-1].numpy()
                x = cord_thres[:, 0]
                y = cord_thres[:, 1]
                w = cord_thres[:, 2]
                h = cord_thres[:, 3]
                print(x,y,w,h)
                
                if not self.play_sound:
                    # Play the sound asynchronously
                    self.play_sound = True
                    threading.Thread(target=self.play_sound_async).start()
                
                # Save the image
                cv2.imwrite('fire_detected.jpg', cv2.cvtColor(a, cv2.COLOR_RGB2BGR))
                now = datetime.datetime.now()
                message = f'Fire detected at {now.strftime("%Y-%m-%d %H:%M:%S")}'
                # Send the image via Telegram
                #with open('fire_detected.jpg', 'rb') as f:
                    #bot.send_photo(chat_id='1937435385', photo=f, caption=message)
                
        else:
            self.play_sound = False
            print('no fire detected')
            
        cv2.waitKey(fps)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        ret, jpeg = cv2.imencode('.jpg', image)
        
        return jpeg.tobytes()
