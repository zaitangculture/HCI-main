import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QSlider
from PyQt5.QtCore import Qt
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
from ctypes import cast, POINTER

class VolumeControl(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.initVolumeControl()

    def initUI(self):
        self.setWindowTitle('Volume Control')
        self.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout()

        self.label = QLabel('Volume: 50', self)
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.setMinimum(0)
        self.slider.setMaximum(100)
        self.slider.setValue(50)
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.setTickInterval(10)
        self.slider.valueChanged.connect(self.on_value_changed)
        layout.addWidget(self.slider)

        self.setLayout(layout)

    def initVolumeControl(self):
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self.volume = cast(interface, POINTER(IAudioEndpointVolume))

        # 设置初始音量
        current_volume = self.volume.GetMasterVolumeLevelScalar()
        self.slider.setValue(int(current_volume * 100))

    def on_value_changed(self, value):
        self.label.setText(f'Volume: {value}')
        self.volume.SetMasterVolumeLevelScalar(value / 100, None)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = VolumeControl()
    ex.show()
    sys.exit(app.exec_())
