import cv2 as cv
import pyautogui
import time
from WindowsCapture import *
import keyboard
import pydirectinput

size_paint_x = 128
size_paint_y = 128

class Classbotdrawing:

    def __init__(self, main_img, temp_img):
        self.windowsname = 'Heartopia'
        # self.main_img = cv.imread(main_img,cv.IMREAD_ANYCOLOR)
        self.main_img = main_img
        # self.main_img = cv.cvtColor(self.main_img, cv.COLOR_BGR2GRAY)
        if temp_img != "":
            self.temp_img = cv.imread(temp_img,cv.IMREAD_ANYCOLOR)
            # self.temp_img = cv.cvtColor(self.temp_img, cv.COLOR_BGR2GRAY)

    def search(self, threshold = 0.8, debug=False, myText = ''):
        result = cv.matchTemplate(self.main_img,self.temp_img,cv.TM_CCOEFF_NORMED)
        _,maxval,_,maxloc = cv.minMaxLoc(result)
        print(maxval,maxloc)
        threshold = threshold

        locations = np.where(result >= threshold)
        locations = list(zip(*locations[::-1]))
        # print(locations)

        height = self.temp_img.shape[0]
        width = self.temp_img.shape[1]

        point = []
        rectangles = []
        for loc in locations:
            rect = [int(loc[0]), int(loc[1]),width, height]
            rectangles.append(rect)
            rectangles.append(rect)

        # group Rectangular
        rectangles, _ = cv.groupRectangles(rectangles, groupThreshold=1, eps=0.5)
        # print(rectangles)
 
        if len(rectangles):
            for (x, y, w, h) in rectangles:
                # print(x, y, w, h)
                topleft = (x,y)
                bottomright = (x+w, y+h)
                # print(topleft)
                # print(bottomright)
                # get X,Y
                centerX = x
                centerY = y
                print(f"Center X is: {centerX} Center Y is: {centerY}")
                # add center X Y to point variable
                point.append((centerX,centerY))

                if debug == True:
                    font = cv.FONT_ITALIC
                    position = (topleft[0], topleft[1])
                    fontsize = 0.5
                    color = (255,0,0)

                    # draw Rectangular
                    cv.rectangle(self.main_img, topleft, bottomright, color=(255,255,0),thickness=3,lineType=cv.LINE_4)
                    # draw marker in img
                    cv.drawMarker(self.main_img, (centerX, centerY), color=(0,0,255), markerSize=30, markerType=cv.MARKER_STAR, thickness=1)
                    cv.putText(self.main_img, myText, position,font, fontsize,color,thickness=2)

        else:
            print("not Matching")
        if debug:
            cv.imshow("result", self.main_img)
            # cv.waitKey()
            # cv.destroyAllWindows()
        return point
    
    def getHwID(self):
        return win32gui.FindWindow(None, self.windowsname)
    
    def window_to_screen(self, x, y):
        hwnd = self.getHwID()
        # แปลง (x,y) จาก window → screen
        point = win32gui.ClientToScreen(hwnd, (x, y))
        return point

Game = 'Heartopia'
windows =  WindowCapture(Game)
screen = windows.screenshot()

# ====================================================
img = cv.imread("img/duck.png")
img = cv.resize(img, (size_paint_x, size_paint_y))

# ลดเหลือ 8 สี
Z = img.reshape((-1, 3))
Z = np.float32(Z)

K = 4
_, label, center = cv.kmeans(
    Z, K, None,
    (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 10, 1.0),
    10,
    cv.KMEANS_RANDOM_CENTERS
)

center = np.uint8(center)
quantized = center[label.flatten()]
img = quantized.reshape((size_paint_x, size_paint_y, 3))

# print(img)

colors = np.unique(img.reshape(-1, 3), axis=0)
print(colors)
# ====================================================

cv.imshow("result", img)
cv.waitKey()
cv.destroyAllWindows()

# ====================================================

search = Classbotdrawing(screen, 'img/pane.jpg')
point = search.search(debug=False, myText="", threshold=0.9)


# start_x, start_y = search.window_to_screen(point[0][0], point[0][1])
start_x = 375
start_y = 252
start_x, start_y = search.window_to_screen(start_x, start_y)
pixel_size = 6

time.sleep(3)  # ให้เวลาสลับไปเกม

# กำหนด background (เช่น สีขาว)
def is_background(pixel):
    b, g, r = pixel
    return b > 240 and g > 240 and r > 240  # ปรับ threshold ได้

# time.sleep(3)
print("prepare to start ....")

last_color = search.window_to_screen(1630, 779)
orange = search.window_to_screen(1850, 430)
darkblue = search.window_to_screen(1725, 775)
blue = search.window_to_screen(1853, 689)

color1 = search.window_to_screen(1726, 436)
color2 = search.window_to_screen(1850, 435)
color3 = search.window_to_screen(1726, 519)
color4 = search.window_to_screen(1850, 519)

color_list = [color4, color2, color3, color1]

# print(colors[::-1])

# for i, color in enumerate(colors[3::-1]):

margin_x = 0
margin_y_count = 0
margin_y = 0

for i, color in enumerate(colors):
    color = tuple(color)

    print(i, color)
    # 🎨 เลือกสีในเกม
    px, py = color_list[i]
    pydirectinput.moveTo(px, py)
    pydirectinput.mouseDown()
    pydirectinput.mouseUp()
    time.sleep(0.2)
    time.sleep(3)
    # ✏️ วาดเฉพาะ pixel สีนี้
    for y in range(size_paint_y):

        if margin_y_count >= 6:
            margin_y = margin_y + pixel_size
            margin_y = 0

        drawing = False
        game_y = start_y + margin_y + y * pixel_size

        for x in range(size_paint_x):
            pixel = tuple(img[y, x])
            game_x = start_x + x * pixel_size

            if pixel == color:
                if not drawing:
                    pydirectinput.moveTo(game_x, game_y)
                    pydirectinput.mouseDown()
                    drawing = True
                else:
                    pydirectinput.moveTo(game_x, game_y)

            else:
                if drawing:
                    pydirectinput.mouseUp()
                    drawing = False

            if keyboard.is_pressed('q'):
                print("Stopped")
                exit()

        if drawing:
            pydirectinput.mouseUp()

        margin_y_count = margin_y_count + 1

        if keyboard.is_pressed('q'):
            print("Stopped")
            exit()