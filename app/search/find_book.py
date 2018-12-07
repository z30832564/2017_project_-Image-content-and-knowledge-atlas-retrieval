# -*-coding: utf-8-*-

import cv2
import numpy as np
import math
import matplotlib.pyplot as plt


def stretch(img):
    max = float(img.max())
    min = float(img.min())

    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            img[i, j] = (255 / (max - min)) * img[i, j] - (255 * min) / (max - min)

    return img


def dobinaryzation(img):
    max = float(img.max())
    min = float(img.min())

    x = max - ((max - min) / 2)
    ret, threshedimg = cv2.threshold(img, 50, 255, cv2.THRESH_BINARY)

    return threshedimg


def find_retangle(contour):
    y, x = [], []

    for p in contour:
        y.append(p[0][0])
        x.append(p[0][1])

    return [min(y), min(x), max(y), max(x)]


def locate_license(img, orgimg):
    img, contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cc = contours[0]
    for i in range(1, len(contours)):
        cc = np.concatenate((cc, contours[i]), axis=0)
    # 找出最大的三个区域
    blocks = []

    # 找出轮廓的左上点和右下点，由此计算它的面积和长宽比
    r = find_retangle(cc)
    a = (r[2] - r[0]) * (r[3] - r[1])
    s = (r[2] - r[0]) // (r[3] - r[1])

    blocks.append([r, a, s])

    # 选出面积最大的3个区域
    blocks = sorted(blocks, key=lambda b: b[2])[-3:]

    return blocks[-1][0]


def sobel_image(image):
    grad_x = cv2.Sobel(image, cv2.CV_32F, 1, 0) #x方向导数
    grad_y = cv2.Sobel(image, cv2.CV_32F, 0, 1) #y方向导数
    gradx = cv2.convertScaleAbs(grad_x)
    grady = cv2.convertScaleAbs(grad_y)
    gradxy = cv2.addWeighted(gradx, 0.5, grady, 0.5, 0)
    return gradxy



def find_license(img):
    '''预处理'''
    # 压缩图像
    img = cv2.resize(img, (400, 400 * img.shape[0] // img.shape[1]))

    # RGB转灰色
    grayimg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 灰度拉伸
    stretchedimg = stretch(grayimg)

    # 进行开运算，用来去噪声
    r = 16
    h = w = r * 2 + 1
    kernel = np.zeros((h, w), dtype=np.uint8)
    cv2.circle(kernel, (r, r), r, 1, -1)

    openingimg = cv2.morphologyEx(stretchedimg, cv2.MORPH_OPEN, kernel)
    strtimg = cv2.absdiff(stretchedimg, openingimg)

    solbelimg = sobel_image(strtimg)

    Laplacianimg = cv2.Laplacian(strtimg, cv2.CV_16S,ksize = 3)

    # 图像二值化
    binaryimg = dobinaryzation(solbelimg)

    # 使用Canny函数做边缘检测
    cannyimg = cv2.Canny(binaryimg, binaryimg.shape[0], binaryimg.shape[1])

    # kernel = np.ones((5, 5), np.uint8)
    # cannyimg = cv2.dilate(cannyimg, kernel, iterations=1)
    # cannyimg = cv2.erode(cannyimg, kernel, iterations=1)

    ''' 消除小区域，保留大块区域，从而定位车牌'''
    # 进行闭运算
    kernel = np.ones((5, 19), np.uint8)
    closingimg = cv2.morphologyEx(cannyimg, cv2.MORPH_CLOSE, kernel)

    # 进行开运算
    kernel = np.ones((11, 5), np.uint8)
    openingimg = cv2.morphologyEx(closingimg, cv2.MORPH_OPEN, kernel)
    #
    # 再次进行开运算
    #


    # 消除小区域，定位车牌位置
    rect = locate_license(openingimg, img)

    return np.array(rect), img


def find_book_edge(img):
    # 读取图片
    rect, img = find_license(img)

    # 框出车牌
    cv2.rectangle(img, (rect[0], rect[1]), (rect[2], rect[3]), (0, 255, 0), 2)
    cv2.imwrite('book.png',img)
    print(img.shape)
    re_img = img[rect[1]+10:rect[3]-10, rect[0]+10:rect[2]-10, :]



    cv2.imwrite('boo.png',re_img)
    re_img = cv2.Canny(re_img, re_img.shape[0], re_img.shape[1])
    re_img = cv2.cvtColor(re_img, cv2.COLOR_GRAY2BGR)
    re_img = cv2.Canny(re_img, re_img.shape[0], re_img.shape[1])

    return re_img