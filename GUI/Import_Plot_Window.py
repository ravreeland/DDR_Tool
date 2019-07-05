"""
DDR_Plotting_Tool Application -- Import_Plot_Window.py
File Created: 2019/01/22
Desc: Class that is a generic importation window. Has two sections, a browse/import section which will be implemented
in this class, and a plot section that be specific to others. Gen
Author: Ryan Vreeland
"""

import wx
import Data_Handler

class ImportPlotWindow(wx.Frame):

    def __init__(self, *args, **kwargs):
        super(ImportPlotWindow, self).__init__(*args, **kwargs)
        # Main sizers
        self.borderSizer = wx.BoxSizer(wx.VERTICAL)
        self.importPlotWindowSizer = wx.FlexGridSizer(2, 1, wx.Size(5, 5))# top level sizer

        # Instance Variables for import section
        self.importPanel = wx.Panel(parent=self)
        self.importSizer = wx.FlexGridSizer(3, 2, wx.Size(5, 5))  # top level sizer for this section
        self.textFileEntry = wx.TextCtrl(parent=self.importPanel, size=wx.Size(20, 20))
        self.appendData = False

        #  Instance Variables for plot section
        self.plotPanel = wx.Panel(parent=self)
        self.plotSizer = wx.FlexGridSizer(3, 2, wx.Size(5, 5))

        self._create_import_section()

        #adding the sections to the main panel
        self.importPlotWindowSizer.Add(self.importPanel, flag=wx.EXPAND) #self.importPanel created in _create_import_section()
        self.importPlotWindowSizer.Add(self.plotPanel, flag=wx.EXPAND)

        # Growing sizer's rows/cols
        self.importPlotWindowSizer.AddGrowableCol(0, 1)
        self.importPlotWindowSizer.AddGrowableRow(0, 1)
        self.importPlotWindowSizer.AddGrowableRow(1, 10)

        backGroundColor = self.importPanel.GetBackgroundColour()
        self.SetBackgroundColour(backGroundColor)
        self.borderSizer.Add(self.importPlotWindowSizer, border=10, proportion=1, flag=wx.ALL | wx.EXPAND)
        self.SetSizer(self.borderSizer)

    """
    creates the import section. Shouldn't need to be overridden by children
    """
    def _create_import_section(self):

        ### Section Contents ###
        # initiated in left to right, top to bottom
        #Static Text Label
        importPanelLabel = wx.StaticText(parent=self.importPanel, label="Browse and Import", style=wx.ALIGN_LEFT)
        IPLFont = importPanelLabel.GetFont()
        IPLFont.PointSize += 6
        IPLFont =IPLFont.Bold()
        importPanelLabel.SetFont(IPLFont)

        # File Label --> Static Text Widget --> added into a seperate flex grid sizer along with textFileEntry
        fileStaticText = wx.StaticText(parent=self.importPanel, label="File:", style=wx.ALIGN_RIGHT)  # size(width, height)
        fileLabelFont = fileStaticText.GetFont()
        fileLabelFont.PointSize += 4
        fileLabelFont = fileLabelFont.Bold()
        fileStaticText.SetFont(fileLabelFont)
        textSizerFlag = wx.SizerFlags(1)
        textSizerFlag.Center()

        #File Entry Bar
        TFEFont = self.textFileEntry.GetFont() #TFE --> text file entry
        TFEFont.PointSize += 3
        self.textFileEntry.SetFont(TFEFont)

        #sizer for File Label and textFileEntry textbox
        fileTextEntrySizer = wx.FlexGridSizer(1,2, wx.Size(5,5))
        fileTextEntrySizer.Add(fileStaticText)
        fileTextEntrySizer.Add(self.textFileEntry, flag=wx.EXPAND)
        fileTextEntrySizer.AddGrowableCol(1, 3)

        # Data Append checkbox --> will control whether appendData is True or False
        appendImportedDataCheckBox = wx.CheckBox(parent=self.importPanel, label="Append Data To Current Data Storage")
        self.Bind(wx.EVT_CHECKBOX, self.on_append_check_box, appendImportedDataCheckBox)

        # Browse and Import buttons
        btnBrowse = wx.Button(parent=self.importPanel, label="Browse", style=wx.BU_EXACTFIT)
        btnSize = btnBrowse.GetSize()
        btnImport = wx.Button(parent=self.importPanel, label="Import", size=btnSize) #making the same size as Browse
        self.Bind(wx.EVT_BUTTON, self.on_import, btnImport)
        self.Bind(wx.EVT_BUTTON, self.on_browse, btnBrowse)

        #Adding widgets to flexgridsizer --> sizer is 3 rows, 2 cols
        self.importSizer.Add(importPanelLabel, flag=wx.EXPAND)  # 0,0 (row, col) --> Main label
        self.importSizer.Add(wx.StaticText(parent=self))  # 0, 1 -->space holder
        self.importSizer.Add(fileTextEntrySizer, flag=wx.EXPAND)  # 1, 0 -->
        self.importSizer.Add(btnBrowse, flag=wx.ALIGN_RIGHT)  # 1,1 --browse
        self.importSizer.Add(appendImportedDataCheckBox, flag=wx.ALIGN_RIGHT) # 2,0
        self.importSizer.Add(btnImport, flag=wx.ALIGN_RIGHT)  # 2,1 --import

        # Growing Rows and Columns
        self.importSizer.AddGrowableCol(0, 3)
        self.importSizer.AddGrowableRow(0, 1)
        self.importSizer.AddGrowableRow(2, 1)

        self.importPanel.SetSizer(self.importSizer)

    """
    Creates the plot section. Must be overridden by children
    """
    def _create_plot_section(self):
        pass

    """ Methods of the Frame """

    # later maybe put this in its own file for GUI Error Handling functions. for right now can just stay
    def _file_error_message(self, error):
        message = wx.MessageDialog(parent=self, message=error, caption="File Error!",
                                   style=wx.OK | wx.CENTER, pos=wx.DefaultPosition)
        message.ShowModal()

    """ Handlers """

    def on_browse(self, e):
        fileDialog = wx.FileDialog(self, "Open csv files", wildcard="csv files (*.csv)|*.csv", style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        if fileDialog.ShowModal() == wx.ID_CANCEL:
            return  # the user changed their mind
        # Proceed loading the file chosen by the user
        pathName = fileDialog.GetPath()
        self.textFileEntry.SetValue(pathName)

    def on_append_check_box(self, e):
        eventObject = e.GetEventObject()
        if(eventObject.IsChecked() == True):
            self.appendData = True
        elif(eventObject.IsChecked() == False):
            self.appendData = False

    """
    This handler does nothing in this abstract class because it has to do with plotting and editing the plotSection.
    Will be/must be overidden in child classes 
    """
    def on_import(self, e):
        pass



