import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np


class Config:
    IS_VIDEO = True
    FILE_PATH = r"C:\Users\zhiyuan\Videos\test.mp4"
    LEFT_TOP = [200, 200]
    RIGHT_BOTTOM = [300, 400]
    BORDER_COLOR = (0, 0, 255)

    def __init__(self):
        cap = cv.VideoCapture(self.FILE_PATH)
        self.FRAME_WIDTH = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
        self.FRAME_HEIGHT = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))


def draw_graph():
    pass


def get_avg_gray_value(img):
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    means, dev = cv.meanStdDev(gray)
    return means[0, 0]


if __name__ == '__main__':
    myconfig = Config()
    # 待绘制点集
    x_points = []
    y_points = []
    # 若为图像处理模式
    if myconfig.IS_VIDEO:
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
                cv.imshow("frame", frame)
                if cv.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                break
            frame_count += 1
        plt.plot(x_points, y_points)
        plt.show()
        # 回收资源
        capture.release()
        cv.destroyAllWindows()


