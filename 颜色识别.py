import cv2
import numpy as np

# 定义颜色范围（以HSV为基础）
color_ranges = {
    "Red": ([0, 120, 70], [10, 255, 255]),
    "Green": ([36, 25, 25], [86, 255, 255]),
    "Blue": ([94, 80, 2], [126, 255, 255])
}

# 打开视频捕捉设备
cap = cv2.VideoCapture(0)

# 形态学操作的内核
kernel = np.ones((5, 5), np.uint8)

while True:
    # 读取一帧
    ret, frame = cap.read()
    if not ret:
        break

    # 将帧从 BGR 转换为 HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    for color_name, (lower, upper) in color_ranges.items():
        lower = np.array(lower, dtype=np.uint8)
        upper = np.array(upper, dtype=np.uint8)

        # 创建颜色遮罩
        mask = cv2.inRange(hsv, lower, upper)

        # 形态学操作去除噪声
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

        # 查找遮罩中的轮廓
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 500:  # 过滤掉小面积的噪声
                x, y, w, h = cv2.boundingRect(contour)
                color = (0, 255, 0) if color_name == "Green" else (0, 0, 255) if color_name == "Red" else (255, 0, 0)
                cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                cv2.putText(frame, color_name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

    # 显示图像
    cv2.imshow('Color Tracking', frame)

    # 按下 'ESC' 键退出
    if cv2.waitKey(1) & 0xFF == 27:
        break

# 释放资源
cap.release()
cv2.destroyAllWindows()
