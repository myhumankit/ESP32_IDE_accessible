from packages import wx, os, sys, time, speech, serial, asyncio
import my_serial
from my_serial import put_cmd
from panels import *
from utilitaries import *
from api.api_pyflakes import main as CheckPySyntax
from constantes import *
from firmware import UpdateFirmwareDialog, FirmwareThread, BurnFrame

#? Doit-on retourner le menu et la toolbar pour la stocker avec self. 
#? ou la stocke t-on directement dans les fonctions associés

#TODO: CUSTOM FONT OF MENUSS

def init_top_menu(main_window):
    """Inits an instance of customized TopMenu class and places it on the main_window

    :param main_window: main_window which will contains the MenuBar
    :type main_window: wx.main_window https://wxpython.org/Phoenix/docs/html/wx.main_window.html
    """

    main_window.top_menu = TopMenu(main_window)
    main_window.SetMenuBar(main_window.top_menu)

    return main_window.top_menu

def init_toolbar(main_window):
    """Inits an instance of the customized ToolBar class and places it on the main_window

    :param main_window: main_window which will contains the ToolBar
    :type main_window: wx.main_window https://wxpython.org/Phoenix/docs/html/wx.main_window.html
    """  
    
    main_window.ToolBar = ToolBar(main_window)
    main_window.SetToolBar(main_window.ToolBar)

class ThemesMenu(wx.Menu):
    """Inits a instance of a wx.Menu to create a Theme menu and his buttons (Copy, Paste, Find,...)

    :return: the Theme menu filled by buttons
    :rtype: wx.Menu see https://wxpython.org/Phoenix/docs/html/wx.Menu.html
    """
    def __init__(self, main_window):
        wx.Menu.__init__(self, "")
        
        self.Append(wx.ID_DARK_THEME, "&Dark")
        self.Append(wx.ID_LIGHT_THEME, "&Light")

