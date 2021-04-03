import sys
import os
import pyautogui
import subprocess
import time
import win32gui
import winsound
import keyboard
import cv2
import numpy as np
import operator

#sys.exit()

Counter = 0
Active = 0
Exit = False

def beep():
    duration = 500
    for frequency in range(500, 3000,500):
        winsound.Beep(frequency, duration)

def edit_pic_path(file_name):
    return os.path.dirname(sys.argv[0])+'\\'+file_name

def error_handle():
    while True:
        hwnd = win32gui.FindWindow(None,'ERROR')
        if hwnd != 0:
            win32gui.SetForegroundWindow(hwnd)
            pyautogui.press('enter')
            break
        else:
            print('fail')
        time.sleep(0.1)
def start_client():
    while True:
        try:
            pyautogui.click(edit_pic_path('start.png'))
        except Exception:
            print('not found start')
        else:
            print('start clicked')
            break
        time.sleep(0.5)
def login():
    while True:
        location = pyautogui.locateOnScreen(edit_pic_path('start2.png'), grayscale=True)
        if location is not None:
            print('found login page')
            time.sleep(0.1)
            pyautogui.write(id, interval=0.05)
            pyautogui.press('tab')
            pyautogui.write(ps, interval=0.05)
            pyautogui.press('enter')
            break
        else:
            print('wait for login page')
        time.sleep(0.5)

def xigncode():
    while True:
        location = pyautogui.locateOnScreen(edit_pic_path('xigncode.png'), grayscale=True)
        server = pyautogui.locateOnScreen(edit_pic_path('server_name.png'), grayscale=True)
        if location is not None:
            print('found xigncode')
            time.sleep(1)
            pyautogui.click(edit_pic_path('OK.png'))
            output = 'found xigncode'
            break
        else:
            print('wait for xigncode')
        if server is not None:
            print('end')
            output = 'found server name'
            break
        time.sleep(1)
    return output

def checkKey(key, func=None):
    if keyboard.is_pressed(str(key)):
        if func is not None:
            func()
        time.sleep(0.2)  # prevent bouncing button

def triggeredSpace():
    global Active, Counter
    print("space")
    if Counter == 0:
        Counter = 1
    Active = not Active

def triggeredEsc():
    global Exit
    Exit = True

def windowScreenshot(window_title=None, wpercent=50, hpercent=50):
    if window_title:
        hwnd = win32gui.FindWindow(None, window_title)
        if hwnd:
            win32gui.SetForegroundWindow(hwnd)
            x, y, x1, y1 = win32gui.GetClientRect(hwnd)
            x, y = win32gui.ClientToScreen(hwnd, (x, y))
            x1, y1 = win32gui.ClientToScreen(hwnd, (x1 - x, y1 - y))
            raw_img = pyautogui.screenshot(region=(x, y, x1, y1))
            raw_img = cv2.cvtColor(np.array(raw_img), cv2.COLOR_RGB2BGR)
            return raw_img, (x, y)
        else:
            print('Window not found!')

def get_pixel():

    const = {'pos':{},'color':{}}
    const['pos']['ui'] = (582, 440)
    const['pos']['talk'] = (171, 260)
    const['pos']['panda'] = (209, 458)
    const['pos']['create'] = (525, 307)
    const['pos']['quit'] = (570, 395)
    const['color']['ui'] = (111, 111, 88)
    const['color']['panda'] = (242, 197, 143)


    while True:
        try:
            #button7location = pyautogui.locateOnScreen(edit_pic_path('Talk.png'))
            #print(button7location)
            pass
        except:
            pass
        img, win_pos = windowScreenshot('12TailsTH')
        for obj in const['pos']:
            const['pos_cal'][obj] = tuple(map(operator.add,
                                              const['pos']['create'],
                                              win_pos))

        posXY = pyautogui.position()
        color = pyautogui.pixel(posXY[0], posXY[1])
        open_cv_image = np.array(color)
        # print(posXY[0]-x,posXY[1]-y)
        # Convert RGB (33, 189, 236) to BGR (236, 189, 33) blue
        # Convert RGB (247, 3, 2) to BGR (2, 3, 247) red
        # Convert RGB (140, 247, 231) to BGR (231, 247, 140) talk
        # print(pyautogui.pixelMatchesColor(300,300,(248,248,248)))
        open_cv_image = open_cv_image[::-1]
        #print(posXY, color)
        time.sleep(0.2)
        image = np.zeros((300, 300, 3), np.uint8)
        image[:] = open_cv_image
        cv2.imshow('w', image)
        cv2.waitKey(1)
        if posXY[0] == 0:
            break




        print(color)

def main():

    global Active, Counter, Exit
    while not Exit:
        checkKey('space', triggeredSpace)
        checkKey('esc', triggeredEsc)
        if Active == 1:
            print('mainloop')
            '''
            error_handle()
            start_client()
            login()
            server = xigncode()
            if server == 'found server name' :
                break
            '''
            time.sleep(1)

if '__main__' == __name__ :
    get_pixel()
    main()
