#Release Ready v2020.01  
#Script to deal with the automated gas values and tables

import pandas as pd
import numpy as py

def importGasTableComplex(csvFileToImport = '//home/GRJ/Documents/3_testDir/gasTable.csv'):
    tempArray=[] #Create Array to temporarily store MFC set values
    #Import Gas Data
    gasTable = pd.read_csv(csvFileToImport)
    gasTestArray = gasTable.to_numpy(copy=True)

    mfc1 = gasTestArray[:,0]*gasTestArray[:,1] #Caluclate MFC1 value
    mfc3 = (gasTestArray[:,1]-mfc1)*gasTestArray[:,2] #Caluclate MFC3 (humidity) value
    mfc2 = gasTestArray[:,1]-mfc1-mfc3 #Caluclate MFC2 value

    tempArray = py.column_stack((mfc1, mfc2, mfc3, gasTestArray[:,3]))
    mfcDataFrame = pd.DataFrame(tempArray, columns = ['MFC1', 'MFC2', 'Humidity', 'Time']) #Convert Array to Data Frame
    return mfcDataFrame
#Array column headings (input) [H2%; TOTALFLOW; HUMIDITY; TIME;]
#Array column headings (calculated) [H2FLOWRATE(H2%*TOTALFLOW); MIXTOTAL(TOTALFLOW-H2FLOWRATE)]

def importGasTableSimple(csvFileToImport = '//home/GRJ/Documents/3_testDir/gasTable2.csv'):
    tempArray=[] #Create Array to temporarily store MFC set values
    #Import Gas Data
    gasTable = pd.read_csv(csvFileToImport)
    gasTestArray = gasTable.to_numpy(copy=True)

    mfc1 = gasTestArray[:,0] #Caluclate MFC1 value
    mfc2 = gasTestArray[:,1] #Caluclate MFC3 (humidity) value
    mfc3 = gasTestArray[:,2] #Caluclate MFC2 value

    tempArray = py.column_stack((mfc1, mfc2, mfc3, gasTestArray[:,3]))
    mfcDataFrame = pd.DataFrame(tempArray, columns = ['MFC1', 'MFC2', 'Humidity', 'Time']) #Convert Array to Data Frame
    return mfcDataFrame

def importGasTableFullAuto(csvFileToImport = '//home/GRJ/Documents/3_testDir/fullAutoGas.csv'):
    tempArray = []
    gasTable = pd.read_csv(csvFileToImport)
    gasTestArray = gasTable.to_numpy(copy=True)

    mfc1 = gasTestArray[:,0]
    mfc2 = gasTestArray[:,1]
    mfc3 = gasTestArray[:,2]
    gasTime = gasTestArray[:,3]
    currentVal = gasTestArray[:,4]
    currentChangeTime = gasTestArray[:,5]

    tempArray = py.column_stack((mfc1, mfc2, mfc3, gasTime))
    mfcDataFrame = pd.DataFrame(tempArray, columns = ['MFC1', 'MFC2', 'MFC3', 'Time'])
    tempArray = []
    tempArray = py.column_stack((currentVal, currentChangeTime))
    hotwireDataFrame = pd.DataFrame(tempArray, columns = ['HWCurrent', 'HWSettleTime'])
    hotwireDataFrame = hotwireDataFrame[hotwireDataFrame.HWSettleTime.notnull()]
    return mfcDataFrame, hotwireDataFrame



def gasCalulations(gasTable):
    #This function caluclates gas values from the data
    #totalFlowRate = 
    return
