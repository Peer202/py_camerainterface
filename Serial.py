import serial
import time

class SerialConnection:
    def __init__(self):
        self.connected = False
        self.serialObject = serial.Serial(timeout=2)

    def connect(self,SerialDevice,Baudrate):
        self.connected = True
        self.serialObject.baudrate = Baudrate
        self.serialObject.port = SerialDevice
        try:
            self.serialObject.open()
        except:
            return False
        return  self.serialObject.isOpen()


    def disconnect(self):
        self.serialObject.close()
        self.connected = False

    def checkConnection(self):
        handshake = "TEST"
        self.sendData(handshake)
        time.sleep(1)
        return self.isConfirmed()
    
    def sendData(self,data):
        bdata = (data+"\n").encode("utf-8")
        self.serialObject.write(bdata)
        print("Tx: " + data + " len: " + str(len(bdata)))

    def isConfirmed(self):
        answer = self.readData()
        return (answer == "CHECK")

    def readData(self):
        data = self.serialObject.readline().decode("utf-8")[:-1]
        print("Rx: " + data)
        self.serialObject.reset_input_buffer()
        return data

    def sendValue(self,value):
        self.sendData("S:" + str(value))
        return self.isConfirmed()
    
    def getValue(self):
        self.sendData("G")
        answer = self.readData()
        if(answer == ""):
            return -1
        else:
            return int(answer)