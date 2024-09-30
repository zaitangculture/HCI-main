import cv2
import mediapipe as mp

mp_objectron = mp.solutions.objectron
mp_drawing = mp.solutions.drawing_utils

# 初始化视频捕捉
cap = cv2.VideoCapture(0)

with mp_objectron.Objectron(static_image_mode=False, max_num_objects=5, min_detection_confidence=0.5, model_name='Shoe') as objectron:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # 将图像转换为RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False

        # 检测物体
        results = objectron.process(image)

        # 将图像转换回BGR
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # 绘制检测结果
        if results.detected_objects:
            for detected_object in results.detected_objects:
                mp_drawing.draw_landmarks(image, detected_object.landmarks_2d, mp_objectron.BOX_CONNECTIONS)
                mp_drawing.draw_axis(image, detected_object.rotation, detected_object.translation)

        # 显示图像
        cv2.imshow('MediaPipe Objectron', image)

        if cv2.waitKey(5) & 0xFF == 27:
            break

cap.release()
cv2.destroyAllWindows()
