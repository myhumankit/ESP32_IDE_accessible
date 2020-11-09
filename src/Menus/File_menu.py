import wx, os
from all_panels import MyEditor
from Panels.Device_tree import save_on_card

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
        
    def OnExit(self, evt):
        """Quit the app

        :param evt: Event to trigger the method
        :type evt: wx.Event
        """
        self.main_window.serial.close()
        self.main_window.stop_thread_serial()
        self.thread_speak.join()
        self.main_window.DestroyChildren()
        self.main_window.Destroy()

        

    def OnSave(self, evt):
        """Save the current page of the notebook

        :param evt: Event to trigger the method
        :type evt: wx.Event
        """   
        notebookP = self.main_window.notebook
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
        self.main_window.shell.AppendText("Content Saved\n")
        self.main_window.q_speak.put("Content Saved")

    def OnSaveAs(self, evt):
        """Open a wx.filedialog to Save as a file the text of the current editor

        :param evt: Event to trigger the method
        :type evt: wx.Event
        """   
        notebookP = self.main_window.notebook
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
            self.main_window.q_speak.put( "Content Saved")
        dialog.Destroy()

    def OnOpen(self, evt):
            """Open a wx.filedialog to open a file on a editor 

            :param evt: Event to trigger the method
            :type evt: wx.Event
            """  
            notebookP = self.main_window.notebook
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
                    notebookP.GetCurrentPage().SetFocus()
                else:
                    new_tab = MyEditor(notebookP, self.main_window, "", False)
                    new_tab.filename = filename
                    new_tab.directory = directory
                    notebookP.AddPage(new_tab, filename, select = True)
                    notebookP.GetCurrentPage().SetFocus()
                    notebookP.tab_num = notebookP.GetPageCount()
                    wx.CallAfter(new_tab.SetFocus)
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
        notebookP = self.main_window.notebook
        notebookP.tab_num = notebookP.GetPageCount()
        #RAJOUTER une variable on_card and Value
        new_tab = MyEditor(self.main_window.notebook, self.main_window, "", False)
        notebookP.AddPage(new_tab, "Tab %s" % new_tab.id, select=True)
        notebookP.GetCurrentPage().SetFocus()
        #print(new_tab.id)

    def OnClosePage(self, evt):
        """Close the current page and update id order

        :param evt: Event to trigger the method
        :type evt: wx.Event
        """  
        #TODO: ajouter dialogue pour sauvegarder si pas saved
        
        notebook = self.main_window.notebook
        page = notebook.GetCurrentPage()
        if page:
            notebook.DeletePage(page.id - 1)
            notebook.tab_num = notebook.GetPageCount()

        nb_pg = notebook.tab_num
        i = 1
        while i <= nb_pg:
            page_to_update = notebook.GetPage(i - 1)
            page_to_update.id = i
            i += 1
