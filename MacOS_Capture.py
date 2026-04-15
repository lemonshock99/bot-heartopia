import Quartz
import numpy as np

class WindowCapture:
    def __init__(self, window_name):
        # find the handle for the window we want to capture
        self.hwnd = win32gui.FindWindow(None, window_name)
        if not self.hwnd:
            raise Exception('Window not found: {}'.format(window_name))

    def screenshot(self):
        image = Quartz.CGWindowListCreateImage(
            Quartz.CGRectNull,
            Quartz.kCGWindowListOptionIncludingWindow,
            self.hwnd,
            Quartz.kCGWindowImageDefault
        )

        width = Quartz.CGImageGetWidth(image)
        height = Quartz.CGImageGetHeight(image)

        data = Quartz.CGDataProviderCopyData(Quartz.CGImageGetDataProvider(image))
        img = np.frombuffer(data, dtype=np.uint8).reshape((height, width, 4))
        return img[:, :, :3]
    
    def findwindowsid(self):
        windows = Quartz.CGWindowListCopyWindowInfo(
            Quartz.kCGWindowListOptionOnScreenOnly,
            Quartz.kCGNullWindowID
        )

        windows_name = ""
        for w in windows:
            # print(w.get('kCGWindowNumber'), w.get('kCGWindowOwnerName'), w.get('kCGWindowName'))
            windows_name = w.get('kCGWindowNumber')