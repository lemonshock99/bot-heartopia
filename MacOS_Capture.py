import Quartz
import numpy as np

def capture_window(window_id):
    image = Quartz.CGWindowListCreateImage(
        Quartz.CGRectNull,
        Quartz.kCGWindowListOptionIncludingWindow,
        window_id,
        Quartz.kCGWindowImageDefault
    )

    width = Quartz.CGImageGetWidth(image)
    height = Quartz.CGImageGetHeight(image)

    data = Quartz.CGDataProviderCopyData(Quartz.CGImageGetDataProvider(image))
    img = np.frombuffer(data, dtype=np.uint8).reshape((height, width, 4))

    return img[:, :, :3]