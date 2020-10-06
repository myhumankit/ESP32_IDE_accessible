from Packages import wx, speech, time, json, asyncio

#TODO établir liste baudrate/sleep

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

def GetCmdReturn(shell_text, cmd):
    """Return the result of a command launched in MicroPython

    :param shell_text: The text catched on the shell panel
    :type shell_text: str
    :param cmd: The cmd return asked
    :type cmd: str
    :return: the return of the command searched
    :rtype: str
    """
    try:
        return_cmd = shell_text.split(cmd, 1)[1]
        return_cmd = return_cmd[:-4]
    except Exception:
        print ("ERROR: |" + shell_text +  "|")
        return "err"
    print ("SUCCESS:" + return_cmd)
    return return_cmd

async def SetView(frame, info):
    frame.show_cmd = info


#TODO: reconstruire l'algo GetFileTree via upycraft
#! Objectif: obtenir le res en json correctement
def getFileTree(frame, dir):
        print("GET FILE TREE : %s"%(dir))
        frame.cmd_return = ""
        frame.get_cmd = True
        asyncio.run(SendCmdAsync(frame, "os.listdir(\'%s\')\r\n"%dir))
        result = frame.ReadCmd("os.listdir(\'%s\')"%dir)
        print("RETURN: " + result)
        if result=="err":
            return result
        print("ON Y EST")
        #if gestion erreur
        filemsg=result[result.find("["):result.find("]")+1]
        print("FILEMSG = " + filemsg)

        ret=json.loads("{}")
        ret[dir]=[]
        if filemsg=="[]":
            return ret
        filelist=[]
        filemsg=filemsg.split("'")
        
        for i in filemsg:
            if i.find("[")>=0 or i.find(",")>=0 or i.find("]")>=0:
                pass
            else:
                filelist.append(i)
        print("FILE LIST =" ,filelist)
        for i in filelist:
            asyncio.run(SendCmdAsync(frame, "os.stat(\'%s\')\r\n"%(dir + "/" + i)))
            res = frame.ReadCmd("os.stat(\'%s\')"%(dir + "/" + i))
            if res == "err":
                return res
            isdir=res.split("\n")[1]
            isdir=isdir.split(", ")
            print("ISDIR = ", isdir)
            try:
                adir = isdir[0]
                if adir.find("(")>=0:
                    adir = adir[1:]
                if adir.find(")")>=0:
                    adir = adir[:-1]
                print("ADIR = ", adir)
                if int(adir)==0o040000:
                    if i=="System Volume Information":
                        pass
                    else:
                        ret[dir].append(getFileTree(frame, dir+"/"+i))
                else:
                    ret[dir].append(i)
            except Exception as e:
                print("ERROr: " + e)
                return "err"
        return ret
    
def treeModel(frame):
        frame.reflushTreeBool=True
        frame.cmd_return =""

        res=json.loads("{}")

        
        res=getFileTree(frame, ".")
        if res=="err":
            frame.reflushTreeBool=False
            frame.cmd_return = ""
            return
        print("RESSSSSSS")
        print(res)
        reflushTree(frame,res)
        frame.cmd_return =""
        frame.reflushTreeBool=False

def reflushTree(frame,data):
    if data=="err":
        print("soucii")
        return
    print("reflushTree=====================%s"%data)

    createReflushTree(frame,frame.device_tree.root,data['.'])
    
def createReflushTree(frame, root, msg):
        print("MSG " + str(msg))
        tree = frame.device_tree
        time.sleep(1)
        if type(msg) is str:
            child = tree.AppendItem(root, msg)
            tree.SetItemImage(child, tree.fldridx, wx.TreeItemIcon_Normal)
            tree.SetItemImage(child, tree.fldropenidx, wx.TreeItemIcon_Expanded)
            #root.RemoveItem(itemDevice.Item())
            
        elif type(msg) is dict:
            for i in msg:
                k=eval("%s"%msg[i])
                i=i.split("/")
                print("KKKK = ", k, "I = ", i)
                child = tree.AppendItem(root, i[1])
                tree.SetItemImage(child, tree.fldridx, wx.TreeItemIcon_Normal)
                tree.SetItemImage(child, tree.fldropenidx, wx.TreeItemIcon_Expanded)
                createReflushTree(frame, child, k)
        elif type(msg) is list:#liste de fichiers
            for i in msg:
                if type(i) is str:
                    createReflushTree(frame, root, i)
                elif type(i) is dict:
                    createReflushTree(frame, root, i)           
                else:
                    pass
    
async def SendCmdAsync(parent, cmd):
    parent.cmd_return = ""
    print("CMDsend = " +cmd)
    parent.serial_manager.put_cmd(cmd)
    await asyncio.sleep(1)
    #return 