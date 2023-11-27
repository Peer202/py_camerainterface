import gxipy as gx
import cv2
from nicegui import ui
import datetime
class CameraHandler:
    def __init__(self):
        global filename
        filename = "test.jpg"
        global saveNextImage
        saveNextImage = False
        self.frameRate = 136
        self.shutterspeed = 2000
        self.isconnected = False
        self.dosave = False
        self.shownFrames = 0
        self.Filename = "default"
        self.device_manager = gx.DeviceManager()
        dev_num, dev_info_list = self.device_manager.update_device_list()
        if dev_num == 0:
            print("Camera Device list empty")
        elif (self.isconnected == True):
            print("Tried to connect, but device already open")
        else:
            self.cam = self.device_manager.open_device_by_index(1)

            self.cam.data_stream[0].register_capture_callback(imageCallback)
            self.startCamera()
            print("Camera Connected")
            self.isconnected = True
            #self.onNewImage()

    def __enter__(self):
        return self

    def __exit__(self,*args):
        pass
        self.stopCamera()
        self.cam.close_device()

    def initGUI(self,parentElement):
        # adds the ui elements
        with parentElement:
            # The image / Camera Stuff
            ui.label(text="CameraControls")
            with ui.column():
                ui.label("Camera Settings")
                self.ui_settings_externalTrigger = ui.switch("Use external Trigger",on_change=lambda c: self.updateExtTrigger())
                self.ui_settings_time = ui.number(label="ExposureTime [ms]",value=2,on_change=lambda c: self.updateExposureTime())
                self.ui_settings_framerate = ui.number(label="Framerate [1/s]",value=20,on_change=lambda c: self.updateFrameRate())
            with ui.row():
                self.ui_settings_save_propname = ui.input(label="Propellername")
                self.ui_settings_save_rpm = ui.input(label="Trial RPM")
                self.ui_settings_save_suffix = ui.input(label="Remark")
                self.ui_settings_savebutton = ui.button(text="Save Image",on_click=lambda s: self.saveLatestImg())
        


    def startStopCamera(self):
        startstop = self.ui_settings_startstop.value
        if (startstop):
            self.startCamera()
        else:
            self.stopCamera()


    def startCamera(self):
        self.cam.AcquisitionStart.send_command()
        self.cam.ExposureTime.set(20000)
        self.cam.TriggerMode.set(gx.GxSwitchEntry.OFF)
        self.cam.AcquisitionFrameRate.set(20)
        self.cam.AcquisitionFrameRateMode.set(gx.GxSwitchEntry.ON)
        self.cam.stream_on()


    def stopCamera(self):
        self.cam.stream_off()
        self.cam.data_stream[0].unregister_capture_callback()

    def savenextimg(self,filename):
        self.saveimg = True
        self.filename = filename

    def updateExposureTime(self):
        self.cam.ExposureTime.set((self.ui_settings_time.value * 1000))

    def updateFrameRate(self):
        self.cam.AcquisitionFrameRate.set(self.ui_settings_framerate.value)
    
    def updateExtTrigger(self):
        if( self.ui_settings_externalTrigger.value):
            self.cam.TriggerMode.set(gx.GxSwitchEntry.ON)
            self.cam.TriggerSource.set(1)
        else:
            self.cam.TriggerMode.set(gx.GxSwitchEntry.OFF)
            self.cam.TriggerSource.set(0)

    def getlatestimg(self):
        img = self.cam.data_stream[0].get_image()
        return img

    def saveLatestImg(self):
        global saveNextImage
        saveNextImage = True
        #raw_image = self.cam.data_stream[0].get_image()
        #cv_image = raw_image.get_numpy_array()
        datestamp = datetime.datetime.now().strftime("%y-%m-%d-%H-%M-%S")
        global filename
        filename = self.ui_settings_save_propname.value + "_" + self.ui_settings_save_rpm.value + "rpm_" + self.ui_settings_save_suffix.value + "_" + datestamp + ".jpg"
        #cv2.imwrite(filename,cv_image) # saves the full resolution image
        ui.notify("Saving Img as " + filename)


def imageCallback(raw_image):
    global saveNextImage
    saveNextImage_local = saveNextImage
    saveNextImage = False
    cv_image = raw_image.get_numpy_array()
    #print(str(cv_image.shape))
    cv2.namedWindow("CameraFeed",cv2.WINDOW_NORMAL)
    previewImage = cv2.resize(cv_image,(768,480))
    cv2.imshow("CameraFeed",previewImage)
    cv2.waitKey(1)
    if(saveNextImage_local):
        print("Saving Image")
        cv2.imwrite(filename,cv_image)
        
