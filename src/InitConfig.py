import wx

class Preferences(wx.Dialog):
    def __init__(self, parent):
        super(Preferences,self).__init__(parent)
        
        self.notebook = wx.Notebook(self)
        self.notebook.AddPage(MySerialPreferences(self.notebook), "Serial", select=True)
        #self.notebook.AddPage(MyConfigPreferences(self), "Config", select=False)

class MySerialPreferences(wx.Panel):
    def __init__(self, parent):
        super(MySerialPreferences,self).__init__(parent)
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        bd = ['100','300','600','1200','2400','4800','9600','14400','19200','38400','56000','57600','115200','128000','256000']
        self.serialBaund=wx.ComboBox(self,choices=bd, name="baudrate")
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        st1 = wx.StaticText(self, label='Baudrate')
        hbox1.Add(st1, 0, 0, 0)
        hbox1.Add(self.serialBaund, 0, 0, 0)

        bytesize = ['5','6','7','8']
        self.serialBytesize=wx.ComboBox(self, name="bytesize", choices=bytesize)
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        st2 = wx.StaticText(self, label='Bytesize')
        hbox2.Add(st2, 0, 0, 0)
        hbox2.Add(self.serialBytesize, 0, 0, 0)
		
        parity = ['NONE','EVEN','ODD','MARK','SPACE']
        self.parityComboBox=wx.ComboBox(self ,name="parity", choices=parity)
        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        st3 = wx.StaticText(self, label='Parity')
        hbox3.Add(st3, 0, 0, 0)
        hbox3.Add(self.parityComboBox, 0, 0, 0)
        
        stopbytes = ['NONE','EVEN','ODD','MARK','SPACE']
        self.stopbitsComboBox=wx.ComboBox(self, name="stopbits", choices=stopbytes)
        hbox4 = wx.BoxSizer(wx.HORIZONTAL)
        st4 = wx.StaticText(self, label='StopBytes')
        hbox4.Add(st4, 0, 0, 0)
        hbox4.Add(self.stopbitsComboBox, 0, 0, 0)
        
        sizer.Add(hbox1, 0, 0, 0)
        sizer.Add(hbox2, 0, 0, 0)
        sizer.Add(hbox3, 0, 0, 0)
        sizer.Add(hbox4, 0, 0, 0)
        self.SetSizer(sizer)