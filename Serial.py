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
        success = self.checkConnection()
        if(success):
            return True
        else:
            return False


    def disconnect(self):
        self.serialObject.close()
        self.connected = False

    def checkConnection(self):
        handshake = "TEST"
        self.sendData(handshake)
        time.sleep(0.1)
        return self.isConfirmed()
    
    def sendData(self,data):
        bdata = (data+"\n").encode("utf-8")
        self.serialObject.write(bdata)
        print("Tx: " + data + " len: " + str(len(bdata)))

    def isConfirmed(self):
        answer = self.readData()
        if(answer == "CHECK"):
            print("Command confirmed")
            return True
        elif(answer == "NOCOM"):
            print("Command not recognized by Board")
            return False
        else:
            print("Command not recognized by Board")
            return False
            

        return (answer == "CHECK")

    def readData(self):
        data = self.serialObject.readline().decode("utf-8")[:-1]
        print("Rx: " + data)
        self.serialObject.reset_input_buffer()
        return data

    def sendValue(self,value):
        self.sendData("S:" + str(value))
        return self.isConfirmed()
    
    def sendSkipValue(self,value):
        self.sendData("T:" + str(value))
        return self.isConfirmed()
    
    def getValue(self):
        self.sendData("G")
        answer = self.readData()
        if(answer == ""):
            return -1
        else:
            return int(answer)