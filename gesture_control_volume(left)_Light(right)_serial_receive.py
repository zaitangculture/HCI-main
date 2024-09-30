import serial

def main():
    ser = serial.Serial('COM3', 9600, timeout=1)  # 确保将 'COM3' 替换为你的串口端口
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('ascii').strip()
            print(f"Received: {line}")

if __name__ == "__main__":
    main()
