from alicat import *
import time

#Unix or Windows
#flow_controller = FlowController(port='/dev/ttyUSB0') #Unix
#flow_controller = FlowController(port='COM1') #Windows

def initialiseMFCs():
    flow_controller = FlowController(port='/dev/ttyUSB0') #Unix 
    #flow_controller = FlowController(port='COM1') #Windows
    print(flow_controller.get())

    #Initialise MFC's 
    initialMFCs = []
    initialMFCs.append(FlowController(port='/dev/ttyUSB0', address='C')) #Hydrogen Controller
    initialMFCs.append(FlowController(port='/dev/ttyUSB0', address='B')) #Nitrogen Controller
    initialMFCs.append(FlowController(port='/dev/ttyUSB0', address='A')) #Humidity Controller 
    initialMFCs.append(FlowMeter(port='/dev/ttyUSB0', address = 'E')) #Exhaust meter
    print(initialMFCs)
    print(initialMFCs[0].get())
    print('Line 21')
    print(initialMFCs[1].get())
    print(initialMFCs[2].get())
    print(initialMFCs[3].get())

    setGas(initialMFCs)
    #updateMFCFlowSetPoint(initialMFCs)
    
    return initialMFCs

#Setup gases 
def setGas(MFCarray, gas1='H2', gas2='N2', gas3='N2', gas4='Air'):
    MFCarray[0].set_gas(gas1)
    MFCarray[1].set_gas(gas2)
    MFCarray[2].set_gas(gas3)
    MFCarray[3].set_gas(gas3)

    print('MFC1 Gas: ' + MFCarray[0].get()['gas'])
    print('MFC2 Gas: ' + MFCarray[2].get()['gas'])
    print('MFC3 Gas: ' + MFCarray[2].get()['gas'])
    print('MFC4 Gas: ' + MFCarray[3].get()['gas'])
    return

#Obtain all data from all MFCs
def mfcGetAll(MFCarray):
    mfcData = []
    currentStateMFC1 = MFCarray[0].get()
    mfcData.append(currentStateMFC1)
    currentStateMFC2 = MFCarray[1].get()
    mfcData.append(currentStateMFC2)
    currentStateMFC3 = MFCarray[2].get()
    mfcData.append(currentStateMFC3)
    currentStateMFC4 = MFCarray[3].get()
    mfcData.append(currentStateMFC4)
    
    return mfcData

def mfcGetOne(MFCarray, mfcNumber):
    mfcData = MFCarray[mfcNumber].get()
    return mfcData


#Loop to obtain current flow rate
def currentFlowRate(MFCarray):
    mfcFlowRate = []
    currentStateMFC1 = MFCarray[0].get()
    mfcFlowRate.append(currentStateMFC1['mass_flow'])
    currentStateMFC2 = MFCarray[1].get()
    mfcFlowRate.append(currentStateMFC2['mass_flow'])
    currentStateMFC3 = MFCarray[2].get()
    mfcFlowRate.append(currentStateMFC3['mass_flow'])
    currentStateMFC4 = MFCarray[3].get()
    mfcFlowRate.append(currentStateMFC4['mass_flow'])

    #Leackage Check
    flowIn = sum(mfcFlowRate)-mfcFlowRate[3]
    leakageValue = flowIn - mfcFlowRate[3]
    leakagePercent = leakageValue/flowIn

    if leakagePercent > 0.02:
        print('Error: Leakage above 2%!!!')
    elif leakagePercent > 0.05:
        print('Error: 5% Leakage')
    elif leakagePercent > 0.1:
        print('Error: 10% leakage, system shutting down')
        zeroMFCFlowRate(MFCarray)     
        mfcFlowRate = []
        currentStateMFC1 = MFCarray[0].get()
        mfcFlowRate.append(currentStateMFC1['mass_flow'])
        currentStateMFC2 = MFCarray[1].get()
        mfcFlowRate.append(currentStateMFC2['mass_flow'])
        currentStateMFC3 = MFCarray[2].get()
        mfcFlowRate.append(currentStateMFC3['mass_flow'])
        currentStateMFC4 = MFCarray[3].get()
        mfcFlowRate.append(currentStateMFC4['mass_flow'])
    return mfcFlowRate

def updateSingleSetPoint(MFCarray, mfcNumber, newRate):
    print(MFCarray)
    print(int(mfcNumber))
    print(float(newRate))
    print(MFCarray[int(mfcNumber)])
    mfcToUpdate = MFCarray[int(mfcNumber)]
    mfcToUpdate.set_flow_rate(float(newRate))
    return

def updateMFCFlowSetPoint(MFCarray, setPointArray):
    MFCarray[0].set_flow_rate(round(setPointArray[0], 2),5)
    print('MFC1 Set')
    time.sleep(0.5)
    MFCarray[1].set_flow_rate(round(setPointArray[1], 2),5)
    time.sleep(0.5)
    print('MFC2 Set')
    MFCarray[2].set_flow_rate(round(setPointArray[2], 2),5)
    time.sleep(0.5)
    print('MFC3 Set')

    # print('MFC1 Gas: ' + MFCarray[0].get()['volumetric_flow'])
    # print('MFC2 Gas: ' + MFCarray[2].get()['volumetric_flow'])
    # print('MFC3 Gas: ' + MFCarray[2].get()['volumetric_flow'])
    return

#Sets all MFC values to zero
def zeroMFCFlowRate(MFCarray):
    MFCarray[0].set_flow_rate(00)
    time.sleep(0.1)
    MFCarray[1].set_flow_rate(00)
    time.sleep(0.1)
    MFCarray[2].set_flow_rate(00)
    time.sleep(0.1)
    
    # print('MFC1 Gas: ' + MFCarray[0].get()['volumetric_flow'])
    # print('MFC2 Gas: ' + MFCarray[2].get()['volumetric_flow'])
    # print('MFC3 Gas: ' + MFCarray[2].get()['volumetric_flow'])
    return
#Export results to csv
""" 
import csv
with open('data.csv', 'wb') a csvfile:
    fieldnames = ['MFC1_flowRate', 'MFC2_flowRate', 'MFC3_flowRate', 'MFC4_flowRate']
    dataWriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
dataWriter.writeheader()

dataWriter.writerow({'MFC1_flowRate': 'Data', 'MFC2_flowRate': 'Data2', 'MFC3_flowRate': 'Data3', 'MFC4_flowRate': 'Data4'}) """