import cv2
import mediapipe as mp
import math
import numpy as np
import screen_brightness_control as sbc
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import serial
import time

class HandControl:
    def __init__(self):
        # 初始化 MediaPipe
        self.mphands = mp.solutions.hands
        self.hands = self.mphands.Hands()
        self.mpDraw = mp.solutions.drawing_utils
        self.pointStyle = self.mpDraw.DrawingSpec(color=(0, 0, 255), thickness=3)
        self.lineStyle = self.mpDraw.DrawingSpec(color=(0, 255, 0), thickness=4)

        # 初始化音量控制
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self.volume = cast(interface, POINTER(IAudioEndpointVolume))
        self.volume.SetMute(0, None)
        self.volRange = self.volume.GetVolumeRange()

        # 初始化串口
        self.ser = serial.Serial('COM6', 9600, timeout=1)  # 确保将 'COM3' 替换为你的串口端口
        time.sleep(2)  # 等待串口稳定

    def gesture(self):
        cap = cv2.VideoCapture(0)
        resize_w = 640
        resize_h = 480

        while cap.isOpened():
            ret, img = cap.read()
            if ret:
                imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                result = self.hands.process(imgRGB)

                if result.multi_hand_landmarks:
                    for handLms in result.multi_hand_landmarks:
                        self.mpDraw.draw_landmarks(img, handLms, self.mphands.HAND_CONNECTIONS, self.pointStyle, self.lineStyle)
                        
                        # 获取手掌中心和拇指的坐标
                        palm_x = handLms.landmark[0].x * resize_w
                        thumb_x = handLms.landmark[4].x * resize_w

                        # 判断是左手还是右手
                        is_left_hand = thumb_x < palm_x

                        # 获取拇指和食指的坐标
                        p4_x = math.ceil(handLms.landmark[4].x * resize_w)
                        p4_y = math.ceil(handLms.landmark[4].y * resize_h)
                        landmarks_p4 = (p4_x, p4_y)

                        p8_x = math.ceil(handLms.landmark[8].x * resize_w)
                        p8_y = math.ceil(handLms.landmark[8].y * resize_h)
                        landmarks_p8 = (p8_x, p8_y)

                        # 中间点坐标
                        middle_point_x = (p4_x + p8_x) // 2
                        middle_point_y = (p4_y + p8_y) // 2
                        landmarks_middle = (middle_point_x, middle_point_y)

                        # 绘制拇指和食指以及它们之间的连线
                        img = cv2.circle(img, landmarks_p4, 10, (255, 0, 255), cv2.FILLED)
                        img = cv2.circle(img, landmarks_p8, 10, (255, 0, 255), cv2.FILLED)
                        img = cv2.circle(img, landmarks_middle, 10, (255, 0, 255), cv2.FILLED)
                        img = cv2.line(img, landmarks_p4, landmarks_p8, (255, 0, 255), 5)

                        # 计算拇指和食指之间的距离
                        line_len = math.hypot(p4_x - p8_x, p4_y - p8_y)
                        print(line_len)

                        # 通过串口发送距离
                        self.ser.write(f'{line_len}\n'.encode('ascii'))

                        if is_left_hand:
                            # 将距离映射到音量范围
                            min_volume = self.volRange[0]
                            max_volume = self.volRange[1]
                            vol = np.interp(line_len, [10, 200], [min_volume, max_volume])
                            
                            # 设置音量
                            self.volume.SetMasterVolumeLevel(vol, None)
                        else:
                            # 将距离映射到亮度范围
                            min_brightness = 0
                            max_brightness = 100
                            brightness = np.interp(line_len, [10, 200], [min_brightness, max_brightness])
                            
                            # 设置屏幕亮度
                            sbc.set_brightness(int(brightness))

                frame = cv2.flip(img, 1)
                cv2.imshow("video", frame)

            if cv2.waitKey(1) == 27:
                break

        cap.release()
        cv2.destroyAllWindows()
        self.ser.close()

if __name__ == "__main__":
    control = HandControl()
    control.gesture()
