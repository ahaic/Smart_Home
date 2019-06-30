# works on python 3.6 Mac


import cv2,logging
from time import gmtime, strftime, time,sleep,strftime
import configparser
import os


logging.basicConfig(format='%(asctime)s %(message)s',
                        filename=os.getcwd()+'camera.log',
                        level=logging.WARNING)
logger = logging.getLogger(__name__)



def load_config():

# load configuration file and return the camer link
    config = configparser.ConfigParser()
    conf_file = "camera.conf"
    print("- Load config file")
    config.read(conf_file)
    interval = config['settings']['interval']
    frames = config['settings']['frames']
    link = config['Camera_2']['link']
    dir = config['settings']['dir']
    if bool(dir):
        return interval,frames,link,dir
    else:
        dir = os.getcwd()
        return interval,frames,link,dir


    #print(interval,frames,link,dir)

def connection(link):
    try:
        #interval,frames,link=load_config()

        cap = cv2.VideoCapture(link)
#        print(cap.isOpened())

        while (cv2.VideoCapture.isOpened(cap)):
            #print("camera connection establised")

            ret, image = cap.read()
            #del(cap)
            return ret,image
        else:
            logger.error('error connection....')
    except:
        logger.debug('exception error')


def capture(link,dir):
    ret,image=connection(link)
    if (ret==True):
        cv2.imwrite(os.path.join(dir,strftime("%Y-%m-%d %H-%M-%S")+'.jpg'), image)
    else:
        #print('release camera and capture again')
        logger.debug('release camera and capture again')

def timelapse_video():
    pass


def photo_upload():
    pass


def face_recognition():
    pass



if __name__ == '__main__':
    print('initializing.....')
    interval,frames,link,dir=load_config()
    print('reading camera from ',link)
    print('save files in ',dir)

    for i in range(int(frames)):
        capture(link,dir)
        print('this is' ,i ,'@', strftime("%Y-%m-%d-%H:%M:%S"),'photos')
        sleep(int(interval))
