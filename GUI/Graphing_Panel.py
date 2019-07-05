"""
DDR_Plotting_Tool Application -- Graphing_Panel.py
File Created: 2019/01/22
Desc: This contains class that is a child of panel and will include every gui item to manipulate the plot, and the Plot_Handler_Panel as well.
      Entire Reason for having this be a seperate object is to be able to make multiple instances of it for later implimentation. (Think, switching pages of graphs)
Author: Ryan Vreeland
"""

import wx
import Data_Handler
from GUI.Plot_Handler_Panel import PlotHandler

"""
Existence of this class is meant to make it easier to impliment having multiple pages of graphs later. Essentially, 
GUI_Main will have a list of objects of the class type, that at a given moment only one will be shown, rest hidden. 
This class initiates a Plot_Handler_Panel object, and uses it as one of its child wx.windows . 
"""

class GraphingPanel(wx.Panel):
    def __init__(self, *args, **kwargs):
        super(GraphingPanel, self).__init__(*args, **kwargs)

        self._create_options_panel() # makes and populates the options panel (makes instance variables)
        self.plotAreaPanel = PlotHandler(parent=self) #widget that contains the plot
        self.graphingPanelSizer = wx.FlexGridSizer(1, 2, wx.Size(5, 5))  # top level sizer

        # adding to top level sizer
        self.graphingPanelSizer.Add(self.optionsPanel, flag=wx.EXPAND)
        self.graphingPanelSizer.Add(self.plotAreaPanel, flag=wx.EXPAND)
        #self.graphingPanelSizer.AddGrowableCol(0, 1)
        self.graphingPanelSizer.AddGrowableCol(1, 3)
        self.graphingPanelSizer.AddGrowableRow(0, 1)
        self.SetSizer(self.graphingPanelSizer)

    def _create_options_panel(self):

        # Initializing panels and sizers
        # Panels
        self.optionsPanel = wx.Panel(parent=self)# top level panel
        self.colorPanel = wx.Panel(parent=self.optionsPanel)
        self.showHidePanel = wx.Panel(parent=self.optionsPanel)
        self.showHideCheckBoxPanel = wx.Panel(parent=self.showHidePanel)  # panel that contains checkboxes, uses BoxSizer
        self.axesEntryPanel = wx.Panel(parent=self.optionsPanel)

        # sizers
        optionsSizer = wx.FlexGridSizer(3, 1, wx.Size(5, 5))
        colorSizer = wx.FlexGridSizer(2, 1, wx.Size(5, 5))
        colorChoiceSizer = wx.FlexGridSizer(1, 2, wx.Size(5, 5))
        showHideSizer = wx.FlexGridSizer(2, 1, wx.Size(5, 5))  # top level sizer for showHidePanel
        showHideCBSizer = wx.BoxSizer(wx.VERTICAL)
        axesEntrySizer = wx.FlexGridSizer(6, 3, wx.Size(5, 5))


        # Creating the content that goes in the panels
        # shown top to bottom, left to right, as would appear on GUI

        # Color Choice Content
        colorLabel = wx.StaticText(parent=self.colorPanel, label="Color Options", style=wx.ALIGN_LEFT)
        colorLabalFont = colorLabel.GetFont()
        colorLabalFont.PointSize += 6
        colorLabalFont = colorLabalFont.Bold()
        colorLabel.SetFont(colorLabalFont)

        # Choice Text Boxes
        self.lineSelection = wx.Choice(parent=self.colorPanel, choices=["Select Line"]) #line options will be added in once plot is created (on_plot)
        colorChoices = ["Select Color", "blue", "green", "red", "cyan", "magenta", "yellow", "black", "purple", "orange"]
        self.colorSelection = wx.Choice(parent=self.colorPanel, choices=colorChoices)
        self.lineSelection.SetSelection(0)
        self.colorSelection.SetSelection(0)
        self.Bind(wx.EVT_CHOICE, self.on_color_selection, self.colorSelection)

        # ShowHide Content
        # Checkboxes are made once the plot is created.
        showHideLabel = wx.StaticText(parent=self.showHidePanel, label="Show/Hide", style=wx.ALIGN_LEFT)
        showHideLabelFont = colorLabalFont
        showHideLabel.SetFont(showHideLabelFont)

        # Axes Specifier Content
        timeAxisLabel = wx.StaticText(parent=self.axesEntryPanel, label="Time Axis", style=wx.ALIGN_LEFT)
        yAxisLabel = wx.StaticText(parent=self.axesEntryPanel, label="Y-Axis", style=wx.ALIGN_LEFT)
        self.yAxisEntryMin = wx.TextCtrl(parent=self.axesEntryPanel, size=wx.Size(20, 20))
        self.yAxisEntryMax = wx.TextCtrl(parent=self.axesEntryPanel, size=wx.Size(20, 20))
        self.timeAxisEntryMin = wx.TextCtrl(parent=self.axesEntryPanel, size=wx.Size(20, 20))
        self.timeAxisEntryMax = wx.TextCtrl(parent=self.axesEntryPanel, size=wx.Size(20, 20))
        yMinMaxSeperator = wx.StaticText(parent=self.axesEntryPanel, label="-") #there is two, bc I am pretty sure you can't add the same wigit twice
        timeMinMaxSeperator = wx.StaticText(parent=self.axesEntryPanel, label="-")
        yMinMaxSeperator.SetFont(colorLabalFont)
        timeMinMaxSeperator.SetFont(colorLabalFont)
        setAxesButton = wx.Button(parent=self.axesEntryPanel, label="Set Axis", style=wx.BU_EXACTFIT)
        resetAxesButton = wx.Button(parent=self.axesEntryPanel, label="Reset", style=wx.BU_EXACTFIT)

        self.Bind(wx.EVT_BUTTON, self.on_set_axes, setAxesButton)
        self.Bind(wx.EVT_BUTTON, self.on_reset_axes, resetAxesButton)
        AEFont = self.timeAxisEntryMax.GetFont()  # AE--> axes entry
        AEFont.PointSize += 3
        self.timeAxisEntryMax.SetFont(AEFont)
        self.timeAxisEntryMin.SetFont(AEFont)
        self.yAxisEntryMax.SetFont(AEFont)
        self.yAxisEntryMin.SetFont(AEFont)

        # adding to sizers
        colorSizer.Add(colorLabel)
        colorSizer.Add(colorChoiceSizer, flag=wx.EXPAND)
        colorChoiceSizer.Add(self.lineSelection, flag=wx.EXPAND)
        colorChoiceSizer.Add(self.colorSelection, flag=wx.EXPAND)
        colorChoiceSizer.AddGrowableCol(0,1)
        colorChoiceSizer.AddGrowableCol(1,1)

        showHideSizer.Add(showHideLabel)
        showHideSizer.Add(self.showHideCheckBoxPanel)
        showHideSizer.AddGrowableRow(1,3)
        showHideSizer.AddGrowableCol(0,1)

        # I use a blank staticText to add a filler (perhaps can use AddSpacer, I think it worked before
        # but I read somewhere that it doesnt work for FlexGridSizer).
        axesEntrySizer.Add(wx.StaticText(parent=self.axesEntryPanel))# 0,0 (row, col in FlexGridSizer) Filler
        axesEntrySizer.Add(yAxisLabel, flag=wx.ALIGN_CENTER) # 0,1
        axesEntrySizer.Add(wx.StaticText(parent=self.axesEntryPanel))# 0,2 Filler
        axesEntrySizer.Add(self.yAxisEntryMin, flag=wx.EXPAND) # 1,0
        axesEntrySizer.Add(yMinMaxSeperator, flag=wx.ALIGN_CENTER) # 1,1
        axesEntrySizer.Add(self.yAxisEntryMax, flag=wx.EXPAND) # 1,2
        axesEntrySizer.Add(wx.StaticText(parent=self.axesEntryPanel)) # 2,0 Filler
        axesEntrySizer.Add(timeAxisLabel, flag=wx.ALIGN_CENTER) # 2,1
        axesEntrySizer.Add(wx.StaticText(parent=self.axesEntryPanel)) # 2,2 Filler
        axesEntrySizer.Add(self.timeAxisEntryMin, flag=wx.EXPAND) # 3,0
        axesEntrySizer.Add(timeMinMaxSeperator, flag=wx.ALIGN_CENTER) # 3,1
        axesEntrySizer.Add(self.timeAxisEntryMax, flag=wx.EXPAND) # 3,2
        axesEntrySizer.Add(wx.StaticText(parent=self.axesEntryPanel)) # 4, 0 Filler
        axesEntrySizer.Add(setAxesButton, flag=wx.ALIGN_CENTER) #4,1
        axesEntrySizer.Add(wx.StaticText(parent=self.axesEntryPanel)) # 4, 2 Filler
        axesEntrySizer.Add(wx.StaticText(parent=self.axesEntryPanel)) # 4, 0 Filler
        axesEntrySizer.Add(resetAxesButton, flag=wx.ALIGN_CENTER) # 4, 1
        axesEntrySizer.Add(wx.StaticText(parent=self.axesEntryPanel)) # 4, 2 Filler
        axesEntrySizer.AddGrowableCol(0, 1)
        axesEntrySizer.AddGrowableCol(2, 1)

        optionsSizer.Add(self.colorPanel, flag=wx.EXPAND)
        optionsSizer.Add(self.showHidePanel, flag=wx.EXPAND)
        optionsSizer.Add(self.axesEntryPanel, flag=wx.EXPAND)

        #self.optionsSizer.AddGrowableRow(0,1)
        optionsSizer.AddGrowableRow(1,3)
        optionsSizer.AddGrowableRow(2,1)
        optionsSizer.AddGrowableCol(0,1)


        # setting the sizers to coresponding panels
        self.colorPanel.SetSizer(colorSizer)
        self.showHidePanel.SetSizer(showHideSizer)
        self.showHideCheckBoxPanel.SetSizer(showHideCBSizer)
        self.axesEntryPanel.SetSizer(axesEntrySizer)
        self.optionsPanel.SetSizer(optionsSizer)

    """
    Functions of the Object
    """
    """
    methods for pop/depop choice list for line selection
    """
    def populate_line_selection(self):
        for header in Data_Handler.plotData.keys():
            self.lineSelection.Append(header)
        self.Layout()

    def depopulate_line_selection(self):
        numOfLines = self.lineSelection.GetCount()
        for i in range(numOfLines-1, 0, -1):
            self.lineSelection.Delete(i)
        self.Layout()

    """
    Next two methods deal with creating, and removing checkboxes from show/hide panel
    When adding in checkboxes, also creates the binding for each box. 
    These methods are called by handlers (on_plot) for ImportPlotWindow children.
    """
    def populate_show_hide_panel(self):
        showHideCBSizer = self.showHideCheckBoxPanel.GetSizer()
        for header in Data_Handler.plotData.keys():
            SHcheckBox = wx.CheckBox(parent=self.showHideCheckBoxPanel, label=header)
            SHcheckBox.SetValue(True) #sets initial appearance with check marked
            self.Bind(wx.EVT_CHECKBOX, self.on_show_hide_checkbox, SHcheckBox)
            showHideCBSizer.Add(SHcheckBox, flag=wx.LEFT, proportion=1)
            showHideCBSizer.AddSpacer(5)
        self.Layout()

    def remove_show_hide_panel_elements(self):
        showHideCBSizer = self.showHideCheckBoxPanel.GetSizer()
        numOfCheckBoxes = len(showHideCBSizer.GetChildren())
        parentOfBoxes = showHideCBSizer.GetContainingWindow() #should be showHideCheckBoxPanel
        while numOfCheckBoxes > 0:
            showHideCBSizer.Hide(numOfCheckBoxes-1)
            showHideCBSizer.Remove(numOfCheckBoxes - 1)
            numOfCheckBoxes -= 1
        parentOfBoxes.DestroyChildren()
        self.Layout()

    """
    Calls the method on its plotAreaPanel object.
    Called by the handler (on_plot) in ImportPlotWindow
    passing the y axis label from timePlotWindow to set the axis
    """
    def populate_plot_area_panel(self, label):
        self.plotAreaPanel.time_plot(Data_Handler.dataFromImport['Time'], Data_Handler.plotData)
        self.plotAreaPanel.set_y_axis_label(label)

    """
    helper method to on_set_axes. Allows to not have to repeat code for both axes as they both have same if statement 
    logic.
    takes in the strings that were entered in the textEntryBox.
    Checks for blank entries, and non numerical entries. If detects non numerical entry, returns a False signal. True if 
    everything is ok. Assuming True to begin with, sets False if exception is triggered
    """
    def _is_axis_entry_digit(self, min, max):
        retBoolean = True
        try:
            min = float(min)
            max = float(max)
        except ValueError:
            retBoolean = False
        return retBoolean


    """ Handlers """

    def on_show_hide_checkbox(self, e):
        eventObject = e.GetEventObject()
        label = eventObject.GetLabel()
        self.plotAreaPanel.show_hide(label, eventObject.IsChecked())

    def on_color_selection(self, e):
        currentColor = self.colorSelection.GetString(self.colorSelection.GetCurrentSelection())
        currentLine = self.lineSelection.GetString(self.lineSelection.GetCurrentSelection())

        if currentLine == "Select Line" and currentColor != "Select Color":
            wx.MessageBox("No Line Selected. Please Select a Line.")

        elif currentColor != "Select Color":
            self.plotAreaPanel.set_color(currentLine, currentColor)

    # handler for when GUI button labeled Set is pressed
    def on_set_axes(self, e):
        yMin = self.yAxisEntryMin.GetValue()
        yMax = self.yAxisEntryMax.GetValue()
        timeMin = self.timeAxisEntryMin.GetValue()
        timeMax = self.timeAxisEntryMax.GetValue()
        currentYMin, currentYMax = self.plotAreaPanel.get_axis().get_ylim()
        currentTimeMin, currentTimeMax = self.plotAreaPanel.get_axis().get_xlim()

        # First check to see if any is blank. If blank, just assign it to current limit
        if yMin == "":
            yMin = str(currentYMin)
        if yMax == "":
            yMax = str(currentYMax)
        if timeMin == "":
            timeMin = str(currentTimeMin)
        if timeMax == "":
            timeMax = str(currentTimeMax)

        # second check to see if it is a digit.
        yAxisCheck = self._is_axis_entry_digit(yMin, yMax)
        timeAxisCheck = self._is_axis_entry_digit(timeMin, timeMax)

        # series of statements checking possible all possible conditions to give helpful messages as to what went wrong.
        # if nothing is wrong, else statement will call the method to change the axis.
        if yAxisCheck == False and timeAxisCheck == True:
            wx.MessageBox("Invalid Entry in Y Axis. Entry is not a digit.")
        elif yAxisCheck == True and timeAxisCheck == False:
            wx.MessageBox("Invalid entry in Time axis. Entry is not a digit.")
        elif yAxisCheck == False and timeAxisCheck == False:
            wx.MessageBox("Invalid entry with both Y and Time axes. Entries are not digits.")
        else:
            self.plotAreaPanel.set_axes([float(yMin), float(yMax)], [float(timeMin), float(timeMax)])

    # home button on NavigationToolbar2WxAgg would not really reset to how it originally was graphed, just to
    # what was set with the set axes button. This will essentially regraph the data. May not need it as last time I was
    # messing with the set axes, it was reseting to original. Will have to play around with it more.
    def on_reset_axes(self, e):
        self.populate_plot_area_panel()



