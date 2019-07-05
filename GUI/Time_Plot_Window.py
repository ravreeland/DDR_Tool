from GUI.Import_Plot_Window import ImportPlotWindow
import wx

"""
DDR_Plotting_Tool Application -- Import_Plot_Window.py
File Created: 2019/01/22
Desc: Class that is a generic importation window. Has two sections, a browse/import section which will be implemented
in this class, and a plot section that be specific to others. Gen
Author: Ryan Vreeland
"""

import wx
import Data_Handler

class TimePlotWindow(ImportPlotWindow):

    def __init__(self, *args, **kwargs):
        ImportPlotWindow.__init__(self, *args, **kwargs) # need to use this rather than super as

        self._create_plot_section() # this isnt called in parant class's

    def _create_plot_section(self):
        self.plotCheckBoxPanel_1 = wx.Panel(parent=self.plotPanel)
        self.plotCheckBoxSizer_1 = wx.BoxSizer(wx.VERTICAL)
        self.plotCheckBoxPanel_2 = wx.Panel(parent=self.plotPanel)
        self.plotCheckBoxSizer_2 = wx.BoxSizer(wx.VERTICAL)

        self.plotCheckBoxPanel_1.SetSizer(self.plotCheckBoxSizer_1)
        self.plotCheckBoxPanel_2.SetSizer(self.plotCheckBoxSizer_2)

        #label for section
        plotLabel = wx.StaticText(parent=self.plotPanel, label="Plotting Info:", style=wx.ALIGN_LEFT|wx.ALIGN_TOP)
        plotLabelFont = plotLabel.GetFont()
        plotLabelFont.PointSize += 6
        plotLabelFont = plotLabelFont.Bold()
        plotLabel.SetFont(plotLabelFont)

        # Y Axis label text entry
        yEntryLabel = wx.StaticText(parent=self.plotPanel, label="Enter Y Axis Label", style=wx.ALIGN_CENTER)
        self.yAxisEntry = wx.TextCtrl(parent=self.plotPanel)
        yEntrySizer= wx.BoxSizer(wx.VERTICAL)
        yEntrySizer.Add(yEntryLabel, flag=wx.EXPAND)
        yEntrySizer.Add(self.yAxisEntry, flag=wx.EXPAND)

        #plot Button
        btnPlot = wx.Button(parent=self.plotPanel, label="Plot", style=wx.BU_EXACTFIT)
        self.Bind(wx.EVT_BUTTON, self.on_plot, btnPlot)

        #adding to flex grid sizer
        self.plotSizer.Add(plotLabel, proportion=1, flag=wx.EXPAND)
        self.plotSizer.Add(yEntrySizer, flag=wx.EXPAND)
        self.plotSizer.Add(self.plotCheckBoxPanel_1, proportion=1)
        self.plotSizer.Add(self.plotCheckBoxPanel_2, proportion=2)
        self.plotSizer.Add(wx.StaticText(parent=self.plotPanel, label=""))
        self.plotSizer.Add(btnPlot, proportion=1, flag=wx.ALIGN_TOP|wx.ALIGN_RIGHT)

        #growing flexgridSizer
        self.plotSizer.AddGrowableCol(0,1)
        self.plotSizer.AddGrowableCol(1,1)
        self.plotSizer.AddGrowableRow(1,2)
        self.plotSizer.AddGrowableRow(2,1)

        # Setting the sizers to panels and Frame
        self.plotPanel.SetSizer(self.plotSizer)

    """ Methods of the Frame """

    # remove all previous check boxes
    def _delete_plot_check_boxes(self, targetSizer):
        numOfCheckBoxes = len(targetSizer.GetChildren())
        parentOfBoxes = targetSizer.GetContainingWindow()
        while numOfCheckBoxes > 0:
            #hide so doesn't attempt to appear on screen still as hadnt been delete from parent
            targetSizer.Hide(numOfCheckBoxes-1)
            targetSizer.Remove(numOfCheckBoxes-1)
            numOfCheckBoxes -= 1

        #making sure the previous boxes are destroy to not take up memory space
        parentOfBoxes.DestroyChildren()
        self.Layout()

    # create and bind check boxes
    def _set_plot_check_boxes(self):
        headerList = Data_Handler.dataFromImport.columns.tolist() #this should be only called after data has been uploaded
        headerList.remove("Time") #dont need this one.
        i = 0
        # in future, may want to use checkBoxSizer.GetItemCount() to control if statements, if allowing using multiple files.
        for header in headerList:
            if 0 <= i <= 13 or 26 <= i <= 39:
                checkBox1=wx.CheckBox(parent=self.plotCheckBoxPanel_1, label=header)
                self.Bind(wx.EVT_CHECKBOX, self.on_plot_check_box, checkBox1)
                self.plotCheckBoxSizer_1.Add(checkBox1, flag=wx.LEFT, proportion=1)
                self.plotCheckBoxSizer_1.AddSpacer(10)
            else:
                checkBox2 = wx.CheckBox(parent=self.plotCheckBoxPanel_2, label=header)
                self.Bind(wx.EVT_CHECKBOX, self.on_plot_check_box, checkBox2)
                self.plotCheckBoxSizer_2.Add(checkBox2, flag=wx.LEFT, proportion=1)
                self.plotCheckBoxSizer_2.AddSpacer(10)
            i += 1
        self.Layout()

    """ Handlers """

    """
    Overrides parentClass (not parent wigix) on_import
    """
    def on_import(self, e):
        """
        handler for import button, displays popup message if file path couldnt be found.
        logic here should all be dealing with GUI
        """
        #Assigns Global variables from Data_Handler rather than having the file Data_Handler assign them because this logic determines whether to append, or just reassign it
        filePath = self.textFileEntry.GetValue()
        Data_Handler.plotData = {} #or call clear/del or something...
        if(filePath != ""):
            DF, error = Data_Handler.csv_import(self.textFileEntry.GetValue())
            if (error == True):
                self._file_error_message("The file, {}, could not be found.".format(filePath)) #f"....{filePath}...." PyCharm kept giving error about f not supported in python2.7 Not sure why...
            elif(self.appendData == False):
                Data_Handler.dataFromImport = DF #this does override it.
                self._delete_plot_check_boxes(self.plotCheckBoxSizer_1)
                self._delete_plot_check_boxes(self.plotCheckBoxSizer_2)
                self._set_plot_check_boxes()
            elif(self.appendData == True): # just clearing away previous check boxes just to make sure.
                currentHeaders = Data_Handler.dataFromImport.columns.values.tolist()

                for header in DF.columns.values.tolist():
                    if header in currentHeaders and header != "Time":
                        DF.rename(columns={header:header+"[1]"}, inplace=True)

                Data_Handler.dataFromImport = Data_Handler.dataFromImport.append(DF, sort=False)
                self._delete_plot_check_boxes(self.plotCheckBoxSizer_1)
                self._delete_plot_check_boxes(self.plotCheckBoxSizer_2)
                self._set_plot_check_boxes()
        else:
            self.textFileEntry.SetValue("No File Choosen!")

    def on_plot_check_box(self, e):
        eventObject = e.GetEventObject()
        header = eventObject.GetLabel()
        if(eventObject.IsChecked()==True):
            Data_Handler.plotData[header] = Data_Handler.dataFromImport[header]
        else:
            del Data_Handler.plotData[header]


    def on_plot(self, e):
        parent = self.GetParent()
        targetGraphingPanel = parent.get_graphing_panel()


        targetGraphingPanel.depopulate_line_selection() #remove any that were there already. Making sure nothing is still there, but existing in the current plot
        targetGraphingPanel.populate_line_selection()
        targetGraphingPanel.populate_plot_area_panel(self.yAxisEntry.GetValue())
        targetGraphingPanel.remove_show_hide_panel_elements() #remove any that were there already. B4 it was keeping the
        #previous checkboxes from the last plotting
        targetGraphingPanel.populate_show_hide_panel()

        self.Close(True)


