import os.path
import argparse
import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np


class Config:
    FILE_PATH = r"./simples/10Hz.mp4"    # 待处理视频路径
    SAVE_RESULT = True                   # 是否保存结果至本地txt文件
    LEFT_TOP = [500, 600]                # 采样区域左上角坐标
    RIGHT_BOTTOM = [800, 900]            # 采样区域右下角坐标
    BORDER_COLOR = [0, 0, 255]           # 边框颜色(BGR)


def parse_opt():
    parser = argparse.ArgumentParser()


def get_avg_gray_value(img):
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    means, dev = cv.meanStdDev(gray)
    return means[0, 0]


def save2local(x_pts, y_pts, cfg: Config):
    # 生成保存路径
    file_name = os.path.splitext(os.path.split(cfg.FILE_PATH)[-1])[0]
    save_path = os.path.join('./', file_name+'_result.txt')
    # 判断结果文件是否存在
    # 若文件存在提示是否进行覆写操作
    try:
        if os.path.isfile(save_path):
            if not input("The result file already exists, do you want to overwrite it?(press y to confirm) ") is 'y':
                print('Results not saved!')
                return
    except FileNotFoundError:
        pass

    # 将灰度值结果保存至本地
    with open(save_path, 'w') as f:
        for i in range(len(x_pts)):
            f.write(str(y_pts[i])+'\n')
        print("Result saved!")


def main():
    # 实例化配置类
    myconfig = Config()
    # 待绘制点集
    x_points = []
    y_points = []

    capture = cv.VideoCapture(myconfig.FILE_PATH)
    frame_count = 0
    while capture.isOpened():
        ret, frame = capture.read()
        if ret:
            # 读取坐标
            x_min = myconfig.LEFT_TOP[0]
            x_max = myconfig.RIGHT_BOTTOM[0]
            y_min = myconfig.LEFT_TOP[1]
            y_max = myconfig.RIGHT_BOTTOM[1]

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
            cv.rectangle(frame, myconfig.LEFT_TOP, myconfig.RIGHT_BOTTOM, myconfig.BORDER_COLOR, 3)
            frame = cv.resize(frame, (0, 0), fx=0.5, fy=0.5)
            cv.imshow("frame", frame)
            if cv.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break
        frame_count += 1

    # 将结果保存至本地
    save2local(x_points, y_points, myconfig)
    # 折线图绘制
    plt.plot(x_points, y_points)
    plt.show()
    # 回收资源
    capture.release()
    cv.destroyAllWindows()


if __name__ == '__main__':
    main()


