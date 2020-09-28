from Packages import wx, speech, time
def load_img(path):
    return wx.Image(path,wx.BITMAP_TYPE_ANY).ConvertToBitmap()

def speak(frame, txt):
    if frame.voice_on:
        speech.say(txt)

def ConnectSerial(self):
        self.Shell.Clear()
        self.serial.write('\x03'.encode())

        startdata=""
        startTime=time.time()
        while True:
            n = self.serial.inWaiting()
            if n>0:
                startdata += (self.serial.read(n)).decode(encoding='utf-8',errors='ignore')
                print("[%s]"%startdata)
                if startdata.find('>>> '):
                    print("OK")
                    break
            time.sleep(0.1)
            endTime=time.time()
            if endTime-startTime > 10:
                self.serial.close()
                if not self.serial.isOpen():
                    print("UPDATE FIRMWARE")
                return False
        senddata="import sys\r"
        for i in senddata:
            self.serial.write(i.encode())
        startdata=""
        startTime=time.time()
        while True:
            n = self.serial.inWaiting()
            if n>0:
                startdata+=(self.serial.read(n)).decode('utf-8')
                if startdata.find('>>> ')>=0:
                    self.Shell.AppendText(">>> ")
                    break
            time.sleep(0.1)
            endTime=time.time()
            if endTime-startTime>2:
                self.serial.close()
                self.Shell.AppendText("connect serial timeout")
                return False

        senddata="sys.platform\r"
        for i in senddata:
            self.serial.write(i.encode())
        startdata=""
        startTime=time.time()
        while True:
            n = self.serial.inWaiting()
            if n>0:
                startdata+=(self.serial.read(n)).decode('utf-8')
                if startdata.find('>>> ')>=0:
                    break
            time.sleep(0.1)
            endTime=time.time()
            if endTime-startTime>2:
                self.serial.close()
                self.Shell.AppendText("connect serial timeout")
                return False
            
        self.StartThread()
        return True
        