from ultralytics import YOLO
import cv2

# 加载 YOLOv8 模型
model = YOLO('yolov8n.pt')  # 你可以使用其他权重文件，如 'yolov8s.pt', 'yolov8m.pt', 'yolov8l.pt', 'yolov8x.pt'

# 打开摄像头
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    # 对帧进行对象检测
    results = model(frame)

    # 可视化结果
    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            confidence = box.conf.item()
            class_id = box.cls.item()
            label = f'{model.names[class_id]} {confidence:.2f}'
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # 显示结果
    cv2.imshow('YOLOv8 Detection', frame)
    
    if cv2.waitKey(1) == 27:  # 按 ESC 退出
        break

cap.release()
cv2.destroyAllWindows()
