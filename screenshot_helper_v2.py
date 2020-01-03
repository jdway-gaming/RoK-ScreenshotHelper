from time import sleep, time
import random
import os
import subprocess
from datetime import datetime
from matplotlib.image import imread, imsave
import numpy as np
import argparse


def get_args():
    parser = argparse.ArgumentParser(description='ScreenshotHelper')
    parser.add_argument('--nox_adb_path', type=str, default='C:\\Program Files\\Nox\\bin\\adb.exe',
                        help='path to adb.exe')
    parser.add_argument('--nox_port', type=str, default='62028')
    parser.add_argument('--nox_share_path', type=str, default='/sdcard/Pictures/images')
    parser.add_argument('--path_check_image', type=str,
                        default='C:\\Users\\jdway\\Nox_share\\ImageShare\\Images\\check-{}.png')
    parser.add_argument('--is_r4', action='store_true', help='Either is R4 or not')
    parser.add_argument('--is_member', action='store_true', help='Either is the member of the alliance or not')
    parser.add_argument('--last_num', type=int, default=12, help='Will skip after this index (start with 0')
    return parser.parse_args()


def main(args):
    # Coords
    start_point = [325, 255]
    stride_y = 79
    stride_x = 480
    kill_detail_button = [895, 320]
    # button 1: button to open information panel
    if args.is_member:
        button_1_bias = [0, -35] if not args.is_r4 else [0, -60]
    else:
        button_1_bias = [520 - 325, 235 - 255]
    button_info = [325, 530]  # Coordinate of button to open detail panel
    # Coordinate of exit buttons
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

    # path for image to check
    path_check_image = args.path_check_image.format(args.nox_port)
    record_check_image = lambda: screenshot('check-{}'.format(args.nox_port))

    # defining functions
    def exec_shell_command(command):
        st = time()
        chk = subprocess.call('{} -s 127.0.0.1:{} shell {}'.format(args.nox_adb_path, args.nox_port, command))
        print('- [{:.4f}] command executed: {}'.format(time() - st, command))
        return chk

    screenshot = lambda img_name: exec_shell_command('screencap -p {}/{}.png'.format(args.nox_share_path, img_name))
    r = lambda mean, bias: mean + random.randint(-1 * bias, bias)

    def tap(coord_x, coord_y, random_bias=True, bias=5):
        if random_bias:
            coord_x = r(coord_x, bias)
            coord_y = r(coord_y, bias)
        return exec_shell_command('input tap {} {}'.format(coord_x, coord_y))
    get_t = lambda: '{}-{}'.format(args.nox_port, datetime.utcnow().strftime('%Y-%m-%d@%H-%M-%S-%f'))

    # function to check returning value from Nox
    def check_func(chk):
        if chk != 0:
            raise ValueError('Value check failed: {}'.format(chk))

    st = time()
    for y in range(0, 6):
        for x in range(2):
            print('[{}/{}] Recording player information...'.format(y * 2 + x, 12))
            if y * x + x > args.last_num:
                continue
            # ---- move to person icon
            coord_x = start_point[0] + x * stride_x
            coord_y = start_point[1] + y * stride_y
            check_func(tap(coord_x, coord_y))
            # ---- click info button
            additional_bias = -40 if y == 5 and args.is_r4 else 0
            check_func(tap(coord_x + button_1_bias[0], coord_y + button_1_bias[1] + additional_bias))
            # check (1) if person info shows up, and (2) if rally panel shows up (which will block person's ID)
            sleep(.2)
            while True:
                check_func(record_check_image())
                chk_img = imread(path_check_image)
                chk_person_info = chk_img[person_info[0]:person_info[1], person_info[2]:person_info[3]]
                chk_val = np.sum(chk_person_info - person_info_img)
                chk_rally = chk_img[check_rally[0]:check_rally[1], check_rally[2]:check_rally[-1]]
                chk_rally_value = np.sum(rally_img - chk_rally)
                if chk_val == 0 and chk_rally_value != 0:
                    break
            # ---- screen shot person's info
            check_func(screenshot(get_t()))
            # ---- open the kill detail
            check_func(tap(kill_detail_button[0], kill_detail_button[1]))
            sleep(.3)  # if screenshot was made during animation, won't able to be recognized via following program
            # ---- screen shot kill detail
            check_func(screenshot(get_t()))
            # ---- click detail info button
            check_func(tap(button_info[0], button_info[1]))
            # ---- check if person detail shows up
            sleep(.2)
            while True:
                check_func(record_check_image())
                chk_img = imread(path_check_image)[person_detail[0]:person_detail[1],
                          person_detail[2]:person_detail[3]]
                chk_val = np.sum(chk_img - person_detail_img)
                if chk_val == 0:
                    break
            # ---- move to screen shot button
            check_func(screenshot(get_t()))
            # ---- exit the detail info
            check_func(tap(exit1[0], exit1[1]))
            # ---- check if person info button shows up
            sleep(.2)
            while True:
                check_func(record_check_image())
                chk_img = imread(path_check_image)[person_info[0]:person_info[1], person_info[2]:person_info[3]]
                chk_val = np.sum(chk_img - person_info_img)
                if chk_val == 0:
                    break
            # ---- exit the personal info
            check_func(tap(exit2[0], exit2[1]))

    print('Time spend: {}'.format(time() - st))
    os.remove(path_check_image)


if __name__ == '__main__':
    main(get_args())
