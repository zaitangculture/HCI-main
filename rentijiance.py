import cv2
import mediapipe as mp
import math
import numpy as np

class PoseControl:
    def __init__(self):
        # 初始化 MediaPipe Pose
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose()
        self.mpDraw = mp.solutions.drawing_utils
        self.pointStyle = self.mpDraw.DrawingSpec(color=(0, 0, 255), thickness=3)
        self.lineStyle = self.mpDraw.DrawingSpec(color=(0, 255, 0), thickness=4)

    def detect_pose(self):
        cap = cv2.VideoCapture(0)
        resize_w = 640
        resize_h = 480

        while cap.isOpened():
            ret, img = cap.read()
            if ret:
                imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                result = self.pose.process(imgRGB)

                if result.pose_landmarks:
                    self.mpDraw.draw_landmarks(img, result.pose_landmarks, self.mp_pose.POSE_CONNECTIONS, self.pointStyle, self.lineStyle)

                    for id, lm in enumerate(result.pose_landmarks.landmark):
                        h, w, c = img.shape
                        cx, cy = int(lm.x * w), int(lm.y * h)
                        cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)

                frame = cv2.flip(img, 1)
                cv2.imshow("Pose Detection", frame)

            if cv2.waitKey(1) == 27:
                break

        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    pose_control = PoseControl()
    pose_control.detect_pose()
