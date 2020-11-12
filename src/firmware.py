from packages import wx, serial, time, threading, sys
from threading import Thread

import serial.tools.list_ports
import subprocess
import api.api_esptool as Esp
from utilitaries import my_speak

class FirmwareManager():
    """Class which contains parameters to use esptool
    """
    def __init__(self):
        """Basic constructor for FirmwareManager Class
        """
        self.burn_adress = None
        self.port = None
        self.board = None
        self.burn_erase = "yes"
        self.bin_path = None

class ChooseBin(wx.FilePickerCtrl):
    """Class wich manage the selection the selection of the binary to be install on the card
    

    :param wx.FilePickerCtrl: WX Class to derivate
    :type wx.FilepickerCtrl: wx.FilePickerCtrl
    """
    def __init__(self, parent, burn_manager):
        """Basic constructor for ChooseBin class

        :param parent: Parent class
        :type parent: :class:UpdateFirmwareDialog
        :param burn_manager: :class:FirmwareManager to fill 
        :type burn_manager: :class:FirmwareManager
        """
        wx.FilePickerCtrl.__init__(self, parent, message="Select the binary to install", wildcard="*.bin", name="select the binary to install", style=wx.FLP_FILE_MUST_EXIST)

        self.burn_manager = burn_manager
        self.__set_properties()
        self.Bind(wx.EVT_FILEPICKER_CHANGED, self.change_bin_path)
    
    def __set_properties(self):
        """Custom the current class
        """
        self.SetLabelText("Select path of the bin")
    
    def change_bin_path(self, event):
        """Change the binary path by the path selected

        :param event: event which sets off the function
        :type event: wx.EVT_FILE_PICKER_CHANGED
        """
        self.burn_manager.bin_path = self.GetPath()

