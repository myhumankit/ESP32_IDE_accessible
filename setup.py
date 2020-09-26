import sys
from cx_Freeze import setup, Executable

pack = ["os",
        "sys",
        "wx",
        "speech",
        "queue",
        "serial",
        "time",
        "codecs",
        "random"]

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": pack, "excludes": ["tkinter","wx.lib.pdfviewer","numpy"]}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "Blind-IDE",
        version = "1.0",
        description = "IDE Micro Python",
        options = {"build_exe": build_exe_options},
        executables = [Executable("./src/main.py", base=base)])