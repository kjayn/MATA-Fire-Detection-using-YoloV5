import cv2
import torch
import numpy as np
import os
import datetime
import time
import sys
from PyQt5 import QtWidgets, QtGui, QtCore
import pygame

model = torch.hub.load(r"C:\Users\Bob\Downloads\yolov5\content\yolov5", 
                       'custom', path=r"C:\Users\Bob\Downloads\yolov5\content\yolov5\runs\train\results_3\weights\best.pt", 
                       source='local')

model.conf = 0.5
model.classes = 0

fire_frames_path = 'fire_frames/'

if not os.path.exists(fire_frames_path):
    os.makedirs(fire_frames_path)

class VideoCamera(object):
    def __init__(self, video_source):
        self.frame_counter = 0
        self.last_save_time = 0
        self.video = cv2.VideoCapture(video_source)
        self.play_sound = False

    def detect_fire(self, image):
        results = model(image, size=240)
        a = np.squeeze(results.render())
        if len(results.xyxy[0]):
            labels = results.pandas().xyxy[0]['name']
            if 'fire' in labels.values:
                print('Fire detected!')
                current_time = time.time()
                if current_time - self.last_save_time > 1:
                    self.last_save_time = current_time
                    a = cv2.cvtColor(a, cv2.COLOR_BGR2RGB)
                    self.frame_counter += 1
                    timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
                    date_folder = datetime.datetime.now().strftime('%Y_%m_%d')
                    date_folder_path = os.path.join(fire_frames_path, date_folder)
                    if not os.path.exists(date_folder_path):
                        os.makedirs(date_folder_path)
                    frame_filename = os.path.join(date_folder_path, f'fire_frame_{timestamp}.jpg')
                    cv2.imencode('.jpg', a)[1].tofile(frame_filename)

                    if not self.play_sound:
                        self.play_sound = True
                        pygame.mixer.init()
                        pygame.mixer.music.load('alarm.mp3')
                        pygame.mixer.music.play()
            
        else:
            if self.play_sound:
                pygame.mixer.music.stop() 
                self.play_sound = False
            print('No fire detected')

    def get_frame(self):
        success, image = self.video.read()
        if not success:
            return None
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        self.detect_fire(image)
        return image

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, video_source):
        super(MainWindow, self).__init__()
        self.video_camera = VideoCamera(video_source)
        self.central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.video_label = QtWidgets.QLabel(self.central_widget)
        self.layout = QtWidgets.QVBoxLayout(self.central_widget)
        self.layout.addWidget(self.video_label)
        self.update_video()
        self.resize(800,800)

    def update_video(self):
        frame = self.video_camera.get_frame()
        if frame is not None:
            frame = QtGui.QImage(frame, frame.shape[1], frame.shape[0], QtGui.QImage.Format_RGB888)
            frame = QtGui.QPixmap.fromImage(frame)
            self.video_label.setPixmap(frame.scaled(self.video_label.size(), QtCore.Qt.KeepAspectRatio))
        QtCore.QTimer.singleShot(1, self.update_video)

if __name__ == '__main__':
    video_source = 'fire.mp4'
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow(video_source)
    main_window.show()
    sys.exit(app.exec_())
