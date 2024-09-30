from pynput.mouse import Button, Controller as MouseController
from pynput.keyboard import Controller as KeyboardController
import time
import math
print("Start")
time.sleep(1)  # 延时2秒


mouse = MouseController()
keyboard = KeyboardController()

# 移动鼠标到屏幕坐标 (100, 100)
mouse.position = (100, 100)
mouse.click(Button.left)
# 输入文本
keyboard.type('Hello, world!')
for i in range(1000):
    mouse.position = (i*math.sin(i), i)
    time.sleep(0.00001)
print("End")
