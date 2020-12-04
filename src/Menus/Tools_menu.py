"""
    Module wich contains the ToolsMenu class and some functions linked to this menu
"""

import wx
import time
from Panels import wxSerialConfigDialog
from Panels.Device_tree import treeModel
from Serial_manager.firmware import burn_firmware
from editor_style import change_theme_choice, customize_editor
from editor_style import activate_highlighted_syntax
from Utils.voice_synthese import my_speak
from Serial_manager.send_infos import put_cmd
from Serial_manager.connexion import ConnectSerial
from Panels.Device_tree import save_on_card


class ToolsMenu(wx.Menu):
    """Class to create a Tools menu and his buttons (Copy, Paste, Find,...)

    :param: Class to derivate
    :type: wx.Menu see https://wxpython.org/Phoenix/docs/html/wx.Menu.html
    """

    def __init__(self, frame):
        """ Constructor method

         :param frame: main window
         :type frame: MainWindow
         """
        wx.Menu.__init__(self, "Tools")

        self.frame = frame
        self.themes_submenu = ThemesMenu(frame)

        self.Append(wx.ID_SETTINGS, "Connection Settings\tF2")
        self.Append(wx.ID_CANCEL, "Close Connection\tF3")
        self.Append(wx.ID_DOWNLOAD, "Upload\tF4")
        self.Append(wx.ID_EXECUTE, "UploadandRun\tF5")
        self.Append(wx.ID_STOP, "&Stop\tCTRL+C")
        self.Append(wx.ID_BURN_FIRMWARE, "BurnFirmware\tF7")
        self.Append(wx.ID_BOARD, "Themes", self.themes_submenu)

    def OnPortSettings(self, evt):
        """
        Show the port settings dialog. The reader thread is stopped for the
        settings change.

        :param evt: Event to trigger the method
        :type evt: wx.Event
        """
        ok = False
        frame = self.frame
        while not ok:
            with wxSerialConfigDialog.SerialConfigDialog(
                    self.frame,
                    -1,
                    "",
                    show=wxSerialConfigDialog.SHOW_BAUDRATE |
                    wxSerialConfigDialog.SHOW_FORMAT |
                    wxSerialConfigDialog.SHOW_FLOW,
                    serial=frame.serial) as dialog_serial_cfg:
                dialog_serial_cfg.CenterOnParent()
                result = dialog_serial_cfg.ShowModal()
            # open port if not called on startup, open it on startup and OK too
            if result == wx.ID_OK:
                try:
                    frame.serial.open()
                    ok = True
                except Exception as e:
                    with wx.MessageDialog(self.frame, str(e),
                                          "Serial Port Error",
                                          wx.OK | wx.ICON_ERROR) as dlg:
                        dlg.ShowModal()
                        ok = True
                    return
            else:
                # on startup, dialog aborted
                frame.alive.clear()
                ok = True
        if frame.serial.isOpen() is True:
            if ConnectSerial(frame) is False:
                return
            frame.connected = True
            # TODO: Découper la fonction
            try:
                frame.start_thread_serial()
                frame.show_cmd = False
                frame.exec_cmd("import os\r\n")
                frame.exec_cmd("os.uname()\r\n")
                if frame.result.find("upgrade") >= 0:
                    frame.serial.close()
                    frame.shell.Clear()
                    frame.shell.WriteText("Device memory corrupted:Upgrade your device with F7")
                    return
                frame.serial_manager.get_card_infos(frame.result)
                frame.actualize_status_bar()
                treeModel(frame)
                my_speak(frame, "Device connected")
                frame.show_cmd = True
                wx.CallAfter(frame.shell.Clear)
                put_cmd(frame, "\r\n")
            except Exception as e:
                print(e)
                self.frame.speak_on = "Connection Error Retry"
                wx.CallAfter(frame.shell.Clear)

    def Ondownload(self, evt):
        """Download the file found on the current tab if it was saved

        :param evt: Event to trigger the method
        :type evt: wx.Event
        """
        frame = self.frame
        frame.shell_text = ""
        notebookP = self.frame.notebook
        page = notebookP.GetCurrentPage()

        if frame.serial.isOpen() is False:
            frame.shell.AppendText('Please open serial')
            return False
        frame.serial.write('\x03'.encode('utf-8'))
        self.frame.show_cmd = False
        if not page:
            frame.shell.AppendText('Please choose file or input something')
            return False
        if page.on_card is True:
            frame.shell.AppendText('Please choose file or input something')
        try:
            if page.directory[len(page.directory) - 1] == '/':
                pathfile = page.directory + page.filename
            else:
                pathfile = page.directory + '/' + page.filename
            if page.saved is False:
                frame.shell.append('Please save the file before download')
                return False
            elif str(pathfile).find(":") >= 0:
                frame.serial_manager.download(pathfile, page.filename)
                self.frame.shell.Clear()
                self.frame.shell.WriteText("Downloaded file : " + page.filename)
                wx.CallAfter(my_speak, self.frame, "Uploaded")
                self.frame.show_cmd = True
                self.frame.shell.SetFocus()
                put_cmd(self.frame, '\r\n')
                return True
            return False
        except Exception as e:
            print("Error: ", e)
            # TODO: finir le upload du tab
            create_new_file(frame)

    def OnRun(self, evt):
        """Upload the file + run

        :param evt: Event to trigger the method
        :type evt: wx.Event
        """
        frame = self.frame
        notebookP = self.frame.notebook
        page = notebookP.GetCurrentPage()
        if frame.serial.isOpen() is False:
            frame.shell.AppendText('Please open serial')
            return False
        frame.serial.write('\x03'.encode('utf-8'))
        time.sleep(0.05)

        if page is None:
            frame.shell.AppendText('Please choose file or input something')
            return False
        # print("dir = %s %s"%(page.directory, page.filename))
        if page.saved is False:
            frame.shell.AppendText('Please save the file before download')
            return False

        self.frame.show_cmd = False
        if page.directory[len(page.directory) - 1] == '/':
            pathfile = page.directory + page.filename
        else:
            pathfile = page.directory + '/' + page.filename
        if str(pathfile).find(":") >= 0:
            frame.serial_manager.download(pathfile, page.filename)
            time.sleep(1)
            self.frame.shell.WriteText("Downloaded file : " + page.filename)
            self.frame.shell.SetFocus()
            self.frame.show_cmd = True
            self.frame.serial_manager.download_and_run(page.filename)
            return True
        return False

    def OnDisconnect(self, evt):
        """Close the connection with the device connected

        :param evt: Event to trigger the method
        :type evt: wx.Event
        """

        if not self.frame.serial.isOpen():
            self.frame.shell.AppendText("already close.")
            return

        put_cmd(self.frame, '\x03')
        time.sleep(0.1)
        self.frame.serial.close()
        self.frame.connected = False
        self.frame.stop_thread_serial()
        self.frame.statusbar.SetStatusText("Status: Not Connected", 1)
        self.frame.device_tree.DeleteChildren(self.frame.device_tree.device)
        self.frame.shell.Clear()
        self.frame.shell.SetEditable(False)
        my_speak(self.frame, "Device Disconnected")

    def OnStop(self, evt):
        """Stop the program on executing

        :param evt: Event to trigger the method
        :type evt: wx.Event
        """
        if self.frame.serial.isOpen():
            put_cmd(self.frame, '\x03')
        else:
            self.frame.shell.AppendText("serial not open")

    def OnBurnFirmware(self, event):
        """Call :function: SerialManager.burn_firmware

        :param event: event
        """
        burn_firmware(self.frame, event)