class UpdateFirmwareDialog(wx.Dialog):
    """
    Dialog to update the firmware or other 
    """
    
    def __init__(self, parent, burn_manager):
        """Basic constructor for UpdateFirmwareDialog class

        :param parent: Parent class
        :type parent: :class:MainWindow
        :param burn_manager: :class:FirmwareManager to fill
        :type burn_manager: :class:FirmwareManager
        """
        wx.Dialog.__init__(self, parent, style=wx.DEFAULT_DIALOG_STYLE)

        self.burn_manager = burn_manager
        self.label_port = wx.StaticText(self, -1, "Port")
        self.choice_port = wx.Choice(self, -1, choices=[])
        self.sizer_1_staticbox = wx.StaticBox(self, -1, "Config")
        self.panel_config = wx.Panel(self, -1)
        self.label_adresses = wx.StaticText(self.panel_config, -1, "Adresses")
        self.choice_adresses = wx.Choice(self.panel_config, -1, choices=["choice 1"])
        self.label_erase_flash = wx.StaticText(self.panel_config, -1, "Erase Flash ?")
        self.choice_erase_flash = wx.Choice(self.panel_config, -1, choices=["choice 1"])
        self.sizer_config_staticbox = wx.StaticBox(self.panel_config, -1, "Data Format")
        self.panel_bin_path = wx.Panel(self, -1)
        self.checkbox_timeout = wx.StaticText(self.panel_bin_path, -1, "Choose your binary")
        self.select_path = ChooseBin(self.panel_bin_path, self.burn_manager)
        self.sizer_binary_staticbox = wx.StaticBox(self.panel_bin_path, -1, "Binary Choice")
        self.button_ok = wx.Button(self, wx.ID_OK, "")
        self.button_cancel = wx.Button(self, wx.ID_CANCEL, "")

        font = wx.Font(pointSize = 10,
                family = wx.FONTFAMILY_DEFAULT,
                style = wx.FONTSTYLE_ITALIC,
                weight = wx.FONTWEIGHT_NORMAL,  
                underline = False,
                faceName ='Fira Code', #Microsoft sans Serif
                encoding = 0)
        self.label_port.SetFont(font)
        self.label_erase_flash.SetFont(font)
        self.label_adresses.SetFont(font)
        
        self.__set_properties()
        self.__do_layout()
        self.__attach_events()

    def __set_properties(self):
        """Custom the current class
         """
        
        self.SetTitle("Update Firmware")
        self.choice_adresses.SetSelection(0)
        self.choice_erase_flash.SetSelection(0)
        self.select_path.Enable(True)
        self.button_ok.SetDefault()

        # fill in ports and select current setting
        preferred_index = 0
        self.choice_port.Clear()
        self.ports = []
        for n, (portname, desc, hwid) in enumerate(sorted(serial.tools.list_ports.comports())):
            self.choice_port.Append(u'{} - {}'.format(portname, desc))
            self.ports.append(portname)
            preferred_index = n
        self.choice_port.SetSelection(preferred_index)

        list_adresses = ["0x1000","0x0",]
        list_erase = ["no","yes"]

        self.choice_adresses.Clear()
        self.choice_erase_flash.Clear()
        index = 0
        for n, adress in enumerate(list_adresses):
            self.choice_adresses.Append(str(adress))
            index = n
        self.choice_adresses.SetSelection(index)

        for n, erase in enumerate(list_erase):
            self.choice_erase_flash.Append(str(erase))
            index = n
        self.choice_erase_flash.SetSelection(index)

    def __do_layout(self):
        """Places the different elements of the current class instance on the window
         """
        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        sizer_3 = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer_binary_staticbox.Lower()
        sizer_binary = wx.StaticBoxSizer(self.sizer_binary_staticbox, wx.HORIZONTAL)
        self.sizer_config_staticbox.Lower()
        sizer_format = wx.StaticBoxSizer(self.sizer_config_staticbox, wx.VERTICAL)
        grid_sizer_1 = wx.FlexGridSizer(3, 2, 0, 0)
        self.sizer_1_staticbox.Lower()
        sizer_1 = wx.StaticBoxSizer(self.sizer_1_staticbox, wx.VERTICAL)
        sizer_config = wx.FlexGridSizer(3, 2, 0, 0)
        sizer_config.Add(self.label_port, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 4)
        sizer_config.Add(self.choice_port, 0, wx.EXPAND, 0)
        sizer_config.AddGrowableCol(1)
        sizer_1.Add(sizer_config, 0, wx.EXPAND, 0)
        sizer_2.Add(sizer_1, 0, wx.EXPAND, 0)
        grid_sizer_1.Add(self.label_adresses, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 4)
        grid_sizer_1.Add(self.choice_adresses, 1, wx.EXPAND | wx.ALIGN_RIGHT, 0)
        grid_sizer_1.Add(self.label_erase_flash, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 4)
        grid_sizer_1.Add(self.choice_erase_flash, 1, wx.EXPAND | wx.ALIGN_RIGHT, 0)
        sizer_format.Add(grid_sizer_1, 1, wx.EXPAND, 0)
        self.panel_config.SetSizer(sizer_format)
        sizer_2.Add(self.panel_config, 0, wx.EXPAND, 0)
        sizer_binary.Add(self.checkbox_timeout, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 4)
        sizer_binary.Add(self.select_path, 0, 0, 0)
        self.panel_bin_path.SetSizer(sizer_binary)
        sizer_2.Add(self.panel_bin_path, 0, wx.EXPAND, 0)
        sizer_3.Add(self.button_ok, 0, 0, 0)
        sizer_3.Add(self.button_cancel, 0, 0, 0)
        sizer_2.Add(sizer_3, 0, wx.ALL | wx.ALIGN_RIGHT, 4)
        self.SetSizer(sizer_2)
        sizer_2.Fit(self)
        self.Layout()
        self.button_ok.SetLabel("Install")
        # end wxGlade

    def __attach_events(self):
        """Attach events on the class instantiated
         """
        
        self.Bind(wx.EVT_BUTTON, self.OnCancel, id=wx.ID_CANCEL)
        self.Bind(wx.EVT_BUTTON, self.OnOK, id=wx.ID_OK)

    def OnOK(self, event):
        """Function to apply when the user click on the OK button

        :param event: event which sets off the function
        :type event: wx.EVT_BUTTON
        """

        success = True
        self.burn_manager.port = self.ports[self.choice_port.GetSelection()]
        self.burn_manager.burn_adress = self.choice_adresses.GetStringSelection()
        self.burn_manager.burn_erase = self.choice_erase_flash.GetStringSelection()
        if success:
            self.EndModal(wx.ID_OK)

    def OnCancel(self, events):
        """Function to apply when the user click on the Cancel button

        :param event: event which sets off the function
        :type event: wx.EVT_BUTTON
        """
        self.EndModal(wx.ID_CANCEL)