class FileMenu(wx.Menu):
    """Inits a instance of a wx.Menu to create a Theme menu and his buttons (Copy, Paste, Find,...)

    :return: the Theme menu filled by buttons
    :rtype: wx.Menu see https://wxpython.org/Phoenix/docs/html/wx.Menu.html
    """
    def __init__(self, main_window):
        wx.Menu.__init__(self, "File")

        self.main_window = main_window
        self.Append(wx.ID_NEW, "&New\tCTRL+N")
        self.Append(wx.ID_OPEN, "&Open\tCTRL+O")
        self.Append(wx.ID_SAVE, "&Save\tCTRL+S")
        self.Append(wx.ID_SAVEAS, "&Save as\tCTRL+A")
        self.Append(wx.ID_CLOSE, "&Close\tCTRL+W")
        self.Append(wx.ID_EXIT, "&Exit\tCTRL+Q")
        self.AppendSeparator()

    def OnExit(self, evt):
        """Quit the app

        :param evt: Event to trigger the method
        :type evt: wx.Event
        """        
        self.main_window.stop_thread_serial()
        self.main_window.Destroy()

    def OnSave(self, evt):
        """Save the current page of the notebook

        :param evt: Event to trigger the method
        :type evt: wx.Event
        """   
        notebookP = self.main_window.MyNotebook
        page = notebookP.GetCurrentPage()
        if page.on_card:
            return save_on_card(self.main_window, page)
        # Check if save is required
        if (page.GetValue() != page.last_save):
            page.saved = False

        # Check if Save should bring up FileDialog
        if (page.saved == False and page.last_save == ""): 
            dialog = wx.FileDialog(self.main_window, "Choose a file", \
                page.directory, "", "*", wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
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
        self.main_window.Shell.AppendText("Content Saved\n")
        speak(self.main_window, "Content Saved")

    def OnSaveAs(self, evt):
        """Open a wx.filedialog to Save as a file the text of the current editor

        :param evt: Event to trigger the method
        :type evt: wx.Event
        """   
        notebookP = self.main_window.MyNotebook
        page = notebookP.GetCurrentPage()
        dialog = wx.FileDialog(self.main_window, "Choose a file", page.directory, \
                               "", "*.py*", wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        
        dialog.CenterOnParent()
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
            speak(self.main_window, "Content Saved")
        dialog.Destroy()

    def OnOpen(self, evt):
            """Open a wx.filedialog to open a file on a editor 

            :param evt: Event to trigger the method
            :type evt: wx.Event
            """  
            notebookP = self.main_window.MyNotebook
            dialog = wx.FileDialog(self.main_window, 
                               "Choose a File", 
                               notebookP.GetCurrentPage().directory, 
                               "", 
                               "*", 
                               wx.FD_OPEN)
            
            dialog.CenterOnParent()
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
                    new_tab = MyEditor(notebookP, self.main_window, "", False)
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

    def OnAddPage(self, evt):
        """Add a new page on the notebook

        :param evt: Event to trigger the method
        :type evt: wx.Event
        """
        notebookP = self.main_window.MyNotebook
        notebookP.tab_num += 1
        #RAJOUTER une variable on_card and Value
        new_tab = MyEditor(self.main_window.MyNotebook, self.main_window, "", False)
        new_tab = notebookP.AddPage(new_tab, "Tab %s" % notebookP.tab_num, select=True)

    def OnClosePage(self, evt):
        """Close the current page and update id order

        :param evt: Event to trigger the method
        :type evt: wx.Event
        """  
        #TODO: ajouter un choix de sauvegarde si saved = False
        
        dataNoteBook = self.main_window.MyNotebook
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
    
class EditMenu(wx.Menu):
    """Inits a instance of a wx.Menu to create a Theme menu and his buttons (Copy, Paste, Find,...)

    :return: the Theme menu filled by buttons
    :rtype: wx.Menu see https://wxpython.org/Phoenix/docs/html/wx.Menu.html
    """
    def __init__(self, main_window):
        wx.Menu.__init__(self, "Edit")

        self.main_window = main_window
        self.Append(wx.ID_COPY, "&Copy\tCTRL+C")
        self.Append(wx.ID_CUT, "&Cut\tCTRL+X")
        self.Append(wx.ID_PASTE, "&Paste\tCTRL+V")
        self.Append(wx.ID_REDO, "&Redo\tCTRL+Z")
        self.Append(wx.ID_UNDO, "&Redo\tCTRL+Z")
        self.Append(wx.ID_SYNTAX_CHECK, "&Syntax Check")
        self.Append(wx.ID_FIND, "&Find and/or Replace\tCTRL+F")
        self.AppendSeparator()
    
    def OnCopy(self, evt):
        """Copy the selection on the clipboard

        :param evt: Event to trigger the method
        :type evt: wx.Event
        """  
        self.main_window.MyNotebook.GetCurrentPage().Copy()

    def OnPaste(self, evt):
        """Paste the content of the clipboard

        :param evt: Event to trigger the method
        :type evt: wx.Event
        """  
        self.main_window.MyNotebook.GetCurrentPage().Paste()

    def OnCut(self, evt):
        """Cut the selection on the clipboard

        :param evt: Event to trigger the method
        :type evt: wx.Event
        """  
        self.main_window.MyNotebook.GetCurrentPage().Cut()

    def OnRedo(self, evt):
        """Redo

        :param evt: Event to trigger the method
        :type evt: wx.Event
        """  
        self.main_window.MyNotebook.GetCurrentPage().Redo()

    def OnUndo(self, evt):
        """Undo

        :param evt: Event to trigger the method
        :type evt: wx.Event
        """  
        self.main_window.MyNotebook.GetCurrentPage().Undo()

    def OnFindReplace(self, evt):
        """Open a wx.FindReplaceDialog to find and/, replace text in the current editor

        :param evt: Event to trigger the method
        :type evt: wx.Event
        """  
        notebookP = self.main_window.MyNotebook
        page = notebookP.GetCurrentPage()
        if page == None:
            return
        page.OnShowFindReplace()
   
    def OnSyntaxCheck(self, evt):
        """Check the python syntax on the current Tab

        :param evt: Event to trigger the method
        :type evt: wx.Event
        """  
        page = self.main_window.MyNotebook.GetCurrentPage()
        
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
            speak(self.main_window, "No Error Detected !")
            pass
        else:
            speak(self.main_window, "Some Errors or Warnings Detected, check")
            if stdout!="":
                stdout=stdout.split("\n")
                for i in stdout:
                    if i=="":
                        continue
                    if i.find("syntaxCheck.py")>0:
                        i=i[len(syntaxCheckFilePath):]
                    appendMsg=appendMsg + i + "\n"
                self.main_window.Shell.AppendText(appendMsg)
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
                self.main_window.Shell.AppendText(appendMsg)
        self.main_window.Shell.AppendText("Syntax terminated.\n")
    
class ToolsMenu(wx.Menu):
    """Class to create a Tools menu and his buttons (Copy, Paste, Find,...)

    :param: Class to derivate
    :type: wx.Menu see https://wxpython.org/Phoenix/docs/html/wx.Menu.html
    """
    def __init__(self, main_window):
        wx.Menu.__init__(self, "Tools")

        self.main_window = main_window
        self.themes_submenu = ThemesMenu(main_window)
        self.Append(wx.ID_SETTINGS, "&Port Settings\tF2", "", wx.ITEM_NORMAL)
        self.Append(wx.ID_DOWNLOAD, "&Download")
        self.Append(wx.ID_EXECUTE, "&DownloadandRun\tF5")
        self.Append(wx.ID_STOP, "&Stop")
        self.Append(wx.ID_BURN_FIRMWARE, "&BurnFirmware")
        self.Append(wx.ID_BOARD, "&Themes", self.themes_submenu)

    def OnPortSettings(self, evt):
        """
        Show the port settings dialog. The reader thread is stopped for the
        settings change.
        
        :param evt: Event to trigger the method
        :type evt: wx.Event
        """  
        ok = False
        main_window = self.main_window
        while not ok:
            with wxSerialConfigDialog.SerialConfigDialog(
                    self.main_window,
                    -1,
                    "",
                    show=wxSerialConfigDialog.SHOW_BAUDRATE | wxSerialConfigDialog.SHOW_FORMAT | wxSerialConfigDialog.SHOW_FLOW,
                    serial=main_window.serial) as dialog_serial_cfg:
                dialog_serial_cfg.CenterOnParent()
                result = dialog_serial_cfg.ShowModal()
            # open port if not called on startup, open it on startup and OK too
            if result == wx.ID_OK or evt is not None:
                try:
                    main_window.serial.open()
                except serial.SerialException as e:
                    with wx.MessageDialog(self.main_window, str(e), "Serial Port Error", wx.OK | wx.ICON_ERROR)as dlg:
                        dlg.ShowModal()
                        ok = True
                else:
                    dialog_serial_cfg.SetTitle("Serial Terminal on {} [{},{},{},{}{}{}]".format(
                        main_window.serial.portstr,
                        main_window.serial.baudrate,
                        main_window.serial.bytesize,
                        main_window.serial.parity,
                        main_window.serial.stopbits,
                        ' RTS/CTS' if main_window.serial.rtscts else '',
                        ' Xon/Xoff' if main_window.serial.xonxoff else '',
                        ))
                    ok = True
            else:
                # on startup, dialog aborted
                main_window.alive.clear()
                ok = True
        if main_window.serial.isOpen() == True:
            if not my_serial.ConnectSerial(main_window):
                return
            main_window.workspace_tree.ReCreateTree()
            main_window.connected = True
            #TODO: change status Barre
            asyncio.run(SetView(main_window, False))
            put_cmd(main_window, "import os\r\n")
            asyncio.run(SendCmdAsync(main_window, "os.uname()\r\n"))
            self.main_window.serial_manager.get_card_infos(self.main_window.read_cmd("os.uname()"))
            print(self.main_window.serial_manager.card)
            put_cmd(main_window, "\r\n")
            self.main_window.actualize_status_bar()
            treeModel(main_window)
            asyncio.run(SetView(main_window, True))
            speak(main_window, "Device Connected")
            print(self.main_window.serial_manager.card)
    
    def Ondownload(self, evt):
        """Download the file found on the current tab if it was saved

        :param evt: Event to trigger the method
        :type evt: wx.Event
        """  
        main_window = self.main_window
        notebookP = self.main_window.MyNotebook
        page = notebookP.GetCurrentPage()
        if main_window.serial.isOpen()==False:
            main_window.Shell.AppendText('Please open serial')
            return False
        main_window.serial.write('\x03'.encode('utf-8'))
        self.main_window.show_cmd = False
        time.sleep(0.05)

        if page == None:
            main_window.Shell.AppendText('Please choose file or input something')
            return False
        print("dir = %s %s"%(page.directory, page.filename))
        if page.directory[len(page.directory) - 1] == '/':
            pathfile=page.directory + page.filename
        else:
            pathfile=page.directory + '/' + page.filename
        if page.saved == False:
            main_window.Shell.append('Please save the file before download')
            return False
        elif str(pathfile).find(":")>=0:
            main_window.serial_manager.download(pathfile, page.filename)
            time.sleep(1)
            #self.main_window.Shell.Clear()
            self.main_window.Shell.SetValue("Downloaded file : " + page.filename)
            self.main_window.show_cmd = True
            self.main_window.Shell.SetFocus()
            put_cmd(self.main_window, '\r\n')
            return True
    
        return False

    def OnRun(self, evt):
        """Upload the file + run 

        :param evt: Event to trigger the method
        :type evt: wx.Event
        """  
        main_window = self.main_window
        notebookP = self.main_window.MyNotebook
        page = notebookP.GetCurrentPage()
        if main_window.serial.isOpen()==False:
            main_window.Shell.AppendText('Please open serial')
            return False
        main_window.serial.write('\x03'.encode('utf-8'))
        self.main_window.show_cmd = False
        time.sleep(0.05)

        if page == None:
            main_window.Shell.AppendText('Please choose file or input something')
            return False
        print("dir = %s %s"%(page.directory, page.filename))
        if page.saved == False:
            main_window.Shell.append('Please save the file before download')
            return False
        if page.directory[len(page.directory) - 1] == '/':
            pathfile=page.directory + page.filename
        else:
            pathfile=page.directory + '/' + page.filename
        if str(pathfile).find(":")>=0:
            main_window.serial_manager.download(pathfile, page.filename)
            time.sleep(1)
            self.main_window.Shell.SetValue("Downloaded file : " + page.filename)
            self.main_window.Shell.SetFocus()
            self.main_window.show_cmd = True
            self.main_window.serial_manager.download_and_run(page.filename)
            return True
        return False

    def OnDisconnect(self, evt):
        """Close the connection with the device connected

        :param evt: Event to trigger the method
        :type evt: wx.Event
        """
  
        if not self.main_window.serial.ser.isOpen():
            self.main_window.Shell.AppendText("already close.")
            return

        put_cmd(self.main_window, '\x03')
        time.sleep(0.1)
        self.main_window.serial.ser.close()
        self.main_window.connected = False
        self.main_window.statusbar.SetStatusText("Status: Not Connected", 1)
        main_window.FileTree.ReCreateTree()
        self.main_window.Shell.setReadOnly(True)
        speak(self.main_window, "Device Disconnected")

    def OnStop(self, evt):
        """Stop the program on executing

        :param evt: Event to trigger the method
        :type evt: wx.Event
        """  
        if self.main_window.serial.ser.isOpen():
            SendCmdAsync(self.main_window, '\x03')
        else:
            self.main_window.Shell.AppendText("serial not open")
    
    def OnBurnFirmware(self, event):
        main_window = self.main_window
        firmware_manager = main_window.firmware_manager
        ok = False
        while not ok:
            with UpdateFirmwareDialog(main_window, firmware_manager) as dialog_serial_cfg:
                dialog_serial_cfg.CenterOnParent()
                result = dialog_serial_cfg.ShowModal()
            # open port if not called on startup, open it on startup and OK too
            if result == wx.ID_OK or event is not None:
                print(firmware_manager.burn_adress, firmware_manager.port, firmware_manager.bin_path)
                if not firmware_manager.port or not firmware_manager.bin_path :
                    with wx.MessageDialog(self, "", "Incorrect Path or Port", wx.OK | wx.ICON_ERROR)as dlg:
                        dlg.ShowModal()
                        ok = True
                else:    
                        sys.stdout = sys.__stdout__
                        self.main_window_burn = Burnmain_window(main_window)
                        burn_thread = FirmwareThread(main_window, firmware_manager, self.main_window_burn)
                        self.main_window_burn.CenterOnParent()
                        burn_thread.setDaemon(1)
                        burn_thread.start()
                        self.main_window_burn.ShowModal()
                        burn_thread._stop()
                        burn_thread.join()
                        speak(self.main_window, "Firmware installed")
                        self.main_window_burn.txt.Destroy()
                        self.main_window_burn.Destroy()
                        sys.stdout = sys.__stdout__
                        ok = True
            else:
                ok = True

    def OnChangeTheme(self, evt):
        """Change the theme of the main_window and the lexer style

        :param evt: Event to trigger the method
        :type evt: wx.Event
        """  
        menuId = evt.Id
        i = 0
        list = [wx.ID_DARK_THEME, wx.ID_LIGHT_THEME, wx.ID_ASTRO_THEME]
        for x in list:
            if x == menuId:
                print('Theme = ' + str(i))
                break
            i += 1
        
        customize_editor(self.main_window.MyNotebook.GetCurrentPage(), themes[i], py_style)
        self.main_window.Shell.custom_shell(themes[i])
        self.main_window.TreeCtrl.custom_tree_ctrl(themes[i])
        self.main_window.MyNotebook.custom_notebook(themes[i])
        self.main_window.MyNotebook.theme = i

#TODO: Menu Help with shortcuts and link on wiki tuto HTML
# class HelpMenu(wx.Menu):
#     ""

class TopMenu(wx.MenuBar):
    """TopMenu class derivated of wx.MenuBar which contains the Edit and File Menus

    :param wx.MenuBar: Class to derivate
    :type wx.MenuBar: wx.MenuBar see  https://wxpython.org/Phoenix/docs/html/wx.MenuBar.html
    """
    def __init__(self, main_window):
        """Constructor which append the Edit and File Menus on the Menubar and bind related events

        :param main_window: main_window class (in this case MainWindow)
        :type main_window: MainWindow(here Mainwindow class derivated of wx.main_window)
        """
        wx.MenuBar.__init__(self)
        self.main_window = main_window
        self.__set_properties() #:Set properties and variables linked to the class
        self.__attach_events__() #:Bind events relatives to this class

    def __set_properties(self):
        """
        Set properties and define variables of the objet instantiated
        """
        self.MenuFile = FileMenu(self.main_window)
        self.MenuEdit = EditMenu(self.main_window)
        self.MenuTools = ToolsMenu(self.main_window)

        self.Append(self.MenuFile, "&File")
        self.Append(self.MenuEdit, "&Edit")
        self.Append(self.MenuTools, "&Tools")
        
    def __attach_events__(self):
        """
        Bind events with the objet instantiated
        """
        self.Bind(wx.EVT_MENU,  self.MenuFile.OnExit, id=wx.ID_EXIT)
        self.Bind(wx.EVT_MENU,  self.MenuFile.OnOpen, id=wx.ID_OPEN)
        self.Bind(wx.EVT_MENU,  self.MenuFile.OnSaveAs, id=wx.ID_SAVEAS)
        self.Bind(wx.EVT_MENU,  self.MenuFile.OnSave, id=wx.ID_SAVE)
        self.Bind(wx.EVT_MENU,  self.MenuFile.OnAddPage, id=wx.ID_NEW)
        self.Bind(wx.EVT_MENU,  self.MenuFile.OnClosePage, id=wx.ID_CLOSE)
        self.Bind(wx.EVT_MENU,  self.MenuEdit.OnCopy, id=wx.ID_COPY)
        self.Bind(wx.EVT_MENU,  self.MenuEdit.OnPaste, id=wx.ID_PASTE)
        self.Bind(wx.EVT_MENU,  self.MenuEdit.OnCut, id=wx.ID_CUT)
        self.Bind(wx.EVT_MENU,  self.MenuEdit.OnFindReplace, id=wx.ID_FIND)
        self.Bind(wx.EVT_MENU,  self.MenuEdit.OnSyntaxCheck, id=wx.ID_SYNTAX_CHECK)
        self.Bind(wx.EVT_MENU, self.MenuTools.OnPortSettings, id=wx.ID_SETTINGS)
        self.Bind(wx.EVT_MENU, self.MenuTools.Ondownload, id=wx.ID_DOWNLOAD)
        self.Bind(wx.EVT_MENU, self.MenuTools.OnRun, id=wx.ID_EXECUTE)
        self.Bind(wx.EVT_MENU, self.MenuTools.OnStop, id=wx.ID_STOP)
        self.Bind(wx.EVT_MENU, self.MenuTools.OnBurnFirmware, id=wx.ID_BURN_FIRMWARE)
        self.Bind(wx.EVT_MENU,  self.MenuTools.OnChangeTheme, \
         id=wx.ID_LIGHT_THEME)
        self.Bind(wx.EVT_MENU,  self.MenuTools.OnChangeTheme, \
         id=wx.ID_DARK_THEME)
        self.Bind(wx.EVT_MENU,  self.MenuTools.OnChangeTheme, \
         id=wx.ID_ASTRO_THEME)

class ToolBar(wx.ToolBar):
    """A custom class derivated from wx.ToolBar to access quickly on some commands

    :param wx.ToolBar: see https://wxpython.org/Phoenix/docs/html/wx.ToolBar.html
    """    
    def __init__(self, main_window):
        """constructor for ToolBar 

        :param main_window: main_window class generally the main window
        :type main_window: MainWindow (generally)
        """           
        wx.ToolBar.__init__(self, parent=main_window, style= wx.TB_RIGHT | wx.TB_DOCKABLE | wx.FULL_REPAINT_ON_RESIZE)
        self.CentreOnParent()
        self.main_window = main_window
        
        self.add_tools()
        self.__set_properties()
        self.__attach_events(main_window.top_menu)

    def add_tools(self):
        """
        Fill the objet created with tools buttons
        """  
        self.AddTool(wx.ID_NEW, '', load_img('./img/newfile.png'))
        self.AddTool(wx.ID_OPEN, '', load_img('./img/fileopen.png'))
        self.AddTool(wx.ID_SAVE, '', load_img('./img/save.png'))
        self.AddTool(wx.ID_EXECUTE, '', load_img('./img/downloadandrun.png'))
        self.AddTool(wx.ID_STOP, '', load_img('./img/stop.png'))
        self.AddTool(wx.ID_UNDO, '', load_img('./img/undo.png'))
        self.AddTool(wx.ID_REDO, '', load_img('./img/redo.png'))
        self.AddTool(wx.ID_SYNTAX_CHECK, '', load_img('./img/syntaxCheck.png'))
        self.AddTool(wx.ID_CLEAR, '', load_img('./img/clear.png'))

    def __set_properties(self):
        """Set properties and declare variables of the instance
        """  
        self.Realize()
        self.SetBackgroundColour("black")

    def __attach_events(self, top_menu):
        """Bind the events related with this class

        :param main_window: often the MainWindow
        :type main_window: MainWindow class
        """
        self.Bind(wx.EVT_MENU, top_menu.MenuFile.OnAddPage, id=wx.ID_NEW)
        self.Bind(wx.EVT_MENU, top_menu.MenuFile.OnOpen, id=wx.ID_OPEN)
        self.Bind(wx.EVT_MENU, top_menu.MenuFile.OnSave, id=wx.ID_SAVE)
        self.Bind(wx.EVT_MENU, top_menu.MenuTools.OnRun, id=wx.ID_EXECUTE)
        self.Bind(wx.EVT_MENU, top_menu.MenuTools.OnStop, id=wx.ID_STOP)
        self.Bind(wx.EVT_MENU, top_menu.MenuEdit.OnSyntaxCheck, id=wx.ID_SYNTAX_CHECK)
        self.Bind(wx.EVT_MENU, self.OnClear, id=wx.ID_CLEAR)
        self.Bind(wx.EVT_MENU, top_menu.MenuEdit.OnUndo, id=wx.ID_UNDO)
        self.Bind(wx.EVT_MENU, top_menu.MenuEdit.OnRedo, id=wx.ID_REDO)
        
    def OnClear(self, event):
        """Clear the shell panel

        :param evt: Event to trigger the method
        :type evt: wx.Event
        """  
        self.main_window.Shell.Clear()
        speak(self.main_window, "Terminal Cleared")