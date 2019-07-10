# works on python 3.6 Mac
#!/usr/bin/python
# -*- coding: UTF-8 -*-
# latest update : 10 July 2019  22:31

import cv2,logging
from time import gmtime, strftime, time,sleep,strftime
import configparser
import os

logging.basicConfig(format='%(asctime)s %(message)s',
                        filename=os.getcwd()+'camera.log',
                        level=logging.WARNING)
logger = logging.getLogger(__name__)


class camera():
    def __init__(self,id):
    # load configuration file and return the camer link
    # id = camera id
        config = configparser.ConfigParser()
        conf_file = "camera.conf"
        print("- Load config file")
        config.read(conf_file)
        interval = config['settings']['interval']
        frames = config['settings']['frames']
        link = config['Camera_2']['link']
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


if __name__ == '__main__':
    print('initializing.....')
    x= camera(2) 
    print('reading camera position from ',x.id)
    print('save files in ',x.dir)

    for i in range(int(x.frames)):
        x.capture()
        print('this is' ,i ,'@', strftime("%Y-%m-%d-%H:%M:%S"),'photos')
        sleep(int(x.interval))
