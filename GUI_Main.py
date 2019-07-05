"""
DDR_Plotting_Tool Application -- GUI_Main.py
File Created: 2019/01/22
Desc: File contains main plotting window object of the gui (child of wx.frame). Object contains menubar, and the
corresponding handlers for menubar. Creates Graphing Panel object for the main display. Will eventually have logic to
create more (hide all but one Graphing_Panel) if decide to implement multiple pages of graphs.
Author: Ryan Vreeland
"""
import wx
import Data_Handler
from GUI.Time_Plot_Window import TimePlotWindow
from GUI.Difference_Plot_Window import DifferencePlotWindow
import pandas
from GUI.Graphing_Panel import GraphingPanel

class MainWindow(wx.Frame):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self._create_menubar()
        self.graphingPanelOne = GraphingPanel(parent=self) #for right now it is going to be just one, but in the future
        #to impliment being able to have multiple 'pages' of graphs going
        self.SetBackgroundColour(self.graphingPanelOne.GetBackgroundColour())
        self.mainWindowSizer = wx.BoxSizer(wx.VERTICAL)
        self.mainWindowSizer.Add(self.graphingPanelOne, border=10, proportion=1, flag=wx.ALL | wx.EXPAND)
        self.SetSizer(self.mainWindowSizer)

    #GUI Initializing related methods
    def _create_menubar(self):
        """
        Creates menubar, and bindings for menu items
        :return:
        """
        """ Status Bar """
        self.CreateStatusBar()
        self.SetStatusText("Welcome to wxPython!")

        """ Creating Top Menu """
        filemenu = wx.Menu()
        plotmenu = wx.Menu()
        plotOptionsMenu =wx.Menu()
        helpmenu = wx.Menu()

        # creates the menu items on the menu objects
        # making the menu items instance variable so when binding, can refer to the objects item,
        clearItem = filemenu.Append(-1, "Clear Plot and Data", "Resets the graph to display nothing and removes all imported data")
        exitItem = filemenu.Append(wx.ID_EXIT, "Exit", "Exit the Application")
        timePlotItem = plotmenu.Append(-1, "Time Plot", "Plot time vs data")  # add event when push opens up menu to import data, and than call plots.timeplot
        diffPlotItem = plotmenu.Append(-1, "Difference Plot(NOT IMPLEMENTED)", "Plot the difference between two units.")
        addLineItem = plotOptionsMenu.Append(-1, "Add Line(NOT IMPLEMENTED)", "Adds a line to current graph")
        clearItemPlotOptions = plotOptionsMenu.Append(-1, "Clear Plot and Data", "Resets the graph to display nothing and removes all imported data")
        aboutItem = helpmenu.Append(wx.ID_ABOUT)

        # create a menu bar that the menu objects go on
        TMB = wx.MenuBar()
        TMB.Append(filemenu, "File")
        TMB.Append(plotmenu, "Plot Data")
        TMB.Append(plotOptionsMenu, "Plot Options")
        TMB.Append(helpmenu, "Help")
        self.SetMenuBar(TMB)

        # Binding Events in the menu object
        self.Bind(wx.EVT_MENU, self.on_about, aboutItem)
        self.Bind(wx.EVT_MENU, self.on_clear, clearItem)
        self.Bind(wx.EVT_MENU, self.on_exit, exitItem)
        self.Bind(wx.EVT_MENU, self.on_time_plot, timePlotItem)
        self.Bind(wx.EVT_MENU, self.on_diff_plot, diffPlotItem)
        self.Bind(wx.EVT_MENU, self.on_clear, clearItemPlotOptions)

    def _restart_graphing_panel(self):
        self.graphingPanelOne = GraphingPanel(parent=self)
        self.mainWindowSizer.Add(self.graphingPanelOne, border=10, proportion=1, flag=wx.ALL | wx.EXPAND)
        self.Layout()

    #using this so as not to call MainWindow.graphingPanelOne. I feel like that may be frowned apon.
    def get_graphing_panel(self):
        return self.graphingPanelOne

    """
    Handlers
    """
    def on_about(self, event):
        wx.MessageBox("DDR Plotting Tool. \n Created by Ryan Vreeland \n Plots CSV data from DDR")

    def on_exit(self, event):
        self.Close(True)

    def on_time_plot(self, e):
        testPopFrm = TimePlotWindow(parent=self, title="Import Data", size=(750, 750))
        testPopFrm.Show()

    def on_diff_plot(self, e):
        diffPlot = DifferencePlotWindow(parent=self, title ="Difference Plot", size=(750, 750))
        diffPlot.Show()

    def on_clear(self, e):
        Data_Handler.dataFromImport = pandas.DataFrame()
        Data_Handler.plotData = {}
        self.graphingPanelOne.Destroy()
        self._restart_graphing_panel()









