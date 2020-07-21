import wx
import wx.lib.agw.flatnotebook as fnb


class MyFrame(wx.Frame):

    def __init__(self, parent):

        wx.Frame.__init__(self, None, -1, "FlatNotebook Demo")

        panel = wx.Panel(self)

        notebook = fnb.FlatNotebook(panel, -1)

        for i in range(3):
            caption = "Page %d"%(i+1)
            notebook.AddPage(self.CreatePage(notebook, caption), caption)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(notebook, 1, wx.ALL | wx.EXPAND, 5)
        panel.SetSizer(sizer)


    def CreatePage(self, notebook, caption):
        '''
        Creates a simple :class:`Panel` containing a :class:`TextCtrl`.

        :param `notebook`: an instance of `FlatNotebook`;
        :param `caption`: a simple label.
        '''

        p = wx.Panel(notebook)
        wx.StaticText(p, -1, caption, (20,20))
        wx.TextCtrl(p, -1, "", (20,40), (150,-1))
        return p


# our normal wxApp-derived class, as usual

app = wx.App(0)

frame = MyFrame(None)
app.SetTopWindow(frame)
frame.Show()

app.MainLoop()