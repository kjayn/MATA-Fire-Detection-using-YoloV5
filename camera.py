import cv2
import torch
import numpy as np


model = torch.hub.load('ultralytics/yolov5', 'custom', path=r"C:\Users\Bob\Downloads\yolov5\content\yolov5\runs\train\results_1\weights\best.pt", force_reload=True, autoshape=True)


class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture('fire.mp4')
        
    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, image = self.video.read()
        fps = int(self.video.get(cv2.CAP_PROP_FPS))
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = model(image)
        if len(results.xyxy[0]):
            labels = results.pandas().xyxy[0]['name']
            if 'Fire' in labels.values:
                print('Fire detected!')
                results.crop()
                # add your code here to take action when fire is detected
        else:
            print('no fire detected')

        a = np.squeeze(results.render())
        cv2.waitKey(fps)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()


