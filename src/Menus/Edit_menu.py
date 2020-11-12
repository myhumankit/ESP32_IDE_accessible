import wx, sys
from constantes import *
from api.api_pyflakes import main as CheckPySyntax
from utilitaries import my_speak

class EditMenu(wx.Menu):
    """Inits a instance of a wx.Menu to create a Theme menu and his buttons (Copy, Paste, Find,...)

    :return: the Theme menu filled by buttons
    :rtype: wx.Menu see https://wxpython.org/Phoenix/docs/html/wx.Menu.html
    """
    def __init__(self, main_window):
        wx.Menu.__init__(self, "Edit")

        self.main_window = main_window
        self.item_list = []
        self.Append(wx.ID_COPY, "&Copy\tCTRL+C")
        self.Append(wx.ID_CUT, "&Cut\tCTRL+X")
        self.Append(wx.ID_PASTE, "&Paste\tCTRL+V")
        self.Append(wx.ID_REDO, "&Undo\tCTRL+Z")
        self.Append(wx.ID_UNDO, "&Redo\tCTRL+Y")
        self.Append(wx.ID_SYNTAX_CHECK, "&Syntax Check")
        self.Append(wx.ID_FIND, "&Find and/or Replace\tCTRL+F")
    
    def OnCopy(self, evt):
        """Copy the selection on the clipboard

        :param evt: Event to trigger the method
        :type evt: wx.Event
        """  
        self.main_window.notebook.GetCurrentPage().Copy()

    def OnPaste(self, evt):
        """Paste the content of the clipboard

        :param evt: Event to trigger the method
        :type evt: wx.Event
        """  
        self.main_window.notebook.GetCurrentPage().Paste()

    def OnCut(self, evt):
        """Cut the selection on the clipboard

        :param evt: Event to trigger the method
        :type evt: wx.Event
        """  
        self.main_window.notebook.GetCurrentPage().Cut()

    def OnRedo(self, evt):
        """Redo

        :param evt: Event to trigger the method
        :type evt: wx.Event
        """  
        self.main_window.notebook.GetCurrentPage().Redo()

    def OnUndo(self, evt):
        """Undo

        :param evt: Event to trigger the method
        :type evt: wx.Event
        """  
        self.main_window.notebook.GetCurrentPage().Undo()

    def OnFindReplace(self, evt):
        """Open a wx.FindReplaceDialog to find and/, replace text in the current editor

        :param evt: Event to trigger the method
        :type evt: wx.Event
        """  
        notebookP = self.main_window.notebook
        page = notebookP.GetCurrentPage()
        if page == None:
            return
        page.OnShowFindReplace()
   
    def OnSyntaxCheck(self, evt):
        """Check the python syntax on the current Tab

        :param evt: Event to trigger the method
        :type evt: wx.Event
        """  
        page = self.main_window.notebook.GetCurrentPage()
        
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
            my_speak(self.main_window, "No Error Detected !")
            pass
        else:
            my_speak(self.main_window, "Some Errors or Warnings Detected, check")
            if stdout!="":
                stdout=stdout.split("\n")
                for i in stdout:
                    if i=="":
                        continue
                    if i.find("syntaxCheck.py")>0:
                        i=i[len(syntaxCheckFilePath):]
                    appendMsg=appendMsg + i + "\n"
                self.main_window.shell.AppendText(appendMsg)
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
                self.main_window.shell.AppendText(appendMsg)
        self.main_window.shell.AppendText("Syntax terminated.\n")