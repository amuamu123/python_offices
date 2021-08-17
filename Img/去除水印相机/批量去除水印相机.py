import cv2 as cv
import numpy as np
import os

def console_location(path):
    # 定片位置
    img = cv.imread(path)
    def on_mouse(event, x, y, flags, param):
        if event == cv.EVENT_LBUTTONDOWN:
            print(x, y)
    # 构建窗口
    # 回调绑定窗口
    cv.namedWindow("img", cv.WINDOW_NORMAL)
    cv.setMouseCallback("img", on_mouse, 0)
    cv.imshow("img", img)
    # 键盘输入 q退出
    if cv.waitKey() == ord("q"):
        cv.destroyAllWindows()

class WaterMark(object):
    def mark(self, path):
        global img
        # 提取感兴趣区域ROI
        img = cv.imread(path)
        # 通过运行console_location函数后在相应的图片上点击两个点可以获取一下两个参数
        # 高1:高2 宽1:宽2
        roi = img[2300:3890, 0:2962]
        # cv.imwrite('02.jpg', roi)
        roi_hsv = cv.cvtColor(roi, cv.COLOR_BGR2HSV)
        # cv.imwrite('hsv.jpg', roi_hsv)
        # 设定白色HSV范围
        lower = np.array([0, 0, 255])
        upper = np.array([255, 255, 255])
        # 创建水印蒙层
        kernel = np.ones((3, 3), np.uint8)
        # cv.imwrite('kernel.jpg',kernel)
        mask = cv.inRange(roi_hsv, lower, upper)
        # cv.imwrite(r'mask.jpg',mask)
        # 对水印蒙层进行膨胀操作
        dilate = cv.dilate(mask, kernel, iterations=3)
        res = cv.inpaint(roi, dilate, 7, flags=cv.INPAINT_TELEA)
        # 双边滤波
        res = cv.bilateralFilter(res, 5, 280, 50)
        # 高1:高2 宽1:宽2
        img[2300:3890, 0:2962] = res
        cv.imwrite('modified'+ str() +'.jpg', img)
        
if __name__ == '__main__':
    文件夹路径 = '文件的副本/'
    a  = 0
    for  i  in os.listdir(文件夹路径) :
        文件路径  = 文件夹路径  + i
        w = WaterMark()
        w.mark(文件路径)
        cv.imwrite('modified'+ str(a) +'.jpg', img)
        a = a+1