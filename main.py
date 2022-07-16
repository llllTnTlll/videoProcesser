import os.path
import argparse
import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np
import datetime
from colorama import Fore
from colorama import Style


def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', default='./simples/10Hz.mp4', help='视频文件路径')
    parser.add_argument('--save', default='True', choices=['True', 'False'], help='是否将检测结果保存至本地txt文件')
    parser.add_argument('--left_top', nargs='+', type=int, default=[500, 600], help='左上角顶点坐标')
    parser.add_argument('--right-bottom', nargs='+', type=int, default=[800, 900], help='右下角顶点坐标')
    parser.add_argument('--color', nargs='+', type=int, default=[0, 0, 255], help='边框颜色(BGR)')
    opt = parser.parse_args()

    # 校验输入内容是否合法
    try:
        assert len(opt.left_top) == 2
    except AssertionError:
        print_info(f'左上角顶点坐标需要x,y两个值,而不是{len(opt.left_top)}个', 2)
        return

    try:
        assert len(opt.right_bottom) == 2
    except AssertionError:
        print_info(f'左上角顶点坐标需要x,y两个值,而不是{len(opt.right_bottom)}个', 2)
        return

    try:
        height = opt.right_bottom[1] - opt.left_top[1]
        width = opt.right_bottom[0] - opt.left_top[0]
        assert height > 0 and width > 0
    except AssertionError:
        print_info('请重新确认两点坐标相对位置（左上角顶点为[0,0]）', 2)
        return

    return opt


def get_avg_gray_value(img):
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    means, dev = cv.meanStdDev(gray)
    return means[0, 0]


def save2local(x_pts, y_pts, opt):
    if opt.save == "True":
        print(Style.BRIGHT + "\n===========SAVING TO LOCAL===========" + Style.RESET_ALL)
        # 生成保存路径
        file_name = os.path.splitext(os.path.split(opt.path)[-1])[0]
        save_dir = "./result"
        save_path = os.path.join(save_dir, file_name + '_result.txt')
        # 判断保存路径是否已经存在
        if not os.path.isdir(save_dir):
            os.makedirs(save_dir)
        # 判断结果文件是否存在
        # 若文件存在提示是否进行覆写操作
        try:
            if os.path.isfile(save_path):
                print_info("The result file already exists, do you want to overwrite it?", 1)
                if input("enter 'y' to confirm: ") != 'y':
                    print_info("Results not saved!", 1)
                    return
        except FileNotFoundError:
            pass
        # 将灰度值结果保存至本地
        with open(save_path, 'w') as f:
            for i in range(len(x_pts)):
                f.write(str(y_pts[i]) + '\n')
            print_info("Result saved!", 0)


def print_info(info, info_type):
    """
    以彩色形式显示提示信息
    :param info: 信息内容
    :param info_type: 0代表INFO类型
                      1代表WARNING类型
                      2代表ERROR类型
    """
    assert info_type in [0, 1, 2]
    d = str(datetime.datetime.now().strftime('%H:%M:%S'))
    if info_type == 0:
        info = d + Fore.GREEN + f" [INFO] {info}" + Fore.RESET
    elif info_type == 1:
        info = d + Fore.YELLOW + f" [WARNING] {info}" + Fore.RESET
    elif info_type == 2:
        info = d + Fore.RED + f" [ERROR] {info}" + Fore.RESET
    print(info)


def main(opt):
    # 待绘制点集
    x_points = []
    y_points = []

    # 读取视频文件并进行处理
    capture = cv.VideoCapture(opt.path)
    frame_count = 0
    while capture.isOpened():
        ret, frame = capture.read()
        if ret:
            # 读取坐标
            x_min = opt.left_top[0]
            x_max = opt.right_bottom[0]
            y_min = opt.left_top[1]
            y_max = opt.right_bottom[1]

            # 对图像进行深度复制
            copied = np.empty_like(frame)
            copied[:] = frame

            # 截取图像
            roi = copied[y_min:y_max, x_min:x_max, :]

            # 计算灰度平均值
            gray_means = get_avg_gray_value(roi)
            y_points.append(gray_means)
            x_points.append(frame_count)
            print(gray_means)

            # 兴趣区域可视化
            cv.rectangle(frame, opt.left_top, opt.right_bottom, opt.color, 3)
            frame = cv.resize(frame, (0, 0), fx=0.5, fy=0.5)
            cv.imshow("frame", frame)
            if cv.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break
        frame_count += 1

    # 回收视频资源
    capture.release()
    cv.destroyAllWindows()
    # 将结果保存至本地
    save2local(x_points, y_points, opt)
    # 折线图绘制
    print(Style.BRIGHT + "\n===========SHOW THE GRAPH============" + Style.RESET_ALL)
    print_info("Chart displayed", 0)
    plt.plot(x_points, y_points)
    plt.show()


if __name__ == '__main__':
    options = parse_opt()
    main(options)


