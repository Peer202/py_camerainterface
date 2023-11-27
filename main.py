from nicegui import ui
import gxipy as gx
from PIL import Image
from Serial import SerialConnection
from Camera import CameraHandler
import cv2
trigger_connection = SerialConnection()
#camera = CameraHandler()
with CameraHandler() as camera:
    def toggleConnect():
        connectionState = trigger_connection.serialObject.isOpen()
        if(connectionState):
            ui.notify("Disconnected")
            trigger_connection.disconnect()
        else:
            devicename = connect_Input_Device.value
            baudrate = connect_Input_Baud.value
            ui.notify("Connecting to Device: " + str(devicename) + " with Baudrate:" + str(baudrate))
            success = trigger_connection.connect(devicename,baudrate)
            if(success):
                ui.notify("Is Connected")
                connect_button.set_text("Disconnect")
            else:
                ui.notify("Connection Failed")
        connect_Input_Baud.set_visibility((not trigger_connection.serialObject.isOpen()))
        connect_Input_Device.set_visibility((not trigger_connection.serialObject.isOpen()))
        connect_testbutton.set_visibility(trigger_connection.serialObject.isOpen())

    def sendValue():
        value = int(increment_Input_raw.value)
        ui.notify("Setting Increment Value: " + str(value))
        success = trigger_connection.sendValue(value)
        if(success):
            ui.notify("Value Set!")
        else:
            ui.notify("Transfer Error")

    def readValue():
        cvalue = trigger_connection.getValue()
        if(cvalue == -1):
            ui.notify("Communication Error")
        else:
            ui.notify("Current Increment Value: " + str(cvalue))
        
    def checkConnection():
        success = trigger_connection.checkConnection()
        if(success):
            ui.notify("Test successfull")
        else:
            ui.notify("Test failed")


    def convertAngletoIncrement():
        angle = increment_Input_Angle.value
        increment_Input_raw.set_value(int((angle * (1000/360))))

    def convertIncrementtoAngle():
        increment = increment_Input_raw.value
        increment_Input_Angle.set_value(int((increment * (360/1000))))


    with ui.row():
        with ui.column():
            with ui.card():
                # Communication Settings
                ui.label("Connection Settings")
                connect_Input_Device = ui.input(label="Serial Device Name",value="/dev/ttyACM3")
                connect_Input_Baud = ui.number(label="BaudRate",value=115200)
                connect_button = ui.button(text='Connect to Device', on_click=lambda e: toggleConnect())
                connect_testbutton = ui.button(text="Test Connection", on_click=lambda e: checkConnection())
                connect_testbutton.set_visibility(False)

            with ui.card():
                # Increment Settings
                ui.label("Increment Settings")
                increment_Input_Angle = ui.number(label="Trigger Angle",value=180,on_change=lambda c: convertAngletoIncrement())
                increment_Input_raw = ui.number(label="Increments",value= 500)#,on_change=lambda c: convertIncrementtoAngle()
                ui.circular_progress(min=0,max=360).bind_value_from(increment_Input_Angle, 'value')
                ui.button(text="Send to Device!",on_click=lambda c: sendValue())
                ui.button(text="Read Current Value",on_click=lambda c: readValue())

        cameracard = ui.card()
        camera.initGUI(cameracard)

    #ui.timer(interval=0.1, callback=lambda: camera.onNewImage())
             
    ui.run(reload=False)
