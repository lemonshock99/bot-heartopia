import cv2 as cv
import numpy as np

class Classbot:
    def __init__(self, main_img, temp_img):
        self.main_img = cv.imread(main_img,cv.IMREAD_ANYCOLOR)
        self.temp_img = cv.imread(temp_img,cv.IMREAD_ANYCOLOR)

    def search(self, threshold = 0.8, debug=False):
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
                centerX = x + int(w/2)
                centerY = y + int(h/2)
                print(f"Center X is: {centerX} Center Y is: {centerY}")
                # add center X Y to point variable
                point.append((centerX,centerY))

                if debug == True:
                    # draw Rectangular
                    cv.rectangle(self.main_img, topleft, bottomright, color=(255,255,0),thickness=3,lineType=cv.LINE_4)
                    # draw marker in img
                    cv.drawMarker(self.main_img, (centerX, centerY), color=(0,0,255), markerSize=30, markerType=cv.MARKER_STAR, thickness=1)

        else:
            print("not Matching")
        if debug:
            cv.imshow("result", self.main_img)
            cv.waitKey()
            cv.destroyAllWindows()
        return point

mybot = Classbot('img/01.jpg', 'img/cook.jpg')
my_point = mybot.search(debug=True)
for click in my_point:
    print(click)