class BurnFrame(wx.Dialog):
    """Burn Firware dialog class to update or install the firmware selected on the card

    :param wx: Class to derivate
    :type wx: :class:wx.Dialog
    """
    def __init__(self, parent):
        """Basic constructor to init the class

        :param parent: Parent class 
        :type parent: :class:MainWindow
        """

        wx.Dialog.__init__(self, parent, style=wx.DEFAULT_DIALOG_STYLE)
        self.EnableCloseButton(enable=False)
        self.SetTitle("Burn Firmware Console")
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.txt = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RICH2)
        font = wx.Font(pointSize = 12, family = wx.FONTFAMILY_SWISS, style = wx.FONTSTYLE_SLANT, weight = wx.FONTWEIGHT_NORMAL,  
                      underline = False, faceName ="Fira Code", encoding = 0)
        self.txt.SetFont(font)
        self.txt.SetMaxClientSize(self.txt.GetMaxSize())
        sizer.Add(self.txt, 1, wx.EXPAND | wx.ALL, 0)
        self.SetSizer(sizer)

class FirmwareThread(Thread):
    """Thread to execute esptool command(s)

    :param Thread: Thread class from Python module
    :type Thread: [type]
    """
    def __init__(self, main_window, firmware_manager, console):
        """Constructor to init a instance of :class:FirmwareThread

        :param parent: MainWindow
        :type parent: :class:MainWindow
        :param firmware_manager: Firmware manager 
        :type firmware_manager: :class:FirmwareManager
        :param console: Place where write the output of esptool
        :type console: :class:BurnFrame
        """

        Thread.__init__(self)
        self.main_window = main_window
        self.burn_frame = console
        self.burn_console = console.txt       
        self.board= firmware_manager.board
        self.binpath= firmware_manager.bin_path
        self.com= firmware_manager.port
        self.iserase= firmware_manager.burn_erase
        self.burnaddr= firmware_manager.burn_adress
        self.port = firmware_manager.port
        self.stop_thread = False
    
        if self.burnaddr=="0x0":
            self.burnaddr=0
        else:
            self.burnaddr=0x1000
        
        #print("burn=====board:%s path:%s port:%s adress:%s "% (str(self.board), self.binpath, self.port, self.burnaddr))

    def run(self):
        while True:
            if self.stop_thread:
                break
            if self.iserase=="yes":
                try:
                    my_speak(self.main_window, "Erase Flash Memory")
                    Esp.Burn(self.burn_console, str(self.board),self.binpath,self.port,"yes", self.burnaddr)
                    my_speak(self.main_window, "Memory erased")
                except Exception as e:
                    time.sleep(3)
                    print(e)
                    self.stop_thread = True
                    self.burn_frame.EnableCloseButton(enable=True)
                    my_speak(self.main_window, "Flash Memory Error")
                    return
            try:
                my_speak(self.main_window, "Start Upload Firmware")
                Esp.Burn(self.burn_console, str(self.board),self.binpath,self.port,"no",self.burnaddr)
            except Exception as e:
                print(e)
                self.stop_thread = True
                self.burn_frame.EnableCloseButton(enable=True)
                my_speak(self.main_window, "Firmware Error")
                return
            if self.board=="esp8266":
                Esp.downOkReset()
            self.burn_frame.EnableCloseButton(enable=True)
            my_speak(self.main_window, "Firmware Installed")
            self.stop_thread = True

def burn_firmware(main_window ,event):
    firmware_manager = main_window.firmware_manager
    ok = False
    while not ok:
        with UpdateFirmwareDialog(main_window, firmware_manager) as dialog_serial_cfg:
            dialog_serial_cfg.CenterOnParent()
            result = dialog_serial_cfg.ShowModal()
        # open port if not called on startup, open it on startup and OK too
        if result == wx.ID_OK or event is not None:
            #print(firmware_manager.burn_adress, firmware_manager.port, firmware_manager.bin_path)
            if not firmware_manager.port or not firmware_manager.bin_path :
                with wx.MessageDialog(main_window, "", "Incorrect Path or Port", wx.OK | wx.ICON_ERROR)as dlg:
                    dlg.ShowModal()
                    ok = True
            else:    
                sys.stdout = sys.__stdout__
                main_window_burn = BurnFrame(main_window)
                burn_thread = FirmwareThread(main_window, firmware_manager, main_window_burn)
                main_window_burn.CenterOnParent()
                burn_thread.setDaemon(1)
                burn_thread.start()
                main_window_burn.ShowModal()
                burn_thread._stop()
                burn_thread.join()
                my_speak(main_window, "Firmware installed")
                main_window_burn.txt.Destroy()
                main_window_burn.Destroy()
                sys.stdout = sys.__stdout__
                ok = True
        else:
            ok = True