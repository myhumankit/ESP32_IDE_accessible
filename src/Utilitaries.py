from packages import wx, speech, time, json, asyncio, sys
from my_serial import SendCmdAsync, put_cmd

def save_on_card(main_window, page):
    print(page.directory)
    print(page.filename)
    notebookP = main_window.notebook

    # Check if save is required
    if (page.GetValue() != page.last_save):
        page.saved = False
        # Grab the content to be saved
        save_as_file_content = page.GetValue()
        print("|+|",save_as_file_content, "|+|")
        main_window.show_cmd = False
        cmd = "f = os.remove('%s')\r\n" % (page.directory + "/" + page.filename)
        asyncio.run(SendCmdAsync(main_window, cmd))
        cmd = "f = open('%s', 'wb')\r\n" % (page.directory + "/" + page.filename)
        asyncio.run(SendCmdAsync(main_window, cmd))
        cmd = "f.write(%s)\r\n" % save_as_file_content
        asyncio.run(SendCmdAsync(main_window, cmd))
        cmd = "f.close()\r\n"
        asyncio.run(SendCmdAsync(main_window, cmd))
        page.last_save = save_as_file_content
        page.saved = True
        treeModel(main_window)
        main_window.shell.AppendText("Content Saved\n")
        self.main_window.speak_on = "Content Saved"

def load_img(path):
    return wx.Image(path,wx.BITMAP_TYPE_ANY).ConvertToBitmap()

def speak(main_window, txt):
    if main_window.voice_on:
        speech.say(txt)

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

async def SetView(main_window, info):
    main_window.show_cmd = info

def getFileTree(main_window, dir):
        print("GET FILE TREE : %s"%(dir))
        main_window.cmd_return = ""
        main_window.get_cmd = True
        asyncio.run(SendCmdAsync(main_window, "os.listdir(\'%s\')\r\n"%dir))
        result = main_window.read_cmd("os.listdir(\'%s\')"%dir)
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
            asyncio.run(SendCmdAsync(main_window, "os.stat(\'%s\')\r\n"%(dir + "/" + i)))
            res = main_window.read_cmd("os.stat(\'%s\')"%(dir + "/" + i))
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
                        ret[dir].append(getFileTree(main_window, dir+"/"+i))
                else:
                    ret[dir].append(i)
            except Exception as e:
                print("ERROr: " + e)
                return "err"
        return ret

def treeModel(main_window):
        main_window.show_cmd = False
        main_window.reflushTreeBool= True
        main_window.cmd_return = ""
        main_window.device_tree.DeleteChildren(main_window.device_tree.root)
        res=json.loads("{}")
        res=getFileTree(main_window, ".")

        if res=="err":
            main_window.cmd_return = ""
            return
        print("RESSSSSSS")
        print(res)
        try:
            ReflushTree(main_window,main_window.device_tree.root,res['.'])
        except Exception as e:
            print(e)
        main_window.cmd_return =""
        main_window.show_cmd = True
    
def ReflushTree(main_window, root, msg):
        if msg=="err":
            print("soucii")
            return
        print("reflushTree=====================%s"%msg)
        print("MSG " + str(msg))
        tree = main_window.device_tree
        if type(msg) is str: #: fichier
            child = tree.AppendItem(root, msg)
            tree.SetItemImage(child, tree.fileidx, wx.TreeItemIcon_Normal)
            tree.SetItemImage(child, tree.fileidx, wx.TreeItemIcon_Expanded)
            #root.RemoveItem(itemDevice.Item())
            
        elif type(msg) is dict: #: dossier
            for i in msg:
                k=eval("%s"%msg[i])
                i=i.split("/")
                #print("KKKK = ", k, "I = ", i)
                child = tree.AppendItem(root, i[1])
                tree.SetItemImage(child, tree.fldridx, wx.TreeItemIcon_Normal)
                tree.SetItemImage(child, tree.fldropenidx, wx.TreeItemIcon_Expanded)
                ReflushTree(main_window, child, k)
        elif type(msg) is list: #liste de fichiers
            for i in msg:
                if type(i) is str:
                    ReflushTree(main_window, root, i)
                elif type(i) is dict:
                    ReflushTree(main_window, root, i)           
                else:
                    pass

def create_Menu_item(parentMenu, id_id, text, submenu, theme_name):

    item = wx.MenuItem(id=id_id, text=text, helpString=text, subMenu=submenu)
    wx.Menu
    try:
        #file = open("./customize.json")
        #theme = json.load(file)
        #file.close()
        #theme = theme[theme_name]
        return item
    except Exception as e:
        print(e)
        print("Can't customize ItemMenu")
        return item

def setDefaultProg(main_window,filename):
    print("setDefaultProg:%s"%filename)
    main_window.show_cmd = False
    ProgMsg= ""
    asyncio.run(SendCmdAsync(main_window, "myfile=open(\'main.py\',\'w\')\r\n"))
    ProgMsg = main_window.read_cmd("myfile=open(\'main.py\',\'w\')")
    if ProgMsg.find("Traceback")>=0 or ProgMsg.find("... ")>=0:
        asyncio.run(SendCmdAsync(main_window, "\x03"))
        return
    cmd = "myfile.write(\"exec(open(\'%s\').read(),globals())\")\r\n"%str(filename)
    asyncio.run(SendCmdAsync(main_window, cmd))
    ProgMsg = main_window.read_cmd(cmd[:-2])
    if ProgMsg.find("Traceback")>=0 or ProgMsg.find("... ")>=0:
        asyncio.run(SendCmdAsync(main_window, "\x03"))
        return
    cmd = "myfile.close()\r\n"
    asyncio.run(SendCmdAsync(main_window, cmd))
    ProgMsg = main_window.read_cmd(cmd[:-2])
    if ProgMsg.find("Traceback")>=0 or ProgMsg.find("... ")>=0:
        asyncio.run(SendCmdAsync(main_window, "\x03"))
        return
    main_window.show_cmd = True