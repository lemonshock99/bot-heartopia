import win32api, win32gui, win32con
import pydirectinput
import time

class Click:
    def __init__(self, windowsname):
        self.windowsname = windowsname
    
    def getHwID(self):
        return win32gui.FindWindow(None, self.windowsname)
    
    def click(self, x, y):
        hwnd = self.getHwID()
        
        if hwnd == 0:
            print("Window not found")
            return
        
        # แปลง x,y เป็น lParam
        lParam = win32api.MAKELONG(x, y)
        
        # ส่ง event click
        win32gui.SendMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
        win32gui.SendMessage(hwnd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, lParam)
        # win32gui.SendMessage(hwnd, win32con.WM_KEYDOWN, ord('x'), 0)
        # win32gui.SendMessage(hwnd, win32con.WM_KEYUP, ord('x'), 0)

    def click_legacy(self, x, y):
        point = self.window_to_screen(x, y)
        pydirectinput.moveTo(x=point[0], y=point[1])
        time.sleep(0.3)
        pydirectinput.mouseDown()
        time.sleep(0.2)
        pydirectinput.mouseUp()

    def window_to_screen(self, x, y):
        hwnd = self.getHwID()
        # แปลง (x,y) จาก window → screen
        point = win32gui.ClientToScreen(hwnd, (x, y))
        return point

if __name__ == "__main__":
    test = Click('Heartopia')
    # print(test.getHwID())
    # print(test.click(124, 40))
    # print(test.window_to_screen(500,500))
    test.click_legacy(850,58)