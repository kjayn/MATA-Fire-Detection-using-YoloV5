# MATA-Fire-Detection-using-YoloV5

This project implements a real-time fire detection system using the YOLOv5 object detection algorithm and Flask web framework. The system is capable of detecting fires in images and videos in real-time, providing a visual interface for monitoring and alerting.

### Features 
* Real-time fire detection using YOLOv5
* Integration with Flask web framework for a user-friendly interface
* Alarm when there is fire detected
* Supports regular camera input for fire detection
* Displays bounding boxes around detected fire instances
* Can be deployed on local systems or servers

### Prerequisites
* Python 3.6 or above
* GPU (recommended for faster detection)
* CUDA toolkit (for GPU acceleration)

### Usage
1. Start the flask application
and run [python main.py](main.py)

2. Open your web browser and navigate to http://localhost:5000.
3. Upload an image or video file containing fire scenes.
4. The system will process the input in real-time, detecting fires and displaying bounding boxes around them.
5. You can monitor the detection results and take appropriate actions based on the detected fire instances.

### Customization
* Training your own YOLOv5 model: If you have a custom fire detection dataset, you can train your own YOLOv5 model by following the instructions provided in the official YOLOv5 repository and you also use roboflow to access millions of dataset.
* Modifying the Flask application: The Flask application can be customized to fit specific requirements. You can modify the HTML templates, CSS styles, or add additional functionality to enhance the user interface or integrate with other systems.

### Contributing
Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

### Acknowledgments
* YOLOv5: https://github.com/ultralytics/yolov5
* Roboflow: https://universe.roboflow.com/

### References
* YOLOv5 paper: https://arxiv.org/abs/1912.02899
* Flask documentation: https://flask.palletsprojects.com/
* YOLOv5 official repository: https://github.com/ultralytics/yolov5
