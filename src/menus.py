from Packages import wx, os, sys, time, speech, Serial, InitConfig
from panels import *
from Utilitaries import load_img, speak
from api import main as CheckPySyntax
from Serial import SerialRxEvent
from Constantes import *

def Init_Top_Menu(frame):
    """Inits and place the top menu

    :param frame: Mainwindow
    :type frame: Mainwindow
    """    
    frame.top_menu = TopMenu(frame)
    frame.SetMenuBar(frame.top_menu)
    return frame.top_menu

def Init_ToolBar(frame):
    """Inits and place the toolbar

    :param frame: Mainwindow
    :type frame: Mainwindow
    """    
    frame.ToolBar = ToolBar(frame)
    frame.SetToolBar(frame.ToolBar)

def create_File_Menu():
    """Inits a File menu and his buttons (Save, Open,...)

    :return: the File menu filled by buttons
    :rtype: wx.Menu see https://wxpython.org/Phoenix/docs/html/wx.Menu.html
    """    
    MenuFile = wx.Menu()
    MenuFile.Append(wx.ID_NEW, "&New\tCTRL+N")
    MenuFile.Append(wx.ID_SAVE, "&Save\tCTRL+S")
    MenuFile.Append(wx.ID_SAVEAS, "&Save as\tCTRL+A")
    MenuFile.Append(wx.ID_OPEN, "&Open\tCTRL+O")
    MenuFile.Append(wx.ID_REFLUSH_DIR, "&Reflush Directory")
    MenuFile.Append(wx.ID_EXAMPLES, "&Examples")
    MenuFile.Append(wx.ID_EXIT, "&Exit\tCTRL+Q")
    MenuFile.Append(wx.ID_CLOSE, "&Close\tCTRL+W")
    MenuFile.AppendSeparator()
    return MenuFile

def create_Edit_Menu():
    """Inits a Edit menu and his buttons (Copy, Paste, Find,...)

    :return: the Edit menu filled by buttons
    :rtype: wx.Menu see https://wxpython.org/Phoenix/docs/html/wx.Menu.html
    """    
    MenuEdit = wx.Menu()
    MenuEdit.Append(wx.ID_COPY, "&Copy\tCTRL+C")
    MenuEdit.Append(wx.ID_CUT, "&Cut\tCTRL+X")
    MenuEdit.Append(wx.ID_PASTE, "&Paste\tCTRL+V")
    MenuEdit.Append(wx.ID_REDO, "&Redo\tCTRL+Z")
    MenuEdit.Append(wx.ID_UNDO, "&Redo\tCTRL+Z")
    MenuEdit.Append(wx.ID_SYNTAX_CHECK, "&Syntax Check")
    MenuEdit.Append(wx.ID_FIND, "&Find and/or Replace\tCTRL+F")
    MenuEdit.AppendSeparator()
    return MenuEdit

def create_Board_Menu():
    MenuTools = wx.Menu()
    MenuTools.Append(wx.ID_ESP32_CHOICE, "&ESP32")
    MenuTools.Append(wx.ID_PYBOARD_CHOICE, "&PYboard")
    return MenuTools

def create_Themes_Menu():
    MenuTools = wx.Menu()
    MenuTools.Append(wx.ID_DARK_THEME, "&Dark")
    MenuTools.Append(wx.ID_LIGHT_THEME, "&Light")
    MenuTools.Append(wx.ID_ASTRO_THEME, "&Astro")
    return MenuTools
    
def create_Tools_Menu():
    MenuTools = wx.Menu()
    MenuTools.Append(wx.ID_SERIAL, "&Serial")
    MenuTools.Append(wx.ID_BOARD, "&Board", create_Board_Menu())
    MenuTools.Append(wx.ID_DOWNLOAD, "&Download")
    MenuTools.Append(wx.ID_EXECUTE, "&DownloadandRun\tF5")
    MenuTools.Append(wx.ID_STOP, "&Stop")
    MenuTools.Append(wx.ID_BURN_FIRMWARE, "&BurnFirmware")
    MenuTools.Append(wx.ID_INIT, "Initconfig")
    MenuTools.Append(wx.ID_PREFERENCES, "Preferences")
    MenuTools.Append(wx.ID_SETTINGS, "&Port Settings\tF2", "", wx.ITEM_NORMAL)
    MenuTools.Append(wx.ID_BOARD, "&Themes", create_Themes_Menu())
    MenuTools.AppendSeparator()
    return MenuTools

