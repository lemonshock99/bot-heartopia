import Quartz
import numpy as np

class WindowCapture:
    def __init__(self, window_name):
        # self.hwnd = self.findwindowsid(window_name)
        self.hwnd = 88
        print(self.hwnd)

    def screenshot(self):
        image = Quartz.CGWindowListCreateImage(
            Quartz.CGRectNull,
            Quartz.kCGWindowListOptionIncludingWindow,
            self.hwnd,
            Quartz.kCGWindowImageDefault
        )

        width = Quartz.CGImageGetWidth(image)
        height = Quartz.CGImageGetHeight(image)
        bytes_per_row = Quartz.CGImageGetBytesPerRow(image)

        data = Quartz.CGDataProviderCopyData(
            Quartz.CGImageGetDataProvider(image)
        )

        # 🔥 reshape ด้วย stride จริง
        img = np.frombuffer(data, dtype=np.uint8)
        img = img.reshape((height, bytes_per_row // 4, 4))

        # ✂️ crop เอาเฉพาะ width จริง
        img = img[:, :width, :3]

        print(img)

        return img
    
    def findwindowsid(self, windows_name):
        windows = Quartz.CGWindowListCopyWindowInfo(
            Quartz.kCGWindowListOptionOnScreenOnly,
            Quartz.kCGNullWindowID
        )

        for w in windows:
            print(w.get('kCGWindowNumber'), w.get('kCGWindowOwnerName'), w.get('kCGWindowName'))
            if w.get('kCGWindowName') == windows_name:
                return w.get('kCGWindowNumber')
            else: return None

# test = WindowCapture("BlueStacks")
# test.screenshot()