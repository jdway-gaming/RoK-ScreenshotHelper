from time import sleep, time
import random
import os
import subprocess
from datetime import datetime
from matplotlib.image import imread, imsave
import numpy as np

if __name__ == '__main__':
    # Hyper-parameters
    IS_R4 = True
    # Nox adb route
    NOX_ADB_PATH = 'C:\\Program Files\\Nox\\bin\\adb.exe'
    NOX_PORT = '62028'
    NOX_SHARE_PATH = '/sdcard/Pictures/images'

    def exec_shell_command(command):
        st = time()
        chk = subprocess.call('{} -s 127.0.0.1:{} shell {}'.format(NOX_ADB_PATH, NOX_PORT, command))
        print('- [{:.4f}] command executed: {}'.format(time() - st, command))
        return chk
    screenshot = lambda img_name: exec_shell_command('screencap -p {}/{}.png'.format(NOX_SHARE_PATH, img_name))
    tap = lambda x, y: exec_shell_command('input tap {} {}'.format(x, y))
    swipe = lambda x1, y1, x2, y2: exec_shell_command('input swipe {} {} {} {}'.format(x1, y1, x2, y2))
    # path for image to check
    PATH_TO_CHECK_IMAGE = 'C:\\Users\\jdway\\Nox_share\\ImageShare\\Images\\check.png'
    record_check_image = lambda: screenshot('check')
    get_t = lambda: datetime.utcnow().strftime('%Y-%m-%d@%H-%M-%S-%f')
    # Coords
    start_point = [325, 255]
    stride_y = 79
    stride_x = 480
    # button 1: button to open information panel
    button_1_bias = [0, -35] if not IS_R4 else [0, -60]
    button_info = [325, 530]  # button to open detail panel
    # exit buttons
    exit1 = [1115, 45]
    exit2 = [1090, 80]
    # check_coord
    check_img_path = 'sample/helper/'
    person_detail = (450, 475, 600, 680)  # y1, y2, x1, x2
    person_info = (510, 550, 295, 350)  # y1, y2, x1, x2
    person_info_img = imread(os.path.join(check_img_path, 'person_info.png'))
    person_detail_img = imread(os.path.join(check_img_path, 'person_detail.png'))
    check_rally = (155, 185, 370, 400)  # y1, y2, x1, x2
    rally_img = imread(os.path.join(check_img_path, 'rally.png'))
    # random function
    r = lambda mean, bias=5: mean + random.randint(-1 * bias, bias)

    # function to check returning value from Nox
    def check_func(chk):
        if chk != 0:
            raise ValueError('Value check failed: {}'.format(chk))

    st = time()
    for y in range(0, 6):
        for x in range(2):
            print('[{}/{}] Recording player information...'.format(y * 2 + x, 12))
            # move to person icon
            coord_x = start_point[0] + x * stride_x
            coord_y = start_point[1] + y * stride_y
            check_func(tap(r(coord_x), r(coord_y)))
            # click info button
            additional_bias = -40 if y == 5 and IS_R4 else 0
            check_func(tap(r(coord_x + button_1_bias[0]), r(coord_y + button_1_bias[1] + additional_bias)))
            # check (1) if person info shows up, and (2) if rally panel shows up (which will block person's ID)
            sleep(.2)
            while True:
                check_func(record_check_image())
                chk_img = imread(PATH_TO_CHECK_IMAGE)
                chk_person_info = chk_img[person_info[0]:person_info[1], person_info[2]:person_info[3]]
                chk_val = np.sum(chk_person_info - person_info_img)
                chk_rally = chk_img[check_rally[0]:check_rally[1], check_rally[2]:check_rally[-1]]
                chk_rally_value = np.sum(rally_img - chk_rally)
                if chk_val == 0 and chk_rally_value != 0:
                    break
            # screen shot person's info
            check_func(screenshot(get_t()))
            # click detail info button
            check_func(tap(r(button_info[0]), r(button_info[1])))
            # check if person detail shows up
            sleep(.2)
            while True:
                check_func(record_check_image())
                chk_img = imread(PATH_TO_CHECK_IMAGE)[person_detail[0]:person_detail[1], person_detail[2]:person_detail[3]]
                chk_val = np.sum(chk_img - person_detail_img)
                if chk_val == 0:
                    break
            # move to screen shot button
            check_func(screenshot(get_t()))
            # exit the detail info
            check_func(tap(r(exit1[0]), r(exit1[1])))
            # check if person info button shows up
            sleep(.2)
            while True:
                check_func(record_check_image())
                chk_img = imread(PATH_TO_CHECK_IMAGE)[person_info[0]:person_info[1], person_info[2]:person_info[3]]
                chk_val = np.sum(chk_img - person_info_img)
                if chk_val == 0:
                    break
            # exit the personal info
            check_func(tap(r(exit2[0]), r(exit2[1])))

    print('Time spend: {}'.format(time() - st))
    os.remove(PATH_TO_CHECK_IMAGE)
