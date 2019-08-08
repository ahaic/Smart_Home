# works on python 3.6 Mac
#!/usr/bin/python
# -*- coding: UTF-8 -*-
# latest update : 8 Aug 2019  14:22
__author__ = "ahaic"

import cv2,logging
from time import gmtime, strftime, time,sleep,strftime
import configparser
import os

logging.basicConfig(format='%(asctime)s %(message)s',
                        filename='camera.log',
                        level=logging.WARNING)
logger = logging.getLogger(__name__)


class camera():
    def __init__(self,id):
    # load configuration file and return the camer link
    # id = camera id
        config = configparser.ConfigParser()
        conf_file = "camera.conf"
        print("- Load config file")
        config.read(conf_file,encoding='utf-8')
        interval = config['settings']['interval']
        frames = config['settings']['frames']
        link = config['Camera_0']['link']
        dir = config['settings']['dir']

        self.interval = interval
        self.frames = frames
        self.link = link
        self.dir = dir
        self.id=id

    def connection(self):
        try:
            #interval,frames,link=load_config()
            #print(self.link)
            cap = cv2.VideoCapture(self.link)
    #       print(cap.isOpened())
            while (cv2.VideoCapture.isOpened(cap)):
                #print("camera connection establised")

                ret, image = cap.read()
                #del(cap)
                return ret,image
            else:
                logger.error('error connection....')
        except:
            logger.debug('exception error')


    def capture(self):
        ret,image=self.connection()
        if (ret==True):
            cv2.imwrite(os.path.join(self.dir,strftime("%Y-%m-%d %H-%M-%S")+'.jpg'), image)
        else:
            #print('release camera and capture again')
            logger.debug('release camera and capture again')


    def timeplapse(self):
        save_path = '/Users/Xiu/Desktop/timelapse.mp4'
        frames_per_seconds = 24.0

        fourcc = cv2.VideoWriter_fourcc('M','J','P','G')

        out = cv2.VideoWriter(save_path, fourcc, frames_per_seconds, (1280,720))
        timelapse_img_dir = "/Users/Xiu/github/smart_camera/photos"


    def motion(self):

        pre_frame = None

        while (cv2.VideoCapture.isOpened(cap)):

            start = time.time()
            # 读取视频流
            ret=None
            frame=None
            while ret is None:
                try:
                    ret,frame = cap.read()
                except Exception as e:
                    print(e)

            # 转灰度图
            gray_lwpCV = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


            end = time.time()

            #cv2.imshow("capture", frame)

            # 运动检测部分
            seconds = end - start
            if seconds < 1.0 / fps:
                time.sleep(1.0 / fps - seconds)

            gray_lwpCV = cv2.resize(gray_lwpCV, (500, 500))
            # 用高斯滤波进行模糊处理
            gray_lwpCV = cv2.GaussianBlur(gray_lwpCV, (21, 21), 0)

            # 如果没有背景图像就将当前帧当作背景图片
            if pre_frame is None:
                pre_frame = gray_lwpCV
            else:
                # absdiff把两幅图的差的绝对值输出到另一幅图上面来
                img_delta = cv2.absdiff(pre_frame, gray_lwpCV)
                #threshold阈值函数(原图像应该是灰度图,对像素值进行分类的阈值,当像素值高于（有时是小于）阈值时应该被赋予的新的像素值,阈值方法)
                thresh = cv2.threshold(img_delta, 25, 255, cv2.THRESH_BINARY)[1]
                # 膨胀图像
                thresh = cv2.dilate(thresh, None, iterations=2)
                # findContours检测物体轮廓(寻找轮廓的图像,轮廓的检索模式,轮廓的近似办法)
                contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                for c in contours:
                    # 设置敏感度
                    # contourArea计算轮廓面积
                    if cv2.contourArea(c) < 1000:
                        continue
                    else:
                        print("Motion Detected",time.strftime("%Y-%m-%d %H-%M-%S"))
                        break
                pre_frame = gray_lwpCV


if __name__ == '__main__':
    print('initializing.....')
    x= camera(2)
    print('reading camera position from ',x.id)
    print('save files in ',x.dir)

    for i in range(int(x.frames)):
        x.capture()
        print('this is' ,i ,'@', strftime("%Y-%m-%d-%H:%M:%S"),'photos')
        sleep(int(x.interval))
