import time
import threading
import wmi
from playsound import playsound
from PIL import Image, ImageDraw
import pystray


def create_icon():
    """创建托盘图标（简单摄像头图案）"""
    img = Image.new("RGB", (64, 64), color=(0, 0, 0))
    d = ImageDraw.Draw(img)
    d.ellipse((16, 16, 48, 48), outline="white", width=4)
    return img


class CameraMonitor:
    def __init__(self):
        self.running = True
        self.icon = pystray.Icon(
            "CameraMonitor",
            create_icon(),
            "Camera Monitor",
            menu=pystray.Menu(
                pystray.MenuItem("退出程序", self.stop)
            ),
        )

    def stop(self):
        self.running = False
        self.icon.stop()

    def monitor_camera(self):
        c = wmi.WMI()
        last_status = None

        while self.running:
            cameras = (
                c.Win32_PnPEntity(Name="Integrated Camera")
                or c.Win32_PnPEntity(Name="USB Camera")
                or c.Win32_PnPEntity(Name="HD Camera")
            )

            status = cameras[0].Status if cameras else "Unknown"

            if status != last_status:
                if status == "OK":
                    playsound("alert.mp3")
                last_status = status

            time.sleep(1)

    def run(self):
        t = threading.Thread(target=self.monitor_camera, daemon=True)
        t.start()
        self.icon.run()


if __name__ == "__main__":
    CameraMonitor().run()
