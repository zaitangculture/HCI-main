from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
from ctypes import cast, POINTER

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

# 获取当前音量
current_volume = volume.GetMasterVolumeLevelScalar()
print(f"当前音量: {current_volume}")

# 设置音量 (范围为 0.0 到 1.0)
volume.SetMasterVolumeLevelScalar(0.5, None)
print("音量已设置为 50%")