class TopMenu(wx.MenuBar):
    """TopMenu class which contains the Edit and File Menus

    :param wx.MenuBar: Parent class to contain menus see  https://wxpython.org/Phoenix/docs/html/wx.MenuBar.html
    """    
    def __init__(self, parent):
        """Constructor which append the Edit and File Menus on the Menubar and bind related events

        :param parent: Parent class (in this case MainWindow)
        :type parent: class Mainwindow
        """        
        wx.MenuBar.__init__(self)
        self.parent = parent
        self.MenuFile = create_File_Menu()
        self.MenuEdit = create_Edit_Menu()
        self.MenuTools = create_Tools_Menu()
        self.Append(self.MenuFile, "&File")
        self.Append(self.MenuEdit, "&Edit")
        self.Append(self.MenuTools, "&Tools")
        self.__attach_events__()
        
    def __attach_events__(self):
        self.Bind(wx.EVT_MENU,  self.OnExit, id=wx.ID_EXIT)
        self.Bind(wx.EVT_MENU,  self.OnOpen, id=wx.ID_OPEN)
        self.Bind(wx.EVT_MENU,  self.OnSaveAs, id=wx.ID_SAVEAS)
        self.Bind(wx.EVT_MENU,  self.OnSave, id=wx.ID_SAVE)
        self.Bind(wx.EVT_MENU,  self.OnCopy, id=wx.ID_COPY)
        self.Bind(wx.EVT_MENU,  self.OnPaste, id=wx.ID_PASTE)
        self.Bind(wx.EVT_MENU,  self.OnCut, id=wx.ID_CUT)
        self.Bind(wx.EVT_MENU,  self.OnFindReplace, id=wx.ID_FIND)

        self.Bind(wx.EVT_MENU,  self.OnSyntaxCheck, id=wx.ID_SYNTAX_CHECK)
        self.Bind(wx.EVT_MENU,  self.OnAddPage, id=wx.ID_NEW)
        self.Bind(wx.EVT_MENU,  self.OnClosePage, id=wx.ID_CLOSE)
        self.Bind(wx.EVT_MENU, self.OnPortSettings, id=wx.ID_SETTINGS)
        self.Bind(wx.EVT_MENU, self.OnDownloadFile, id=wx.ID_DOWNLOAD)
        self.Bind(wx.EVT_MENU, self.OnRun, id=wx.ID_EXECUTE)

        self.Bind(wx.EVT_MENU,  self.OnChangeTheme, id=wx.ID_LIGHT_THEME)
        self.Bind(wx.EVT_MENU,  self.OnChangeTheme, id=wx.ID_DARK_THEME)
        self.Bind(wx.EVT_MENU,  self.OnChangeTheme, id=wx.ID_ASTRO_THEME)

    def OnExit(self, evt):
        """Quit the app

        :param evt: always to get the macrocode
        :type evt: (wx.event ?)
        """        
        self.Parent.Destroy()

    def OnSave(self, evt):
        """Save the current page of the notebook

        :param evt: always to get the macrocode
        :type evt: (wx.event ?)
        """   
        notebookP = self.parent.MyNotebook
        page = notebookP.GetCurrentPage()
        # Check if save is required
        if (page.GetValue() != page.last_save):
            page.saved = False

        # Check if Save should bring up FileDialog
        if (page.saved == False and page.last_save == ""): 
            dialog = wx.FileDialog(self, 
                                   "Choose a file", 
                                   page.directory, 
                                   "", 
                                   "*", 
                                   wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
            if dialog.ShowModal() == wx.ID_OK:
                # Grab the content to be saved
                save_as_file_contents = page.GetValue()

                # Open, Write & Close File
                save_as_name = dialog.GetFilename()
                save_as_directory = dialog.GetDirectory()    
                filehandle=open(os.path.join(save_as_directory, save_as_name), 'w')
                filehandle.write(save_as_file_contents)
                filehandle.close()
                notebookP.SetPageText(notebookP.GetSelection(), save_as_name)
                page.filename = save_as_name
                page.directory = save_as_directory
                page.last_save = save_as_file_contents
                page.saved = True
        else:
            # Grab the content to be saved
            save_as_file_contents = page.GetValue()
            filehandle=open(os.path.join(page.directory, page.filename), 'w')
            filehandle.write(save_as_file_contents)
            filehandle.close()
            page.last_save = save_as_file_contents
            page.saved = True
        self.parent.Shell.AppendText("Content Saved\n")
        speak(self.parent, "Content Saved")

    def OnSaveAs(self, evt):
        """Open a wx.filedialog to Save as a file the text of the current editor

        :param evt: always to get the macrocode
        :type evt: (wx.event ?)
        """   
        notebookP = self.parent.MyNotebook
        page = notebookP.GetCurrentPage()
        dialog = wx.FileDialog(self, 
                               "Choose a file", 
                               page.directory, 
                               "", 
                               "*.py*", 
                               wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        if dialog.ShowModal() == wx.ID_OK:
            # Grab the content to be saved
            save_as_file_contents = page.GetValue()
            # Open, Write & Close File
            save_as_name = dialog.GetFilename()
            save_as_directory = dialog.GetDirectory()
            filehandle=open(os.path.join(save_as_directory, save_as_name), 'w')
            filehandle.write(save_as_file_contents)
            filehandle.close()
            notebookP.SetPageText(notebookP.GetSelection(), save_as_name)
            page.filename = save_as_name
            page.directory = save_as_directory
            page.last_save = save_as_file_contents
            page.saved = True
            speak(self.parent, "Content Saved")
        dialog.Destroy()

    def OnOpen(self, evt):
            """Open a wx.filedialog to open a file on a editor 

            :param evt: always to get the macrocode
            :type evt: (wx.event ?)
            """  
            notebookP = self.parent.MyNotebook
            dialog = wx.FileDialog(self, 
                               "Choose a File", 
                               notebookP.GetCurrentPage().directory, 
                               "", 
                               "*", 
                               wx.FD_OPEN)
            if dialog.ShowModal() == wx.ID_OK:
                filename = dialog.GetFilename()
                directory = dialog.GetDirectory()
                filehandle = open(os.path.join(directory, filename), 'r')
                # Check if a new tabe needs to be created to display contents of opened file
                if (notebookP.GetPageCount() == 1 
                    and notebookP.GetCurrentPage().GetValue() == ""):
                    notebookP.GetCurrentPage().SetValue(filehandle.read())
                    notebookP.GetCurrentPage().filename = filename
                    notebookP.GetCurrentPage().directory = directory
                    notebookP.GetCurrentPage().last_save = notebookP.GetCurrentPage().GetValue()
                    notebookP.GetCurrentPage().saved = True
                else:
                    print("")
                    notebookP.tab_num += 1
                    new_tab = MyEditor(notebookP)
                    new_tab.filename = filename
                    new_tab.directory = directory
                    notebookP.AddPage(new_tab, filename, select = True)
                    wx.CallAfter(new_tab.SetFocus)
                # Populate the tab with file contents
                    new_tab.SetValue(filehandle.read())
                    new_tab.last_save = new_tab.GetValue()
                    new_tab.saved = True
                notebookP.SetPageText(notebookP.GetSelection(), filename)
                filehandle.close()
            dialog.Destroy()

    def OnCopy(self, event):
        """Copy the selection on the clipboard

        :param evt: always to get the macrocode
        :type evt: (wx.event ?)
        """  
        self.parent.MyNotebook.GetCurrentPage().Copy()

    def OnPaste(self, event):
        """Paste the content of the clipboard

        :param evt: always to get the macrocode
        :type evt: (wx.event ?)
        """  
        self.parent.MyNotebook.GetCurrentPage().Paste()

    def OnCut(self, event):
        """Cut the selection on the clipboard

        :param evt: always to get the macrocode
        :type evt: (wx.event ?)
        """  
        self.parent.MyNotebook.GetCurrentPage().Cut()

    def OnRedo(self, event):
        """Redo

        :param evt: always to get the macrocode
        :type evt: (wx.event ?)
        """  
        self.parent.MyNotebook.GetCurrentPage().Redo()

    def OnUndo(self, event):
        """Undo

        :param evt: always to get the macrocode
        :type evt: (wx.event ?)
        """  
        self.parent.MyNotebook.GetCurrentPage().Undo()

    def OnFindReplace(self, event):
        """Open a wx.FindReplaceDialog to find and/, replace text in the current editor

        :param evt: always to get the macrocode
        :type evt: (wx.event ?)
        """  
        notebookP = self.parent.MyNotebook
        page = notebookP.GetCurrentPage()
        if page == None:
            return
        page.OnShowFindReplace()

    def OnAddPage(self, event):
        """Add a new page on the notebook

        :param evt: always to get the macrocode
        :type evt: (wx.event ?)
        """
        notebookP = self.parent.MyNotebook
        notebookP.tab_num += 1
        new_tab = MyEditor(self.parent.MyNotebook, self.parent)
        new_tab = notebookP.AddPage(new_tab, "Tab %s" % notebookP.tab_num, select=True)

    def OnClosePage(self, event):
        """Close the current page and update id order

        :param evt: always to get the macrocode
        :type evt: (wx.event ?)
        """  
        #TODO: ajouter un choix de sauvegarde si saved = False
        
        dataNoteBook = self.parent.MyNotebook
        page = dataNoteBook.GetCurrentPage()
        print("Deleted page: " + str(page.id))
        print(dataNoteBook.GetPageText(page.id - 1))
        dataNoteBook.DeletePage(page.id - 1)
        dataNoteBook.tab_num -= 1
        #Update Ids 
        i = 1
        maxi = dataNoteBook.GetPageCount()
        print("Maxi : " + str(maxi))
        while i <= maxi:
            page_a = dataNoteBook.GetPage(i)
            if page_a.id > page.id:
                page_a.id -= 1
            print("Id = " + str(page_a.id))
            i += 1
    
    def OnChangeTheme(self, event):
        menuId = event.Id
        i = 0
        list = [wx.ID_DARK_THEME, wx.ID_LIGHT_THEME, wx.ID_ASTRO_THEME]
        for x in list:
            if x == menuId:
                print('Theme = ' + str(i))
                break
            i += 1
        
        Change_Theme(self.parent.MyNotebook.GetCurrentPage(), themes[i], py_style)
        self.parent.Shell.Custom_Shell(themes[i])
        self.parent.TreeCtrl.Custom_Tree_Ctrl(themes[i])
        self.parent.MyNotebook.Custom_Notebook(themes[i])
        self.parent.MyNotebook.theme = i
    
    def OnSyntaxCheck(self, event):
        page = self.parent.MyNotebook.GetCurrentPage()
        
        syntaxCheckFilePath="%s/AppData/Local/uPyCraft/temp/syntaxCheck.py"%rootDirectoryPath
        syntaxCheckFileText=page.GetValue()

        filehandle=open(syntaxCheckFilePath,"wb")
        syntaxCheckFileText=syntaxCheckFileText.split("\r")
        nocheck=0
        for i in syntaxCheckFileText:
            if i.find("'''")>=0 and nocheck==0:
                nocheck=1
            elif i.find("'''")>=0 and nocheck==1:
                nocheck=0

            if nocheck==1:
                if i=="":
                    filehandle.write('\r'.encode('utf-8'))
                    continue
                else:
                    filehandle.write(i.encode('utf-8'))
                    filehandle.write('\r'.encode('utf-8'))
                    continue
            elif i=="":
                filehandle.write('\r'.encode('utf-8'))
                continue
            filehandle.write(i.encode('utf-8'))
            filehandle.write('\r'.encode('utf-8'))
        
        filehandle.close()

        backStdout=sys.stdout
        backStderr=sys.stderr
        stdoutFilePath="%s/AppData/Local/uPyCraft/temp/stdout.py"%rootDirectoryPath
        stderrFilePath="%s/AppData/Local/uPyCraft/temp/stderr.py"%rootDirectoryPath
        stdoutFile=open(stdoutFilePath,'w')
        stderrFile=open(stderrFilePath,'w')
        sys.stdout=stdoutFile
        sys.stderr=stderrFile
        CheckPySyntax(None,str(syntaxCheckFilePath))
        sys.stdout=backStdout
        sys.stderr=backStderr
        stdoutFile.close()
        stderrFile.close()
        
        stdoutFile=open(stdoutFilePath,'r')
        stderrFile=open(stderrFilePath,'r')
        stdout = stdoutFile.read()
        stderr = stderrFile.read()
        stdoutFile.close()
        stderrFile.close()
        
        appendMsg=page.filename
        
        if str(stdout)=="" and str(stderr)=="":
            speak(self.parent, "No Error Detected !")
            pass
        else:
            speak(self.parent, "Some Errors or Warnings Detected, check")
            if stdout!="":
                stdout=stdout.split("\n")
                for i in stdout:
                    if i=="":
                        continue
                    if i.find("syntaxCheck.py")>0:
                        i=i[len(syntaxCheckFilePath):]
                    appendMsg=appendMsg + i + "\n"
                self.parent.Shell.AppendText(appendMsg)
            if stderr=="":
                pass
            else:
                stderr=stderr.split("\n")
                for i in stderr:
                    if i=="":
                        continue
                    if i.find("syntaxCheck.py")>0:
                        i=i[len(syntaxCheckFilePath):]
                    appendMsg=appendMsg + "\n" + i
                self.parent.Shell.AppendText(appendMsg)
        self.parent.Shell.AppendText("Syntax terminated.\n")
    
    def OnPreferences(self, event):
        self.parent.preferences.Show()
    
    def OnPortSettings(self, event):
        """
        Show the port settings dialog. The reader thread is stopped for the
        settings change.
        """
        print("BANANA")
        ok = False
        parent = self.parent
        while not ok:
            with wxSerialConfigDialog.SerialConfigDialog(
                    self,
                    -1,
                    "",
                    show=wxSerialConfigDialog.SHOW_BAUDRATE | wxSerialConfigDialog.SHOW_FORMAT | wxSerialConfigDialog.SHOW_FLOW,
                    serial=parent.serial) as dialog_serial_cfg:
                dialog_serial_cfg.CenterOnParent()
                result = dialog_serial_cfg.ShowModal()
            # open port if not called on startup, open it on startup and OK too
            if result == wx.ID_OK or event is not None:
                try:
                    parent.serial.open()
                except serial.SerialException as e:
                    with wx.MessageDialog(self, str(e), "Serial Port Error", wx.OK | wx.ICON_ERROR)as dlg:
                        dlg.ShowModal()
                        ok = True
                else:
                    parent.StartThread()
                    dialog_serial_cfg.SetTitle("Serial Terminal on {} [{},{},{},{}{}{}]".format(
                        parent.serial.portstr,
                        parent.serial.baudrate,
                        parent.serial.bytesize,
                        parent.serial.parity,
                        parent.serial.stopbits,
                        ' RTS/CTS' if parent.serial.rtscts else '',
                        ' Xon/Xoff' if parent.serial.xonxoff else '',
                        ))
                    ok = True
            else:
                # on startup, dialog aborted
                parent.alive.clear()
                ok = True
        if parent.serial.isOpen() == True:
            parent.FileTree.Update()
            #TODO: change status Barre
            parent.serial.flush()
            parent.serial_manager.put_cmd('import os\r\n')
            speak(parent, "Device Connected")
            
    def OnDownloadFile(self, event):
        parent = self.parent
        notebookP = self.parent.MyNotebook
        page = notebookP.GetCurrentPage()
        if parent.serial.isOpen()==False:
            parent.Shell.AppendText('Please open serial')
            return False
        parent.serial.write('\x03'.encode('utf-8'))
        self.parent.show_cmd = False
        time.sleep(0.05)

        if page == None:
            parent.Shell.AppendText('Please choose file or input something')
            return False
        print("dir = %s %s"%(page.directory, page.filename))
        if page.directory[len(page.directory) - 1] == '/':
            pathfile=page.directory + page.filename
        else:
            pathfile=page.directory + '/' + page.filename
        if page.saved == False:
            parent.Shell.append('Please save the file before download')
            return False
        elif str(pathfile).find(":")>=0:
            parent.serial_manager.downloadFile(pathfile, page.filename)
            time.sleep(1)
            #self.parent.Shell.Clear()
            self.parent.Shell.SetValue("Downloaded file : " + page.filename)
            #TODO:Transformer en fonction les 2 lignes suiv
            event = SerialRxEvent(self.parent.GetId(), "show_cmd")
            self.parent.GetEventHandler().AddPendingEvent(event)
            self.parent.Shell.SetFocus()
            self.serial_manager.put_cmd('\r\n')
            return True
    
        return False

    def OnRun(self, event):
        parent = self.parent
        notebookP = self.parent.MyNotebook
        page = notebookP.GetCurrentPage()
        if parent.serial.isOpen()==False:
            parent.Shell.AppendText('Please open serial')
            return False
        parent.serial.write('\x03'.encode('utf-8'))
        self.parent.show_cmd = False
        time.sleep(0.05)

        if page == None:
            parent.Shell.AppendText('Please choose file or input something')
            return False
        print("dir = %s %s"%(page.directory, page.filename))
        if page.saved == False:
            parent.Shell.append('Please save the file before download')
            return False
        if page.directory[len(page.directory) - 1] == '/':
            pathfile=page.directory + page.filename
        else:
            pathfile=page.directory + '/' + page.filename
        if str(pathfile).find(":")>=0:
            parent.serial_manager.downloadFile(pathfile, page.filename)
            time.sleep(1)
            self.parent.Shell.SetValue("Downloaded file : " + page.filename)
            #TODO:Transformer en fonction les 2 lignes suiv
            event = SerialRxEvent(self.parent.GetId(), "show_cmd")
            self.parent.GetEventHandler().AddPendingEvent(event)
            self.parent.Shell.SetFocus()
            self.parent.serial_manager.downloadRun(page.filename)
            return True
        return False

class ToolBar(wx.ToolBar):
    """MOMENT : Derivated class to set A toolbar maybe we'll erase this derivated class

    :param wx.ToolBar: see https://wxpython.org/Phoenix/docs/html/wx.ToolBar.html
    """    
    def __init__(self, parent):
        """constructor for ToolBar 

        :param parent: Parent class generally the main window
        :type parent: MainWindow (generally)
        """           
        wx.ToolBar.__init__(self, parent=parent, style= wx.TB_RIGHT | wx.TB_DOCKABLE | wx.FULL_REPAINT_ON_RESIZE)
        self.CentreOnParent()
        self.parent = parent
        
        self.AddTools()
        self.__set_properties()
        self.__attach_events(parent)

    def AddTools(self):
        self.AddTool(wx.ID_NEW, '', load_img('./img/newfile.png'))
        self.AddTool(wx.ID_OPEN, '', load_img('./img/fileopen.png'))
        self.AddTool(wx.ID_SAVE, '', load_img('./img/save.png'))
        self.AddTool(wx.ID_EXECUTE, '', load_img('./img/downloadandrun.png'))
        #TODO: ajouter disconnectg with boolean
        self.AddTool(wx.ID_CONNECT, '', load_img('./img/serialConnect.png'))
        self.AddTool(wx.ID_STOP, '', load_img('./img/stop.png'))
        self.AddTool(wx.ID_UNDO, '', load_img('./img/undo.png'))
        self.AddTool(wx.ID_REDO, '', load_img('./img/redo.png'))
        self.AddTool(wx.ID_SYNTAX_CHECK, '', load_img('./img/syntaxCheck.png'))
        self.AddTool(wx.ID_CLEAR, '', load_img('./img/clear.png'))

    def __set_properties(self):
        self.Realize()
        self.SetBackgroundColour("black")

    def __attach_events(self, parent):
        self.Bind(wx.EVT_MENU, parent.top_menu.OnAddPage, id=wx.ID_NEW)
        self.Bind(wx.EVT_MENU, parent.top_menu.OnOpen, id=wx.ID_OPEN)
        self.Bind(wx.EVT_MENU, parent.top_menu.OnSave, id=wx.ID_SAVE)
        self.Bind(wx.EVT_MENU, parent.top_menu.OnRun, id=wx.ID_EXECUTE)
        self.Bind(wx.EVT_MENU, parent.top_menu.OnSyntaxCheck, id=wx.ID_SYNTAX_CHECK)
        self.Bind(wx.EVT_MENU, self.OnClear, id=wx.ID_CLEAR)
        self.Bind(wx.EVT_MENU, parent.top_menu.OnUndo, id=wx.ID_UNDO)
        self.Bind(wx.EVT_MENU, parent.top_menu.OnRedo, id=wx.ID_REDO)
        
    def OnClear(self, event):
        self.parent.Shell.Clear()
        speak(self.parent, "Terminal Cleared")