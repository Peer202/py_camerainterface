import gxipy as gx
import cv2
from nicegui import ui
import datetime
class CameraHandler:
    def __init__(self):
        self.saveimg = False
        self.filename = "Default"
        self.frameRate = 136
        self.shutterspeed = 2000
        self.isconnected = False
        self.dosave = False
        self.Filename = "default"
        self.device_manager = gx.DeviceManager()
        dev_num, dev_info_list = self.device_manager.update_device_list()
        if dev_num == 0:
            print("Camera Device list empty")
        elif (self.isconnected == True):
            print("Tried to connect, but device already open")
        else:
            self.cam = self.device_manager.open_device_by_index(1)
            self.cam.data_stream[0].register_capture_callback(self.onNewImage)
            self.cam.stream_on()
            print("Camera Connected")
            self.isconnected = True

    def __enter__(self):
        return self

    def __exit__(self,*args):
        self.stopCamera()
        self.cam.close_device()

    def initGUI(self,parentElement):
        # adds the ui elements
        with parentElement:
            # The image / Camera Stuff
            ui.label(text="CameraControls")
            with ui.column():
                ui.label("Camera Settings")
                self.ui_settings_startstop = ui.switch("Start Acquisition",value=True,on_change=lambda c: self.startStopCamera())
                self.ui_settings_externalTrigger = ui.switch("Use external Trigger")
                self.ui_settings_time = ui.number(label="ExposureTime [ms]",value=2,on_change=lambda c: self.updateExposureTime())
                self.ui_settings_framerate = ui.number(label="Framerate [1/s]",value=20,on_change=lambda c: self.updateFrameRate())
            with ui.row():
                self.ui_settings_save_propname = ui.input(label="Propellername")
                self.ui_settings_save_rpm = ui.input(label="Trial RPM")
                self.ui_settings_save_suffix = ui.input(label="Remark")
                self.ui_settings_savebutton = ui.button(text="Save Image",on_click=lambda s: self.saveLatestImg())
    def onNewImage(self,raw_image):
        # handles the callback when a new image is available
        # converts the image to opencv / numpy format
        if raw_image.get_status() == gx.GxFrameStatusList.INCOMPLETE:
            print("incomplete frame, wont process")
        else:
            cv_image = raw_image.get_numpy_array()
            cv2.namedWindow("CameraFeed",cv2.WINDOW_NORMAL)
            previewImage = cv2.resize(cv_image,(768,480))
            cv2.imshow("CameraFeed",previewImage)
            if(self.dosave):
                # saves the Frame to Disk
                self.dosave = False # clear Flag
                datestamp = datetime.datetime.now().strftime("%y-%m-%d-%H:%M")
                filename = self.Filename + "-" + datestamp + ".png"
                cv2.imwrite(filename,cv_image) # saves the full resolution image

    def startStopCamera(self):
        startstop = self.ui_settings_startstop.value
        if (startstop):
            self.startCamera()
        else:
            self.stopCamera()


    def startCamera(self):
        self.cam.stream_on()

    def stopCamera(self):
        self.cam.stream_off()

    def savenextimg(self,filename):
        self.saveimg = True
        self.filename = filename

    def updateExposureTime(self):
        self.cam.ExposureTime.set((self.ui_settings_time.value * 1000))

    def updateFrameRate(self):
        self.cam.AcquisitionFrameRate.set(self.ui_settings_framerate.value)

    def getlatestimg(self):
        img = self.cam.data_stream[0].get_image()
        return img

    def saveLatestImg(self):
        self.Filename = self.ui_settings_save_propname.value + "_" + self.ui_settings_save_rpm.value + "rpm_" + self.ui_settings_save_suffix.value
        ui.notify("Saving Img as " + self.Filename)
        self.dosave = True