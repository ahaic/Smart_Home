import cv2,logging
from time import gmtime, strftime, time,sleep,strftime,configparser

interval = 30
frames=6000
logging.basicConfig(format='%(asctime)s %(message)s',
                    filename='/var/www/html/h5ai/timelapse/camera.log',
                    level=logging.WARNING)

#filepath = "/Users/Xiu/Desktop/timelapse/%s.jpg" % datetime.now.strftime("%Y-%m-%d-%H:%M:%S")
#filepath = "/home/pi/timelapse/%s.png" % strftime("%Y-%m-%d-%H:%M:%S")


def load_config():

# load configuration file and return the camer link
    config = configparser.ConfigParser()
    conf_file = "camera.conf"
    print("- Load config file")
    config.read(conf_file)


    return (config['Camera_1']['link'])



def connection():
    try:
        cap = cv2.VideoCapture(load_config())
        while (cv2.VideoCapture.isOpened(cap)):
            ret, image = cap.read()
            #del(cap)
            return ret,image
        else:
            logger.error('error connection....')
    except:
        logger.debug('exception error')


def capture():
    ret,image=connection()
    if (ret==True):
        cv2.imwrite("/var/www/html/h5ai/timelapse/%s.jpg" % strftime("%Y-%m-%d-%H:%M:%S"), image)
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
    for i in range(frames):
        capture()
        print('this is' ,i ,'@', strftime("%Y-%m-%d-%H:%M:%S"),'photos')
        sleep(interval)
