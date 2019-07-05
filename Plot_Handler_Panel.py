"""
DDR_PlottingTool Application -- Plot_Handler_Panel.py
File Created: 2019/01/22
Desc: contains wx.Panel child object that combines matlabplot and wxPython. Contains all the plotting functions as well
Author: Ryan Vreeland
"""


import wx
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wxagg import NavigationToolbar2WxAgg as NavigationToolbar
from matplotlib.figure import Figure
import Data_Handler

class PlotHandler(wx.Panel):
    def __init__(self, *args, **kwargs):
        super(PlotHandler, self).__init__(*args, **kwargs)
        self.figure = Figure()
        self.axes = self.figure.add_subplot(111)

        self.legend = None
        self.canvas = FigureCanvas(self, -1, self.figure) # I think FigureCannas is a widget from matlabplot
        self.toolbar = NavigationToolbar(self.canvas) #this creates the tool bar to do basic zoom, save, etc...
        self.toolbar.Realize()
        self.sizer = wx.FlexGridSizer(2, 1, wx.Size(5,5))
        self.sizer.Add(self.canvas, flag=wx.EXPAND)
        self.sizer.Add(self.toolbar, flag=wx.EXPAND)
        self.sizer.AddGrowableCol(0, 1)
        self.sizer.AddGrowableRow(0,1)
        self.SetSizer(self.sizer)


    """
    time_plot 
    plots time vs data for each 
    Mask works by making a list/pandas series of booleans indicating which items in the index are NAN. 
    Calling time[mask] will return sublist of time whose values are where mask is True. 
    example: data = [1, 2, NAN, 5, NAN, 8, 10, NAN, 13] mask= [T, T, F, T, F, T, T, F, T] 
    data[mask] = [1, 2, 5, 8, 10, 13] but pandas will still recognize them belonging to original index of data, 
    so the index of data[mask] [0, 1, 3, 5, 6, 8]
    Reason for Masking: for data with nan to appear properly and without displaying weirdness (essentially smooth line
    without gaps, or smoothline and gaps)
    """
    def time_plot(self, time, dataDict):
        self.axes.clear() # clearing anything that was there before.
        self.axes.set_xlabel("Time - Seconds", fontsize='x-large')

        for header, data in dataDict.items():
            mask = data.notna()
            self.axes.plot(time[mask], data[mask], label=header)

        #updates canvas so once I hit plot it shows up
        self._create_legend()
        self.canvas.draw()
        self.canvas.flush_events()

    def _create_legend(self):
        self.legend = self.axes.legend()


    """
    set the color of the particular line, 
    needs to take in the axis the line is located in, and the label of the line, and the new color
    """
    def set_color(self, label, color):
        for line in self.axes.get_lines():
            if line.get_label() == label:
                line.set_color(color)
        self._create_legend()
        self.canvas.draw()
        self.canvas.flush_events()


    def show_hide(self, label, evt_boolean):
        for line in self.axes.get_lines():
            if line.get_label() == label:
                line.set_visible(evt_boolean)
        self._create_legend()
        self.canvas.draw()
        self.canvas.flush_events()

    def clearLines(self):
        self.axes.clear()
        self.canvas.draw()
        self.canvas.flush_events()

    def get_axis(self):
        return self.axes

    def set_axes(self, yLimits, xLimits):
        yMin, yMax = yLimits
        xMin, xMax= xLimits

        self.axes.set_ylim(yMin, yMax, auto=True)
        self.axes.set_xlim(xMin, xMax, auto=True)
        self.canvas.draw()
        self.canvas.flush_events()


    def set_y_axis_label(self, label):
        self.axes.set_ylabel(label)
        self.canvas.draw()
        self.canvas.flush_events()