class ThemesMenu(wx.Menu):
    """Inits a instance of a wx.Menu to create a Theme menu and his buttons (Copy, Paste, Find,...)

    :return: the Theme menu filled by buttons
    :rtype: wx.Menu see https://wxpython.org/Phoenix/docs/html/wx.Menu.html
    """

    def __init__(self, frame):
        """ Constructor method

        :param frame: main window
        :type frame: MainWindow
        """
        wx.Menu.__init__(self, "")

        self.frame = frame
        self.Append(wx.ID_DARK_THEME, "&Dark")
        self.Append(wx.ID_LIGHT_THEME, "&Light")
        self.syntax_on_item = self.Append(wx.ID_NVDA_THEME,
                                          "&Syntax Highlight Enabled")

    def OnChangeTheme(self, evt):
        """Change the theme of the frame and the lexer style

        :param evt: Event to trigger the method
        :type evt: wx.Event
        """

        if evt.Id == wx.ID_DARK_THEME:
            theme_name = 'Dark Theme'
        elif evt.Id == wx.ID_LIGHT_THEME:
            theme_name = 'Light Theme'
        else:
            return activate_highlighted_syntax(
                self.frame.notebook,
                self)
        try:
            change_theme_choice(self.frame, theme_name)
            page = self.frame.notebook.GetCurrentPage()
            if page:
                customize_editor(page, theme_name)
            self.frame.shell.custom_shell(theme_name)
            self.frame.device_tree.custom_tree_ctrl()
            self.frame.notebook.custom_notebook(theme_name)
        except Exception as e:
            print(e)

# TODO: deplacer cette fonction à un autre endroit


def create_new_file(frame):
    """ Create a new file on the card

        :param frame: main window
        :type frame: MainWindow
    """
    ok = False
    txt = "Select the name of the new file"
    frame.exec_cmd("\r\n")
    frame.show_cmd = False
    while not ok:
        with wx.TextEntryDialog(frame, txt) as dlg:
            dlg.CenterOnParent()
            result = dlg.ShowModal()
            if result == wx.ID_OK:
                path = "./" + dlg.GetValue()
                frame.exec_cmd("myfile = open('%s', 'w')\r\n" % path)
                frame.exec_cmd("myfile.close()\r\n")
                page = frame.notebook.GetCurrentPage()
                page.directory = path
                page.filename = dlg.GetValue()
                save_on_card(frame, page)
                treeModel(frame)
                ok = True
            else:
                ok = True
    frame.show_cmd = True

