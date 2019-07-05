"""
DDR_PlottingTool Application -- Data_Handler.py
File Created: 2019/01/22
DESC: File to read in data from path, and alter data (such as removing HEX values, or making sure display correct rates).
Author: Ryan Vreeland
"""

import pandas
import matplotlib.pyplot as plt
import numpy as np
"""Global Variables"""
dataFromImport = pandas.DataFrame()
plotData = {} #dictionary


"""
returns a Data Frame if pathname was good, returns False IOError was triggered.
"""
def csv_import(filepath):
    retDF = pandas.DataFrame()
    errorTriggered = False

    try:
        retDF = pandas.read_csv(filepath, sep=',', header=0)
        retDF.columns = retDF.columns.str.strip()
        retDF =_remove_hex_values(retDF)

    except FileNotFoundError:
       errorTriggered = True

    return retDF, errorTriggered

# display headers of a dataframe df.columns.tolist()

def _remove_hex_values(DF):
    headerList = DF.columns.tolist()
    for col in headerList:
        if ("(hex)" in col):
            DF = DF.drop(col, axis=1)
    return DF



#testPath = r"C:\Users\ravreeland\PycharmProjects\DDR_PlottingTool\Testing\drirr_buffer1.csv"
#testData = csv_import(testPath)[0]
#droppedNAN = testData["MemAddr.EEbegin (dec)"].dropna()


"""#print(testData.fillna(method="ffill", limit=1))

#try masking later according to https://stackoverflow.com/questions/14399689/matplotlib-drawing-lines-between-points-ignoring-missing-data
#masking works. just want to see if I can do with with pandas and not have to have numpy. If i need numpy, oh well, will just use it
#see how the following code works, and how masking works
series1 = np.array(list(testData["MemAddr.EEbegin (dec)"])).astype(np.double)
s1mask = np.isfinite(series1) #creates a list of booleans saying whether a number is finite and graphable. helps with matplotlib
maskedX = testData["Time"][s1mask]
#s1mask is what allows it to graph
print(s1mask)
print(testData["Time"][s1mask])
print(series1[s1mask])
print(len(s1mask))
fig, axes = plt.subplots(1,1)

testSeries = pandas.Series([1, np.nan, 3, 4, np.nan])
print(testSeries.notna())

ySeries = testData["MemAddr.EEbegin (dec)"]
mask = ySeries.notna()


axes.plot(testData["Time"][mask], ySeries[mask], linestyle='-')
plt.show()
"""