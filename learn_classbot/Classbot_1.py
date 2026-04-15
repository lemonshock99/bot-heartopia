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

        locations = np.where(result >= threshold)
        locations = list(zip(*locations[::-1]))
        print(locations)

        if locations:
            height = self.temp_img.shape[0]
            width = self.temp_img.shape[1]

            for loc in locations:
                bottom_right = (loc[0]+width, loc[1]+height)
                cv.rectangle(self.main_img, loc, bottom_right, color=(255,255,0),thickness=3,lineType=cv.LINE_4)


            cv.imshow("result", self.main_img)
            cv.waitKey()
            cv.destroyAllWindows()

mybot = Classbot('img/01.jpg', 'img/cook.jpg')
mybot.search()