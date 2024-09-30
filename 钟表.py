import sys
from PyQt5.QtCore import QTimer, QTime, Qt
from PyQt5.QtGui import QPainter, QColor, QPen, QFont
from PyQt5.QtWidgets import QApplication, QWidget

class Clock(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Circular Clock')
        self.setGeometry(100, 100, 400, 400)
        self.setStyleSheet("background-color: black;")
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(1000)  # Update every second

        self.show()

    def paintEvent(self, event):
        currentTime = QTime.currentTime()
        hour = currentTime.hour() % 12
        minute = currentTime.minute()
        second = currentTime.second()

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        side = min(self.width(), self.height())
        painter.translate(self.width() / 2, self.height() / 2)
        painter.scale(side / 200.0, side / 200.0)

        # Draw clock background
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(0, 128, 128))
        painter.drawEllipse(-95, -95, 190, 190)

        # Draw clock marks
        painter.setPen(QPen(QColor(255, 255, 255), 2))
        for i in range(60):
            painter.drawLine(88, 0, 96, 0)
            painter.rotate(6.0)

        # Draw clock numbers
        font = QFont('Arial', 10)
        painter.setFont(font)
        for i, number in enumerate(range(1, 13), 1):
            painter.save()
            painter.rotate(-30 * i)
            painter.translate(0, -78)
            painter.rotate(30 * i)
            painter.drawText(-10, 10, str(number))
            painter.restore()

        # Draw hour hand
        painter.save()
        painter.setPen(QPen(QColor(255, 255, 255), 8, Qt.SolidLine, Qt.RoundCap))
        painter.rotate(30.0 * (hour + minute / 60.0))
        painter.drawLine(0, 0, 0, -50)
        painter.restore()

        # Draw minute hand
        painter.save()
        painter.setPen(QPen(QColor(255, 255, 255), 6, Qt.SolidLine, Qt.RoundCap))
        painter.rotate(6.0 * (minute + second / 60.0))
        painter.drawLine(0, 0, 0, -70)
        painter.restore()

        # Draw second hand
        painter.save()
        painter.setPen(QPen(QColor(255, 0, 0), 2, Qt.SolidLine, Qt.RoundCap))
        painter.rotate(6.0 * second)
        painter.drawLine(0, 0, 0, -90)
        painter.restore()

        # Draw clock center
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(255, 255, 255))
        painter.drawEllipse(-5, -5, 10, 10)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    clock = Clock()
    sys.exit(app.exec_())
