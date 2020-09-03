


def find_replace(self, event=None):
    """Find and Replace dialog and action."""
    if self.app.children:
    #find string
        findStr = self.app.childActive.source.GetSelectedText()
        if findStr and self.findDialog:
            self.findDialog.Destroy()
            self.findDialog = None
            #dialog already open, if yes give focus
        if self.findDialog:
            self.findDialog.Show(1)
            self.findDialog.Raise()
            return
        if not findStr:
            findStr = self.findStr
        self.numberMessages=0
        #find data
        data    = wx.FindReplaceData(self.findFlags)
        data.SetFindString(findStr)
        data.SetReplaceString(self.replaceStr)
        #dialog
        self.findDialog = wx.FindReplaceDialog(self, data, "Find & Replace",
        wx.FR_REPLACEDIALOG|wx.FR_NOUPDOWN)
        x, y    = self.frame.GetPosition()
        self.findDialog.SetPosition((x+5,y+200))
        self.findDialog.Show(1)
        self.findDialog.Raise()
        self.findDialog.data = data  # save a reference to it...