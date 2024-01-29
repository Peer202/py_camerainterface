from nicegui import ui
import gxipy as gx
from PIL import Image
from Serial import SerialConnection
from Camera import CameraHandler
import cv2
trigger_connection = SerialConnection()
global calculated_increments
calculated_increments = 500
camera = CameraHandler()

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
    #value = int(increment_Input_raw.value)
    #ui.notify("Setting Increment Value: " + str(value))
    value = calculated_increments
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

def calculateIncrements():
    n_fullRot = increment_Input_fullRotIncrements.value
    n_div = increment_Input_nFlash.value
    n_dropped = increment_Input_droppedIncrements.value
    global calculated_increments
    calculated_increments = round((n_fullRot - n_dropped) / n_div)
    increment_output_calculcatedinterval.set_text("Calculated Incrementvalue: " + str(calculated_increments))
    #sendValue(calculated_increments)

def skipIncrements(value=0):
    if(value == 0):
        value = skip_input_increments.value
    trigger_connection.sendSkipValue(value=value)
    

with ui.row():
    with ui.column():
        with ui.card():
            # Communication Settings
            ui.label("Connection Settings")
            connect_Input_Device = ui.input(label="Serial Device Name",value="COM4")
            connect_Input_Baud = ui.number(label="BaudRate",value=115200)
            connect_button = ui.button(text='Connect to Device', on_click=lambda e: toggleConnect())
            connect_testbutton = ui.button(text="Test Connection", on_click=lambda e: checkConnection())
            connect_testbutton.set_visibility(False)

        with ui.card():
            # Increment Settings
            ui.label("Trigger Settings")
            increment_Input_fullRotIncrements = ui.number(label="Number of Increments per Rot",value = 2000, on_change=lambda e: calculateIncrements())
            increment_Input_nFlash = ui.number("Number of equally spaced trigger intervals per Rot",value = 4,min=1,on_change=lambda e: calculateIncrements())
            #increment_Input_Angle = ui.number(label="Trigger Angle",value=180,on_change=lambda c: convertAngletoIncrement())
            #increment_Input_raw = ui.number(label="Increments",value= 500)#,on_change=lambda c: convertIncrementtoAngle()
            #ui.circular_progress(min=0,max=360).bind_value_from(increment_Input_Angle, 'value')
            increment_Input_droppedIncrements = ui.number(label="Dropped Increments",value = 0,min=0,on_change=lambda e: calculateIncrements())
            increment_output_calculcatedinterval = ui.label("Calculated Incrementvalue: " + str(calculated_increments))
            ui.button(text="Send Current Value",on_click=lambda c: sendValue())
            ui.button(text="Read Current Value",on_click=lambda c: readValue())
        
            with ui.card():
                ui.label("Skipping Increments")
                skip_input_increments = ui.number(label="Number of Intervals to skip",value=10)
                skip_button_small = ui.button(text="Skip Intervals",on_click=lambda e:skipIncrements())
                skip_button_large = ui.button(text="Skip 100 Increments",on_click=lambda e:skipIncrements(100))
            

        cameracard = ui.card()
        camera.initGUI(cameracard)

    #ui.timer(interval=0.1, callback=lambda: camera.onNewImage())
             
    ui.run(reload=False)
