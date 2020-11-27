"""
    Module wich contains the functions used to receive infos from the device connected
"""
import wx


def GetCmdReturn(shell_text, cmd):
    """Return the result of a command launched in MicroPython

    :param shell_text: The text catched on the shell panel
    :type shell_text: str
    :param cmd: The cmd return asked
    :type cmd: str
    :return: the return of the command searched
    :rtype: str
    """
    if cmd == "":
        return "clean"
    try:
        return_cmd = shell_text.split(cmd)
        return_cmd = return_cmd[len(return_cmd) - 1]
        return_cmd = return_cmd[:-4]
    except Exception:
        print("Error command back: |" + shell_text + "|")
        return "err"
    return return_cmd


def serial_read_data(frame, data):
    """Handle input from the serial port."""
    msg = frame.keypressmsg
    if data == b'':
        return
    txt = data.decode('UTF-8', 'ignore')
    if msg == "\x08":
        frame.keypressmsg = "debug"
        return frame.shell.remove_char()
    elif msg == "\x1b\x5b\x44":
        return frame.shell.move_key_left()
    elif msg == "\x1b\x5b\x43":
        return frame.shell.move_key_right()
    elif frame.keypressmsg == "debug":
        frame.keypressmsg = "else"
        return
    frame.shell_text += txt
    frame.last_cmd_red += txt
    if frame.show_cmd:
        try:
            print_device_data(frame, txt)
        except Exception as e:
            print(e)


def print_device_data(frame, txt):
    """[summary]

    :param frame: [description]
    :type frame: [type]
    :param txt: [description]
    :type txt: [type]
    :return: [description]
    :rtype: [type]
    """
    wx.CallAfter(frame.shell.WriteText, txt)
    if frame.last_enter:
        frame.cmd_return += txt
    if txt.find(">>>") >= 0:
        frame.cmd_return = ""
        frame.last_enter = False
    if not frame.on_key:
        frame.on_key = True
        frame.last_enter = True


def read_cmd(frame, data):
    """Get the return of the cmd sent to the MicroPython card

    :param data: The commande sent
    :type data: str
    :return: the return of the command sent
    :rtype: str
    """
    b = frame.serial.read(frame.serial.in_waiting)
    frame.is_data = False
    if b:
        frame.is_data = True
        b = b.replace(b'\r\n', b'\n')
        serial_read_data(frame, b)
    frame.result = GetCmdReturn(frame.last_cmd_red, data)
