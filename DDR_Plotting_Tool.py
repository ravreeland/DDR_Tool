"""
DDR_Plotting_Tool Application -- DDR_Plotting_Tool.py
File Created: 2019/01/22
Desc: The main py script to run whole thing
Author: Ryan Vreeland

Style GuideLine --> For Ryan Vreeland own rememberance

Methods --> lower case with underscore seperation --> example_of_method.
Private methods (those not are not/should not be used in a another file) --> leading underscore --> _example_of_private_method
variables --> lowercase first word, capital first on other words --> exampleOfVariable : series of capital letters indicates acronym
class names --> capital on all cases, should have same name as file its in. --> ExampleClassName
important file names --> capitalized words with underscore seperating words --> Example_File_Name.py

"""
import wx
from GUI.GUI_Main import MainWindow


def run_tool():

    app = wx.App()
    mw_size = wx.Size(1000,800)

    main_window = MainWindow(None, title='DDR Plotting Tool', size=mw_size)
    main_window.Show()
    
    app.MainLoop()

"""
Things to change/add Notes:

Need to implement being able to graph different rate data. Current not plotting (but no error) data that is as a 
different recording rate. Examples: MemAddr.EEbegin (dec) and MemAddrEEend(dec) 

I want to see if i can create a child class of NavigationToolbar2WxAgg to have the home button reset axis to original 
view when first plotted. And wish to add the axis to that panel instead as there is a lot of wasted space. Makes more 
sense for those to be there. 


"""

"""
Notes on behavior of import and plot on data.
import button behavior
when importing data, and then closing out of import/plot(I/P) window --> overrides previous data with imported data.


plot button behaviour


Plotting window does not remove previous lines. Will have to destory those, or call an update/clear on axes

"""

run_tool()