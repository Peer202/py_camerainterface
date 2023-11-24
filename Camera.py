import gxipy as gx
from nicegui import ui

class CameraHandler:
    def __init__(self,imageuielement):
        self.saveimg = False
        self.filename = "Default"
        self.frameRate = 136
        self.shutterspeed = 2000
        self.imageuielement = imageuielement

        device_manager = gx.DeviceManager()
        dev_num, dev_info_list = device_manager.update_device_list()
        if dev_num == 0:
            ui.notify("Camera Device list empty")
        else:
            self.cam = device_manager.open_device_by_index(1)
            self.cam.data_stream[0].register_capture_callback(self.imgCallback)
            
        
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
        self.cam.AcquisitionFrameRate = self.frameRate


    def imgCallback(self,rawimage):
        if rawimage.get_status() == gx.GxFrameStatusList.INCOMPLETE:
            print("incomplete frame")
        else:
            self.imageuielement.set_source(rawimage)