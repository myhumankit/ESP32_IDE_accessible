import wx
import json
import wx.lib.agw.flatnotebook as fnb

from Panels.Editor import Styled_Editor


class NotebookPanel(fnb.FlatNotebook):
    """Customized Notebook class

    :param fnb.FlatNotebook: A class of notebook to derivate
    :type fnb.FlatNotebook: wx.lib.agw.flatnotebook.FlatNotebook
    """

    def __init__(self, parent, topwindow):
        """ constructor to create a notebook multi-tabs

        :param parent: Splitter window (unused in methods, just to init)
        :type parent: wx.SplitterWindow
        :param topwindow: MainWindow to use her attibuts
        :type parent: MainWindow class

        """
        style = fnb.FNB_FF2 | \
                wx.FULL_REPAINT_ON_RESIZE | \
                fnb.FNB_BACKGROUND_GRADIENT
        fnb.FlatNotebook.__init__(self,
                                  parent=parent, style=style, name="COUCOU")

        self.SetGradientColours(wx.BLACK, wx.WHITE, wx.BLACK)
        self.SetAGWWindowStyleFlag(
            fnb.FNB_X_ON_TAB | fnb.FNB_DROPDOWN_TABS_LIST | fnb.FNB_RIBBON_TABS)
        self.__set_properties(parent, topwindow)
        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(fnb.EVT_FLATNOTEBOOK_PAGE_CHANGED, self.set_focus_editor)
        self.Bind(fnb.EVT_FLATNOTEBOOK_PAGE_CHANGING, self.set_focus_editor)
        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.set_focus_editor)
        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGING, self.set_focus_editor)
        self.custom_notebook("Dark Theme")

    def on_paint(self, event):
        """Paint a gradient color on the Notebook background

        :param event: Event to repaint the notebook background
        :type event: wx.Event
        """
        x = 0
        y = 0
        w, h = self.GetSize()
        try:
            self.dc = wx.PaintDC(self)
            file = open('./customize.json')
            theme = json.load(file)
            theme = theme[self.theme_choice]
            file.close()
            self.dc.GradientFillLinear((x, y, w, h),
                                       theme['Panels Colors']['Background notebook gradient 2'],
                                       theme['Panels Colors']['Background notebook gradient 1'])
        except Exception as e:
            print("Can't custom notebook background :", e)

    def __set_properties(self, parent, topwindow):
        """Set the properties and declare the variables of the instance

        :param parent: Splitter window (unused)
        :type parent: wx.SplitterWindow
        :param topwindow: the MainWindow in this case
        :type parent: MainWindow class
        """

        self.parent = parent
        self.topwindow = topwindow
        self.tab_num = 0
        self.data = ""
        self.dlg = None
        self.theme_choice = 'Dark Theme'
        self.colorized = True

    def custom_notebook(self, theme):
        """Custom the Notebook according to the theme passed on args

        :param theme: The theme to apply
        :type theme: list
        """
        try:
            file = open("./customize.json")
            theme = json.load(file)
            file.close()
            theme = theme['Dark Theme']['Panels Colors']
            self.SetTabAreaColour("#D3D3D3")  # FIXME: ADD TAB TO JSON
            self.SetActiveTabColour(theme['Background active tab area'])
            # self.SetTabAreaColour(theme['Background tab area'])
            self.SetActiveTabTextColour(theme['Active tab text'])
            self.SetNonActiveTabTextColour(theme['Active tab text'])
        except Exception:
            print("Can't Customize Notebook")

    def set_focus_editor(self, evt):
        try:
            page = self.GetCurrentPage()
            page = self.GetTabArea()
            page.SetFocus()
        except Exception as e:
            print(e)

    def new_page(self, filename, path, text, on_card):
        new_tab = Styled_Editor(self, self.topwindow, text, on_card)
        new_tab.filename = filename
        new_tab.directory = path
        new_tab = self.AddPage(new_tab, "%s" % filename, select=True)
        self.tab_num = self.GetPageCount()
        self.GetCurrentPage().SetFocus()
