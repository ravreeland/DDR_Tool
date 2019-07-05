from GUI.Import_Plot_Window import ImportPlotWindow
import wx

class DifferencePlotWindow(ImportPlotWindow):

    def __init__(self, *args, **kwargs):
        ImportPlotWindow.__init__(self, *args, **kwargs)
        self._create_plot_section()

    #Overloading from ImportPlotWindow
    def _create_plot_section(self):
        self.plotSizer.Add(wx.StaticText(parent=self.plotPanel, label="TEST OVERRIDE"))
        #self.plotSizer.Add()
        self.plotPanel.SetSizer(self.plotSizer)
