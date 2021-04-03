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
    for frequency in range(500, 3000, 500):
        winsound.Beep(frequency, duration)


def edit_pic_path(file_name):
    return os.path.dirname(sys.argv[0])+'\\'+file_name


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


def windowScreenshot(window_title=None):
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


def wait(pos, bgr, print_str='no str'):
    while True:
        if pyautogui.pixelMatchesColor(*pos, bgr):
            break
        print('wait for '+print_str)
        time.sleep(1)
    print('found '+print_str)
    time.sleep(1.5)


def key_hold(key, hold_time):
    pyautogui.keyDown(key)
    time.sleep(hold_time)
    pyautogui.keyUp(key)


def window_cal(constant, win_pos, scan=None):
    for obj in constant['pos']:
        constant['pos_cal'][obj] = tuple(map(operator.add,
                                             constant['pos'][obj], win_pos))
        if scan is not None:
            constant[scan][obj] = pyautogui.pixel(*constant['pos_cal'][obj])
            ''' debug '''
            # pyautogui.moveTo(constant['pos_cal'][obj])
            if obj in constant['init'] and obj in constant['now']:
                constant['cd'][obj] = constant['init'][obj] \
                                      == constant['now'][obj]
                # print(obj, constant['cd'][obj])
            ''' debug '''


def wait_casting(const):
    ''' wait delay 1s '''
    time.sleep(1)
    while True:
        if pyautogui.pixel(*const['pos_cal']['cast']) \
           != const['color']['cast']:
            break
        print('casting')
        time.sleep(0.5)
    print('cast end')

def wait_cooldown(skill_const, skill_list):
    for skill in skill_list:
        while True:
            now = pyautogui.pixel(*skill_const['pos_cal'][skill])
            if now == skill_const['init'][skill]:
                pyautogui.press(skill[1:])
                break
            print('wait for cooldown skill ' + skill)
            time.sleep(1)
        print(skill + ' used')


def get_pixel():

    const = {'pos': {}, 'color': {}, 'pos_cal': {}}
    const['pos']['ui'] = (582, 440)
    const['pos']['talk'] = (180, 260)
    # const['pos']['panda'] = (209, 458)
    const['pos']['create'] = (525, 307)
    const['pos']['start'] = (525, 307)
    const['pos']['quit'] = (570, 395)
    const['pos']['text'] = (177, 361)
    const['pos']['cast'] = (297, 285)
    const['color']['ui'] = (111, 111, 88)
    # const['color']['panda'] = (242, 197, 143)
    const['color']['create'] = (50, 37, 17)
    const['color']['start'] = (244, 243, 241)
    const['color']['quit'] = (76, 60, 40)
    const['color']['text'] = (216, 200, 176)
    const['color']['cast'] = (90, 73, 57)

    skill_const = {'pos': {}, 'pos_cal': {}, 'init': {}, 'now': {}, 'cd': {}}
    for i in range(10):
        skill_const['pos']['s'+str(i+1)] = (int(248+31.5*i), 459)  # s1-s10
    win_pos = windowScreenshot('12TailsTH')[1]
    window_cal(skill_const, win_pos, scan='init')
    window_cal(skill_const, win_pos, scan='now')

    while True:
        img, win_pos = windowScreenshot('12TailsTH')
        window_cal(const, win_pos)
        window_cal(skill_const, win_pos, scan='now')  # get skill_const['cd']
        # print(skill_const['cd']['s1'])

        ''' 1/1 mole '''
        #wait(const['pos_cal']['text'], const['color']['text'], 'text')
        #pyautogui.click(clicks=3, interval=2)
        wait(const['pos_cal']['ui'], const['color']['ui'], 'ui_mission')
        wait_cooldown(skill_const, ['s1'])
        wait_casting(const)
        key_hold('w', 4)
        wait_cooldown(skill_const, ['s1'])
        wait_casting(const)
        key_hold('q', 4)
        wait_cooldown(skill_const, ['s1'])
        wait_casting(const)
        key_hold('s', 4)
        wait_cooldown(skill_const, ['s1'])
        wait_casting(const)
        key_hold('e', 4)

        ''' 1/1 mole '''


        ''' quit to start '''
        wait(const['pos_cal']['ui'], const['color']['ui'], 'ui_mission')
        pyautogui.press('f3', interval=1)
        wait(const['pos_cal']['quit'], const['color']['quit'], 'quit')
        pyautogui.click(*const['pos_cal']['quit'])
        ''' camp '''
        wait(const['pos_cal']['ui'], const['color']['ui'], 'ui_home')
        key_hold('s', 1.5)
        key_hold('q', 1.5)
        pyautogui.click(*const['pos_cal']['talk'])
        wait(const['pos_cal']['create'], const['color']['create'], 'create')
        time.sleep(1)
        pyautogui.click(*const['pos_cal']['create'])
        wait(const['pos_cal']['start'], const['color']['start'], 'start')
        pyautogui.click(*const['pos_cal']['start'])
        ''' quit to start  '''


        posXY = pyautogui.position()
        color = pyautogui.pixel(posXY[0], posXY[1])

        cal_posXY = (posXY[0]-win_pos[0], posXY[1]-win_pos[1])


        print('m pos:', posXY,
              'm color:', color,
              'cal pos:', cal_posXY,
              'debug:', pyautogui.pixel(*const['pos_cal']['cast']))




        open_cv_image = np.array(color)
        open_cv_image = open_cv_image[::-1]
        image = np.zeros((300, 300, 3), np.uint8)
        image[:] = open_cv_image

        time.sleep(0.2)
        # cv2.imshow('w', image)
        # cv2.waitKey(1)

        if posXY[0] == 0:
            break


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
    time.sleep(2)
    get_pixel()
    main()
