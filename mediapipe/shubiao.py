import cv2
import mediapipe as mp
import pyautogui
import time

# 初始化 MediaPipe 手部追踪模块
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# 获取屏幕尺寸
screen_width, screen_height = pyautogui.size()

# 初始化视频捕捉
cap = cv2.VideoCapture(0)

# 控制鼠标的手部关键点索引
INDEX_FINGER_TIP = 8
THUMB_TIP = 4

# 用于防止重复点击的变量
click_counter = 0
click_delay = 10  # 设置点击延迟，单位为帧

try:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # 将图像转换为RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False

        # 检测手部
        results = hands.process(image)

        # 将图像转换回BGR
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # 获取图像尺寸
        image_height, image_width, _ = image.shape

        # 绘制手部关键点
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # 获取食指尖端的坐标
                x = int(hand_landmarks.landmark[INDEX_FINGER_TIP].x * image_width)
                y = int(hand_landmarks.landmark[INDEX_FINGER_TIP].y * image_height)

                # 将图像坐标转换为屏幕坐标
                screen_x = screen_width - int((x / image_width) * screen_width)
                screen_y = int((y / image_height) * screen_height)

                # 移动鼠标到屏幕坐标
                pyautogui.moveTo(screen_x, screen_y)

                # 检测食指和拇指是否接触（模拟点击）
                thumb_tip = hand_landmarks.landmark[THUMB_TIP]
                index_finger_tip = hand_landmarks.landmark[INDEX_FINGER_TIP]
                
                distance = ((thumb_tip.x - index_finger_tip.x) ** 2 + (thumb_tip.y - index_finger_tip.y) ** 2) ** 0.5
                if distance < 0.05:
                    if click_counter == 0:
                        pyautogui.click()
                        click_counter = click_delay
                else:
                    click_counter = max(0, click_counter - 1)

        # 显示图像
        cv2.imshow('Hand Tracking', image)

        if cv2.waitKey(5) & 0xFF == 27:
            break
finally:
    cap.release()
    cv2.destroyAllWindows()
    hands.close()
