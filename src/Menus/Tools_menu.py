from packages import wx, serial, wxSerialConfigDialog, asyncio, time
from Panels.Device_tree import treeModel
from firmware import burn_firmware
from editor_style import change_theme_choice, customize_editor
from utilitaries import put_cmd, SendCmdAsync, my_speak
import my_serial

class ToolsMenu(wx.Menu):
    """Class to create a Tools menu and his buttons (Copy, Paste, Find,...)

    :param: Class to derivate
    :type: wx.Menu see https://wxpython.org/Phoenix/docs/html/wx.Menu.html
    """
    def __init__(self, main_window):
        wx.Menu.__init__(self, "Tools")

        self.main_window = main_window
        self.themes_submenu = ThemesMenu(main_window)

        self.Append(wx.ID_SETTINGS, "Connection Settings\tF2")
        self.Append(wx.ID_DOWNLOAD, "Upload")
        self.Append(wx.ID_EXECUTE, "UploadandRun\tF5")
        self.Append(wx.ID_STOP, "Stop")
        self.Append(wx.ID_BURN_FIRMWARE, "BurnFirmware\tF7")
        self.Append(wx.ID_BOARD, "Themes", self.themes_submenu)
        self.Append(wx.ID_CANCEL, "Close Connection")

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
            main_window.connected = True
            #TODO: Découper la fonction
            try:
                main_window.show_cmd = False
                put_cmd(main_window, "import os\r\n")
                main_window.exec_cmd("os.uname()\r\n")
                main_window.serial_manager.get_card_infos(main_window.result)
                main_window.actualize_status_bar()
                treeModel(main_window)
                my_speak(main_window, "Device connected")
                main_window.show_cmd = True
                #my_speak(self.main_window, "Device Connected")
            except Exception as e:
                print(e)
                self.main_window.speak_on = "Connection Error Retry"
                main_window.serial.close()
                main_window.shell.Clear()
    
    def Ondownload(self, evt):
        """Download the file found on the current tab if it was saved

        :param evt: Event to trigger the method
        :type evt: wx.Event
        """  
        main_window = self.main_window
        notebookP = self.main_window.notebook
        page = notebookP.GetCurrentPage()
        if main_window.serial.isOpen()==False:
            main_window.shell.AppendText('Please open serial')
            return False
        main_window.serial.write('\x03'.encode('utf-8'))
        self.main_window.show_cmd = False
        time.sleep(0.05)

        if page == None:
            main_window.shell.AppendText('Please choose file or input something')
            return False
        #print("dir = %s %s"%(page.directory, page.filename))
        if page.directory[len(page.directory) - 1] == '/':
            pathfile=page.directory + page.filename
        else:
            pathfile=page.directory + '/' + page.filename
        if page.saved == False:
            main_window.shell.append('Please save the file before download')
            return False
        elif str(pathfile).find(":")>=0:
            main_window.serial_manager.download(pathfile, page.filename)
            time.sleep(1)
            #self.main_window.shell.Clear()
            self.main_window.shell.SetValue("Downloaded file : " + page.filename)
            self.main_window.show_cmd = True
            self.main_window.shell.SetFocus()
            put_cmd(self.main_window, '\r\n')
            return True
    
        return False

    def OnRun(self, evt):
        """Upload the file + run 

        :param evt: Event to trigger the method
        :type evt: wx.Event
        """  
        main_window = self.main_window
        notebookP = self.main_window.notebook
        page = notebookP.GetCurrentPage()
        if main_window.serial.isOpen()==False:
            main_window.shell.AppendText('Please open serial')
            return False
        main_window.serial.write('\x03'.encode('utf-8'))
        self.main_window.show_cmd = False
        time.sleep(0.05)

        if page == None:
            main_window.shell.AppendText('Please choose file or input something')
            return False
        #print("dir = %s %s"%(page.directory, page.filename))
        if page.saved == False:
            main_window.shell.AppendText('Please save the file before download')
            return False
        if page.directory[len(page.directory) - 1] == '/':
            pathfile=page.directory + page.filename
        else:
            pathfile=page.directory + '/' + page.filename
        if str(pathfile).find(":")>=0:
            main_window.serial_manager.download(pathfile, page.filename)
            time.sleep(1)
            self.main_window.shell.SetValue("Downloaded file : " + page.filename)
            self.main_window.shell.SetFocus()
            self.main_window.show_cmd = True
            self.main_window.serial_manager.download_and_run(page.filename)
            return True
        return False

    def OnDisconnect(self, evt):
        """Close the connection with the device connected

        :param evt: Event to trigger the method
        :type evt: wx.Event
        """
  
        if not self.main_window.serial.isOpen():
            self.main_window.shell.AppendText("already close.")
            return

        put_cmd(self.main_window, '\x03')
        time.sleep(0.1)
        self.main_window.serial.close()
        self.main_window.connected = False
        self.main_window.stop_thread_serial()
        self.main_window.statusbar.SetStatusText("Status: Not Connected", 1)
        self.main_window.device_tree.DeleteChildren(self.main_window.device_tree.device)
        self.main_window.shell.Clear()
        self.main_window.shell.SetEditable(False)
        self.main_window.speak_on = "Device Disconnected"

    def OnStop(self, evt):
        """Stop the program on executing

        :param evt: Event to trigger the method
        :type evt: wx.Event
        """  
        if self.main_window.serial.ser.isOpen():
            self.main_window.exec_cmd(  '\x03')
        else:
            self.main_window.shell.AppendText("serial not open")
    
    def OnBurnFirmware(self, event):
        main_window = self.main_window
        burn_firmware(self.main_window, event)

    def OnChangeTheme(self, evt):
        """Change the theme of the main_window and the lexer style

        :param evt: Event to trigger the method
        :type evt: wx.Event
        """  
        if evt.Id == wx.ID_DARK_THEME:
            theme_name = 'Dark Theme'
        else:
            theme_name = 'Light Theme'
        try:
            change_theme_choice(self.main_window, theme_name)
            page = self.main_window.notebook.GetCurrentPage()
            if page:
                customize_editor(page, theme_name)
            self.main_window.shell.custom_shell(theme_name)
            self.main_window.device_tree.custom_tree_ctrl()
            self.main_window.notebook.custom_notebook(theme_name)
        except Exception as e:
            print(e)

class ThemesMenu(wx.Menu):
    """Inits a instance of a wx.Menu to create a Theme menu and his buttons (Copy, Paste, Find,...)

    :return: the Theme menu filled by buttons
    :rtype: wx.Menu see https://wxpython.org/Phoenix/docs/html/wx.Menu.html
    """
    def __init__(self, main_window):
        wx.Menu.__init__(self, "")
        
        self.Append(wx.ID_DARK_THEME, "&Dark")
        self.Append(wx.ID_LIGHT_THEME, "&Light")
