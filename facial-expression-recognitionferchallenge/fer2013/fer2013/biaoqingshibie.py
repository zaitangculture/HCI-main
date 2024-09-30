import cv2
import numpy as np
from ultralytics import YOLO
from keras.models import load_model
from keras.preprocessing.image import img_to_array

# 加载 YOLOv8 模型
model = YOLO('yolov8n.pt')

# 加载表情识别模型
emotion_model = load_model('path_to_your_emotion_model.h5')
emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']

# 打开摄像头
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # 对帧进行面部检测
    results = model(frame)

    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            face = frame[y1:y2, x1:x2]
            
            if face.size != 0:
                face_gray = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
                face_resized = cv2.resize(face_gray, (48, 48))
                face_array = img_to_array(face_resized)
                face_array = np.expand_dims(face_array, axis=0) / 255.0

                # 表情识别
                emotion_prediction = emotion_model.predict(face_array)
                max_index = np.argmax(emotion_prediction[0])
                emotion_label = emotion_labels[max_index]

                # 绘制边界框和标签
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, emotion_label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    # 显示结果
    cv2.imshow('Emotion Recognition', frame)

    if cv2.waitKey(1) == 27:  # 按 ESC 退出
        break

cap.release()
cv2.destroyAllWindows()
