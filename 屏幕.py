import screen_brightness_control as sbc

# 获取当前亮度
current_brightness = sbc.get_brightness()
print(f"当前亮度: {current_brightness}")

# 设置亮度 (范围为 0 到 100)
sbc.set_brightness(50)
print("亮度已设置为 50%")
