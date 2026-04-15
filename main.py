from WindowsCapture import *
import cv2 as cv
from MyClassbot import *
import time
from pyautogui import click
import Classclick
import keyboard


Game = 'Heartopia'
windows =  WindowCapture(Game)
action = Classclick.Click(Game)

print("prepare in 3 sec ....")
time.sleep(3)
print("Start !!!!")

count = 0

myCookData = {
    # 'cook': 'img/cook.jpg',
    # 'start_cook': 'img/start_cook.jpg',
    # 'product': 'img/product.jpg',
    'product0': 'img/product0.png',
    # 'product1': 'img/product1.jpg',
    # 'product2': 'img/product2.jpg',
    # 'product3': 'img/product3.jpg',
    # 'product4': 'img/product4.jpg',
    # 'finishcook': 'img/finishcook.jpg',
    # 'mushroom': 'img/mushroom.jpg',
    # 'grape_jam': 'img/grape_jam.jpg'
    
}


while True:

    if keyboard.is_pressed('q'):  # กด q เพื่อหยุด
        print("Stopped by user")
        break

    screen = windows.screenshot()
    print(f"Concurrent cook: {count}")

# ====================================================
# process food

    for name, path in myCookData.items():
        search = Classbot(screen, path)
        point = search.search(debug=False, myText=name, threshold=0.75)
        print("Process Food Location: {}", point)
        for myclick in point:
            action.click_legacy(x=myclick[0], y=myclick[1])
            
# ====================================================
# start
    if count <= 2:
        search = Classbot(screen, 'img/cook.png')
        point = search.search(debug=False, myText='Start Cook', threshold=0.8)
        if len(point) != 0:
            action.click_legacy(point[0][0], point[0][1])

        search = Classbot(screen, 'img/start_cook.jpg')
        point = search.search(debug=False, myText='Start Cook', threshold=0.8)
        print("Start Location: {}", point)
        if len(point) != 0:
            for myclick in point:
                action.click_legacy(x=myclick[0], y=myclick[1])
                count = min(2, count + 1)
                break

            

# ====================================================
# collect food
    search = Classbot(screen, 'img/finishcook.png')
    point = search.search(debug=False, myText='finish Cook', threshold=0.8)
    if len(point) != 0:
        for myclick in point:
            action.click_legacy(x=myclick[0], y=myclick[1])
            count = max(0, count - 1)
            time.sleep(1.5)
            print('Collect Complete ******')
            break


# ====================================================

    # search = Classbot(screen, 'img/cook.jpg')
    # point = search.search(debug=True, myText='Cook', threshold=0.8)
    time.sleep(0.3)

    # for myclick in point:
    #     click(x=myclick[0], y=myclick[1])


    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break