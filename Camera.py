import gxipy as gx
from nicegui import ui

class CameraHandler:
    def __init__(self):
        self.saveimg = False
        self.filename = "Default"
        self.frameRate = 136
        self.shutterspeed = 2000
        self.isconnected = False
        self.device_manager = gx.DeviceManager()
        dev_num, dev_info_list = self.device_manager.update_device_list()
        if dev_num == 0:
            print("Camera Device list empty")
        elif (self.isconnected == True):
            print("Tried to connect, but device already open")
        else:
            self.cam = self.device_manager.open_device_by_index(1)
            #self.cam.data_stream[0].register_capture_callback(imgCallback)
            self.cam.stream_on()
            print("Camera Connected")
            self.isconnected = True
    
    def __enter__(self):
        return self

    def __exit__(self,*args):
        self.stopCamera()
        self.cam.close_device()

    def startCamera(self):
        self.cam.stream_on()

    def stopCamera(self):
        self.cam.stream_off()

    def savenextimg(self,filename):
        self.saveimg = True
        self.filename = filename

    def updateParameters(self,shutterSpeed,frameRate):
        self.shutterspeed = shutterSpeed * 1000
        self.frameRate = frameRate
        self.cam.AcquisitionFrameRate.set(self.frameRate)
        self.cam.ExposureTime.set(self.shutterspeed)

    def getlatestimg(self):
        img = self.cam.data_stream[0].get_image()
        return img
