import cv2 as cv
import numpy as np

class Classbot:
    def __init__(self, main_img, temp_img):
        self.main_img = cv.imread(main_img,cv.IMREAD_ANYCOLOR)
        self.temp_img = cv.imread(temp_img,cv.IMREAD_ANYCOLOR)

    def search(self):
        result = cv.matchTemplate(self.main_img,self.temp_img,cv.TM_CCOEFF_NORMED)
        _,maxval,_,maxloc = cv.minMaxLoc(result)
        print(maxval,maxloc)
        threshold = 0.9
        if maxval >= threshold:
            topleft = maxloc

            # get shape
            height = self.temp_img.shape[0]
            width = self.temp_img.shape[1]

            # draw Rectangular
            bottomright = (topleft[0]+width, topleft[1]+height)
            cv.rectangle(self.main_img, topleft, bottomright, color=(255,255,0),thickness=3,lineType=cv.LINE_4)

            # put text
            font = cv.FONT_ITALIC
            position = (topleft[0], topleft[1])
            fontsize = 0.5
            color = (255,0,0)
            cv.putText(self.main_img, "TEXT", position,font, fontsize,color,thickness=2)

            cv.imshow("result", self.main_img)
            cv.waitKey()
            cv.destroyAllWindows()


mybot = Classbot('img/03.jpg', 'img/temp.jpg')
mybot.search()