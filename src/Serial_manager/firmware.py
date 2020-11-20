from threading import Thread
from Utils.voice_synthese import my_speak
from Panels.wx_burn_firmware import BurnFrame, UpdateFirmwareDialog

import api.api_esptool as Esp
import wx
import time
import sys


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


class FirmwareThread(Thread):
    """Thread to execute esptool command(s)

    :param Thread: Thread class from Python module
    :type Thread: [type]
    """
    def __init__(self, frame, firmware_manager, console):
        """Constructor to init a instance of :class:FirmwareThread

        :param parent: MainWindow
        :type parent: :class:MainWindow
        :param firmware_manager: Firmware manager
        :type firmware_manager: :class:FirmwareManager
        :param console: Place where write the output of esptool
        :type console: :class:BurnFrame
        """

        Thread.__init__(self)
        self.__set_properties(frame, console, firmware_manager)

        if self.burnaddr == "0x0":
            self.burnaddr = 0
        else:
            self.burnaddr = 0x1000

    def __set_properties(self, frame, console, firmware_manager):
        self.frame = frame
        self.burn_frame = console
        self.burn_console = console.txt
        self.board = firmware_manager.board
        self.binpath = firmware_manager.bin_path
        self.com = firmware_manager.port
        self.iserase = firmware_manager.burn_erase
        self.burnaddr = firmware_manager.burn_adress
        self.port = firmware_manager.port
        self.stop_thread = False

    def run(self):
        while True:
            if self.stop_thread:
                break
            if self.iserase == "yes":
                try:
                    my_speak(self.frame, "Erase Flash Memory")
                    Esp.Burn(self.burn_console,
                             str(self.board), self.binpath, self.port,
                             "yes", self.burnaddr)
                    my_speak(self.frame, "Memory erased")
                except Exception as e:
                    time.sleep(3)
                    print(e)
                    self.stop_thread = True
                    self.burn_frame.EnableCloseButton(enable=True)
                    my_speak(self.frame, "Flash Memory Error")
                    break
            try:
                my_speak(self.frame, "Start Upload Firmware")
                Esp.Burn(self.burn_console, str(self.board), self.binpath,
                         self.port, "no", self.burnaddr)
            except Exception as e:
                print(e)
                self.stop_thread = True
                self.burn_frame.EnableCloseButton(enable=True)
                my_speak(self.frame, "Firmware Error")
                break
            if self.board == "esp8266":
                Esp.downOkReset()
            self.burn_frame.EnableCloseButton(enable=True)
            my_speak(self.frame, "Firmware Installed")
            self.stop_thread = True
            break


def burn_firmware(frame, event):
    firmware_manager = frame.firmware_manager
    ok = False
    while not ok:
        with UpdateFirmwareDialog(frame,
                                  firmware_manager) as dialog_serial_cfg:
            dialog_serial_cfg.CenterOnParent()
            result = dialog_serial_cfg.ShowModal()
        # open port if not called on startup, open it on startup and OK too
        if result == wx.ID_OK:
            try:
                if not firmware_manager.port or not firmware_manager.bin_path:
                    raise Exception
                sys.stdout = sys.__stdout__
                frame_burn = BurnFrame(frame)
                burn_thread = FirmwareThread(frame, firmware_manager,
                                             frame_burn)
                frame_burn.CenterOnParent()
                burn_thread.setDaemon(1)
                burn_thread.start()
                frame_burn.ShowModal()
                burn_thread.join()
                burn_thread = None
                my_speak(frame, "Firmware installed")
                frame_burn.txt.Destroy()
                frame_burn.Destroy()
                sys.stdout = sys.__stdout__
                ok = True
            except Exception:
                with wx.MessageDialog(frame, "Incorrect Path or Port", "Error",
                                      wx.OK | wx.ICON_ERROR)as dlg:
                    dlg.ShowModal()
                    ok = True
        else:
            ok = True
