from alicat import *
from flask import Flask, request, render_template, jsonify
from keithley2600 import Keithley2600, ResultTable
from myAlicat import *
from gasTable import *
#from dataLogger import *
#from keithley26xxControl import *
#from autoExperiment import *
import time
import datetime
import numpy as np
import threading
import random
import board
import busio
import visa
i2c = busio.I2C(board.SCL, board.SDA)
#from smuBeepMario import *
#from dataLogger import *

#Initialise common variables used across functions

MFCs = []
hotWireParams = [0.0301, 25, 8]
allData = []
automodeTrue = 1
automode = False
liveData = []

class smuDefaultSettings():
    pulseWidth = 1
    dutyRatio = 0.5
    currentLevel = 0

class tempVariableStore():
    dataLoggerMode = False
    resultsTable = None
    hotWireParams = [0.0301, 7, 25]
    mfcUpdating = False
    SMUUpdating = False
    SMUPulse = False

tempVarStore = tempVariableStore()
smuSettings = smuDefaultSettings()

""" Initialise Instruments
    Scripts below initialise MFCs using the myAlicat library and returns the 4 MFC objects as an array
    Keithley SMU 2602B initialised with a VISA py backend. On initialisation, 
 """

print("Initialising MFCs")
try:
    #MFC = FlowController(port='/dev/ttyUSB0', address='C')
    #MFC.set_gas('Air')
    MFCs = initialiseMFCs()
    print(MFCs)
    print("MFC Initialised")
except:
    print("MFCs not Conected")

SENSE_REMOTE = 1 # Set 1 for 4-wire measuement and 0 for 2-wire
try:
    keithSMU = Keithley2600('USB0::1510::9730::4366190\x00::0::INSTR') #VISA address
    print("SMU Initialised")
    print("Setting Defalts")
    print("4-Wire...")
    keithSMU.smua.source.output = keithSMU.smua.OUTPUT_OFF
    keithSMU.smua.sense = keithSMU.smua.SENSE_REMOTE
    keithSMU.smua.source.leveli = 0
    print("Done")
    print("Set Limit...")
    keithSMU.smua.source.func = keithSMU.smua.OUTPUT_DCAMPS
    keithSMU.smua.limitv = 2
    print("Done")
    keithSMU.playChord()
    print("SMU Initialisation Complete")
except:
    keithSMU = False
    #smuConected = False
    print('SMU Not conected')
#keithSMU = []
#SMUaddress = []
# Initialise adafruit adc's
try:
    import adafruit_ads1x15.ads1115 as ADS
    from adafruit_ads1x15.analog_in import AnalogIn
    ads = ADS.ADS1115(i2c)
    ads.gain = 4
    adcChan = [None]*2
    adcChan[0] = AnalogIn(ads, ADS.P0, ADS.P1) # Differential measurment on 2 channels
    #adcChan[1] = AnalogIn(ads, ADS.P1)
    adcChan[1] = AnalogIn(ads, ADS.P2, ADS.P3) # Differential measurment on 2 channels
    #adcChan[3] = AnalogIn(ads, ADS.P3)
    print("ADCs Initialised")
except:
    print("ADCs not connected")

# Class to initialise a thread for PWM operation of the keithley smu 
class pulsedCurrentThread(threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.signal = False
    def run(self):
        print("Pulsed Starting")
        while not self.signal:
            tempVariableStore.SMUUpdating = True
            keithSMU.smua.source.leveli = smuSettings.currentLevel
            tempVariableStore.SMUUpdating = False
            time.sleep(smuSettings.pulseWidth*smuSettings.dutyRatio)
            tempVariableStore.SMUUpdating = True
            keithSMU.smua.source.leveli = 0.0000001
            tempVariableStore.SMUUpdating = False
            time.sleep(smuDefaultSettings.pulseWidth*(1-smuSettings.dutyRatio))


class recordDataThread(threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.signal = False
    def run(self):
        global liveData
        sampleRate = 2
        results = tempVarStore.resultsTable
        prevDataThread = [None]*11
        while not self.signal:
            returnDataThread = []
            returnDataThread.append(datetime.datetime.utcnow().timestamp())
            if tempVariableStore.mfcUpdating == True:
                returnDataThread.append(prevDataThread[1])
                returnDataThread.append(prevDataThread[2])
                returnDataThread.append(prevDataThread[3])
                returnDataThread.append(prevDataThread[4])
            else:
                #print('Else')
                try:
                    returnDataThread.append(MFCs[0].get()['mass_flow'])
                except:
                    returnDataThread.append(prevDataThread[1])
                try:
                    returnDataThread.append(MFCs[1].get()['mass_flow'])
                except:
                    returnDataThread.append(prevDataThread[2])
                try:
                    returnDataThread.append(MFCs[2].get()['mass_flow'])
                except:
                    returnDataThread.append(prevDataThread[3])
                try:
                    returnDataThread.append(MFCs[3].get()['mass_flow'])
                except:
                    returnDataThread.append(prevDataThread[4])

            if tempVariableStore.SMUUpdating == True:
                returnDataThread.append(prevDataThread[5])
                returnDataThread.append(prevDataThread[6])
            else:
                returnDataThread.append(keithSMU.smua.measure.i())
                returnDataThread.append(keithSMU.smua.measure.v())

            HWResistance = returnDataThread[6]/returnDataThread[5]
            returnDataThread.append(HWResistance)
            #Temperature
            hotWireTemp = ((HWResistance/tempVariableStore.hotWireParams[1])-1)/tempVariableStore.hotWireParams[0]
            hotWireTemp = hotWireTemp + tempVariableStore.hotWireParams[2]
            returnDataThread.append(hotWireTemp)

            returnDataThread.append(adcChan[0].voltage)
            returnDataThread.append(adcChan[1].voltage)
            liveData = returnDataThread
            prevDataThread = []
            prevDataThread = returnDataThread
            tempVarStore.testResultsTable.append_row(returnDataThread)
            time.sleep(1/sampleRate)
        print('Ending Thread')
        print('Saving Data')
        try:
            tempVarStore.testResultsTable.save('//home/GRJ/Documents/3_testDir/testData')
        except:
            print('TXT save failed')
        try:
            tempVarStore.testResultsTable.save_csv('//home/GRJ/Documents/3_testDir/testData2')
        except:
            print('CSV save failed')
        print('Data Saved!')

class autoMFCThread(threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.signal = False
    def run(self):
        while not self.signal:
            testPlanArray = importGasTableComplex()
            print(testPlanArray)
            numSteps = testPlanArray.shape[0]
            print(numSteps)
            for testStepNumber in range(0,numSteps):
                a = []
                currentTest = testPlanArray.iloc[testStepNumber]
                a.append(currentTest.MFC1)
                a.append(currentTest.MFC2)
                a.append(currentTest.Humidity)
                print(a)
                tempVariableStore.mfcUpdating = True
                time.sleep(0.1)
                try:
                    MFCs[0].flush()
                    MFCs[0].set_flow_rate(round(currentTest.MFC1, 2),5)
                    MFCs[0].flush()
                    print('MFC1 Set')
                except:
                    print("MFC1 Fail")
                time.sleep(0.1)
                try:
                    MFCs[1].flush()
                    MFCs[1].set_flow_rate(round(currentTest.MFC2, 2),5)
                    MFCs[1].flush()
                    print('MFC2 Set')
                except:
                    print("MFC2 Fail")
                time.sleep(0.1)
                try:
                    MFCs[2].flush()
                    MFCs[2].set_flow_rate(round(currentTest.Humidity, 2),5)
                    MFCs[2].flush()
                    print('MFC3 Set')
                except:
                    print("MFC3 Fail")
                time.sleep(0.1)
                tempVariableStore.mfcUpdating = False
                #Set wait time
                time.sleep(currentTest.Time)
            
            tempVariableStore.SMUUpdating = True
            keithSMU.playChord(notes=('G6','E6','C6'))
            tempVariableStore.SMUUpdating = False
            print("End of Test")
            break

class fullAutoThread(threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.signal = False
    def run(self):
        while not self.signal:
            mfcTestPlan, HWTestPlan = importGasTableFullAuto()
            print(HWTestPlan)
            numSteps = HWTestPlan.shape[0]
            print(numSteps)
            for testHWStepNumber in range(0,numSteps):
                currentHWTest = HWTestPlan.iloc[testHWStepNumber]
                smuSettings.currentLevel = currentHWTest.HWCurrent
                time.sleep(currentHWTest.HWSettleTime)

                numSteps2 = mfcTestPlan.shape[0]
                for testMFCStepNumber in range(0, numSteps2):
                    a = []
                    currentTest = mfcTestPlan.iloc[testMFCStepNumber]
                    a.append(currentTest.MFC1)
                    a.append(currentTest.MFC2)
                    a.append(currentTest.MFC3)
                    print(a)
                    tempVariableStore.mfcUpdating = True
                    try:
                        MFCs[0].flush()
                        MFCs[0].set_flow_rate(round(currentTest.MFC1, 2),5)
                        MFCs[0].flush()
                        print('MFC1 Set')
                    except:
                        print("MFC1 Fail")
                    time.sleep(0.1)
                    try:
                        MFCs[1].flush()
                        MFCs[1].set_flow_rate(round(currentTest.MFC2, 2),5)
                        MFCs[1].flush()
                        print('MFC2 Set')
                    except:
                        print("MFC2 Fail")
                    time.sleep(0.1)
                    try:
                        MFCs[2].flush()
                        MFCs[2].set_flow_rate(round(currentTest.MFC3, 2),5)
                        MFCs[2].flush()
                        print('MFC3 Set')
                    except:
                        print("MFC3 Fail")
                    time.sleep(0.1)
                    tempVariableStore.mfcUpdating = False
                    #Set wait time
                time.sleep(currentTest.Time)
            
            tempVariableStore.SMUUpdating = True
            keithSMU.playChord(notes=('G6','E6','C6'))
            tempVariableStore.SMUUpdating = False
            print("End of Test")
            break


app = Flask(__name__)

@app.route("/", methods= ['GET', 'POST'])
def index():
    print("Page Loaded")
    return render_template('master.html')

@app.route("/setParams", methods=['POST'])
def setParams():
    testParams=[None]*5
    testParams[0] = float(request.form["tcrVal"])
    testParams[1] = float(request.form["r0Val"])
    testParams[2] = float(request.form["t0Val"])
    testParams[3] = request.form["testNameVal"]
    testParams[4] = request.form["userNameVal"]
    tempVariableStore.hotWireParams[0] = testParams[0]
    tempVariableStore.hotWireParams[1] = testParams[1]
    tempVariableStore.hotWireParams[2] = testParams[2]
    params = {'recorded': time.asctime(), 'TCR':testParams[0] , 'R0':testParams[1], 'T0':testParams[2], 'Test Name':testParams[3], 'Username':testParams[4]}
    tempVarStore.testResultsTable= ResultTable(column_titles=['Time','MFC1', 'MFC2', 'MFC3', 'MFC4', 'current', 'voltage', 'resistance', 'temperature', 'adc1', 'adc2'], units=['time', 'SCLPM', 'SCLPM', 'SCLPM', 'SCLPM', 'A', 'V', 'ohm', 'degC', 'V', 'V'], params=params)
    print(tempVarStore.testResultsTable)
    return('',204)

@app.route("/updateMFC", methods = ['POST'])
def updateMFCValues():
    print("Im in the Flask")
    flowRate = request.form["flowRate"]
    mfcIndex = request.form["mfcIndex"]
    updateSingleSetPoint(MFCs, mfcIndex, flowRate)
    return (flowRate)

""" @app.route("/updateMFC", methods = ['POST'])
def updateMFCValues():
    #print("Im in the Flask")
    #print(tempVarStore.testResultsTable)
    flowRate = '1'
    return (flowRate) """

@app.route("/increaseMFC", methods = ['POST'])
def increaseFlowRate():
    mfcIndex = request.form["mfcIndex"]
    singleMFCData = mfcGetOne(MFCs, mfcIndex)
    currentFlowRate = singleMFCData['mass_flow']
    newFlowRate = currentFlowRate + 1
    updateSingleSetPoint(MFCs, mfcIndex, newFlowRate)
    return()

@app.route("/decreaseMFC", methods = ['POST'])
def decreaseFlowRate():
    mfcIndex = request.form["mfcIndex"]
    singleMFCData = mfcGetOne(MFCs, mfcIndex)
    currentFlowRate = singleMFCData['mass_flow']
    newFlowRate = currentFlowRate - 1
    updateSingleSetPoint(MFCs, mfcIndex, newFlowRate)
    return()

@app.route("/setMFCGas", methods = ['POST'])
def setNewGas():
    mfcIndex = request.form["mfcIndex"]
    mfcIndex = int(mfcIndex)
    newGas = request.form["newGas"]
    #print(newGas)
    #print(type(newGas))
    try:
        print("Trying")
        MFCs[mfcIndex].set_gas(newGas)
        print("Success")
    except:
        print("Failed")
    return('', 204)

@app.route("/updateMultiMFC", methods = ['POST'])
def updateMultiMFCValues():

    flowRate1 = request.form["flowRate1"]
    flowRate2 = request.form["flowRate2"]
    flowRate3 = request.form["flowRate3"]
    MFCs[0].set_flow_rate(round(float(flowRate1)))
    MFCs[1].set_flow_rate(round(float(flowRate2)))
    MFCs[2].set_flow_rate(round(float(flowRate3)))
    return ('', 204)


@app.route("/getMFCInfo", methods = ['GET'])
def getMFCInfo():
    a = mfcGetAll(MFCs)
    print(a)
    return jsonify(a)

@app.route("/mfcShutdown", methods = ['GET'])
def mfcShutdown():
    print("MFCs Shutting Down")
    zeroMFCFlowRate(MFCs)
    return()

@app.route("/updateSMUCurrent", methods = ['POST'])
def updateSMUCurrent():
    a = request.form["newCurrent"]
    #b = request.form["newVoltage"]
    a = float(a)
    #smuSettings.currentLevel = a
    source = request.form["source"]
    #SMU_level(keithSMU, 1, str(a))
    print(source)
    int(source)
    print(a)
    if source == 1:
        print("Setting Voltage")
        keithSMU.smua.source.levelv = a
    else:
        if float(a) > 0.1:
            a=0.1
        keithSMU.smua.source.leveli = a
        smuSettings.currentLevel = a
        print("I Set")
    #keithSMU.applyCurrent(keithSMU.smua, str(a))
    return ('', 204)

@app.route("/updateSMUPeriod", methods = ['POST'])
def updateSMUPeriod():
    a = request.form["newPeriod"]
    a = float(a)
    smuSettings.pulseWidth = a
    return('', 204)

@app.route("/updateSMUDutyRatio", methods = ['POST'])
def updateSMUDutyRatio():
    a = request.form["newRatio"]
    a = float(a)
    smuSettings.dutyRatio = a
    return('', 204)

@app.route("/smuOutputPulse", methods = ['POST'])
def setOutputPulseMode():
    pulseState = request.form["smuPulseState"]
    print(pulseState)
    if pulseState == '1':
        print(pulseState)
        pulsedCurrentThread
        tempVarStore.SMUPulse = True
        smuPulseThread=pulsedCurrentThread(1, 'pulseCurrent', 1)
        smuPulseThread.signal = False
        smuPulseThread.start()
        tempVarStore.smuPulseThread = smuPulseThread
    else:
        smuPulseThread = tempVarStore.smuPulseThread
        smuPulseThread.signal = True
        smuPulseThread.join()
        tempVarStore.SMUPulse = False
    return('', 204)


@app.route("/smuOnOff", methods = ['POST'])
def changeSMUOutputState():
    print("SMU On Off Route")
    a = request.form["smuOutputState"]
    #SMU_Output(keithSMU, a)
    print(a)
    if a == '1':
        print("SMU On")
        keithSMU.smua.source.output = keithSMU.smua.OUTPUT_ON
        keithSMU.playChord()
    else:
        keithSMU.smua.source.output = keithSMU.smua.OUTPUT_OFF
        keithSMU.playChord(notes=('G6','E6','C6'))
    return (a)

@app.route("/smuSourceSelect", methods = ['POST'])
def changeSMUSourceType():
    print("Set SMU Source")
    a = request.form["source"]
    print(a)
    if a == 1:
        print("Changed to volts")
        keithSMU.smua.source.func = keithSMU.smua.OUTPUT_DCVOLTS
    else:
        keithSMU.smua.source.func = keithSMU.smua.OUTPUT_DCAMPS
    return (a)

@app.route("/smuSenseSelect", methods = ['POST'])
def changeSMUSenseMode():
    print("SMU Sense Mode")
    a = request.form["senseMode"]
    if a == "2wire":
        #SMU_setSense(keithSMU, 0)
        keithSMU.smua.sense = keithSMU.smua.SENSE_LOCAL
    else:
        #SMU_setSense(keithSMU, 1)
        keithSMU.smua.sense = keithSMU.smua.SENSE_REMOTE
    return (a)

@app.route("/updateCompliance", methods = ['POST'])
def updateComplianceLimit():
    print("Updating Compliance")
    newLimit = request.form["newLimit"]
    limitType = float(request.form["limitType"])
    print(limitType)
    print(newLimit)

    SMU_limit(keithSMU, limitType, newLimit)
    return ('', 204)

@app.route("/autoExperimentModeStart", methods = ['POST'])
def startAutoMode():
    autoMFCMode = autoMFCThread(2, 'autoMFC', 1)
    autoMFCMode.signal = False
    autoMFCMode.start()
    tempVarStore.autoMFCMode = autoMFCMode
    return ('', 204)

@app.route("/autoExperimentModeStop", methods = ['POST'])
def stopAutoMode():
    autoMFCMode = tempVarStore.autoMFCMode
    autoMFCMode.signal = True
    autoMFCMode.join()
    zeroMFCFlowRate(MFCs)
    print('Thread Ended')
    return ('', 204)

@app.route("/runDataLogger", methods = ['POST'])
def runDataLogger():
    dataRecordState = request.form["dataRecordState"]
    if dataRecordState == '1':
        tempVarStore.dataLoggerMode = True
        dataLoggerThread=recordDataThread(1, 'logData', 1)
        dataLoggerThread.signal = False
        print(tempVarStore.dataLoggerMode)
        dataLoggerThread.start()
        tempVarStore.dataLogThread = dataLoggerThread
    else:
        dataLoggerThread = tempVarStore.dataLogThread
        dataLoggerThread.signal = True
        dataLoggerThread.join()
        tempVarStore.dataLoggerMode = False
    return('', 204)

@app.route("/recordData", methods = ['POST'])
def recordData():
    #If record is not set, poll, else, read from global variable
    if tempVarStore.dataLoggerMode == False:
        try:
            returnData = []
            #Time Stamp
            returnData.append(datetime.datetime.now())
            #MFCs
            if tempVariableStore.mfcUpdating == True:
                returnData.append(prevData[1])
                returnData.append(prevData[2])
                returnData.append(prevData[3])
                returnData.append(prevData[4])
            else:
                #print('Geting MFC1')
                returnData.append(MFCs[0].get())
                #print('Geting MFC2')
                returnData.append(MFCs[1].get())
                #print('Geting MFC3')
                returnData.append(MFCs[2].get())
                #print('Geting MFC4')
                returnData.append(MFCs[3].get())
            #SMU
            #returnData.append(random.randint(0,5000)/1000)
            #returnData.append(random.randint(0,5))
            try:
                returnData.append(keithSMU.smua.measure.i())
                voltageMeas = keithSMU.smua.measure.v()
                returnData.append(voltageMeas)
                HWResistance = returnData[6]/returnData[5]
                if voltageMeas < 0.1:
                    try:
                        HWResistance = prevData[7]
                    except:
                        HWResistance = HWResistance
                returnData.append(HWResistance)
            except:
                returnData.append(5)
                returnData.append(5)
                returnData.append(5)

            #Temperature
            hotWireTemp = ((HWResistance/tempVariableStore.hotWireParams[1])-1)/tempVariableStore.hotWireParams[0]
            hotWireTemp = hotWireTemp + tempVariableStore.hotWireParams[2]
            returnData.append(hotWireTemp)
            #ADC
            returnData.append(adcChan[0].voltage)
            returnData.append(adcChan[1].voltage)
            prevData = []
            prevData = returnData

        except:
            returnData = []
            print('error')
            #returnData = prevData
    else:
        global liveData
        returnData = liveData
        print(returnData)
    
    return jsonify(returnData)

@app.route("/playStarWars", methods = ['POST'])
def playSW():
    killDataReading.set()
    autoModeThread.join()
    return ('', 204)
#   print("PLay")
#   playTune(keithSMU)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)


""" 
PID Code


@app.route("/updatePIDCoefficients", methods = ['POST'])
def updatePIDCoefficients():
    newValue = request.form["newValue"]
    coefficient = request.form["coefficient"]
    if coefficient == "P":
        print("Change P")
    elif coefficient == "I":
        print("Change I")
    elif coefficient == "D":
        print("Change D")
    else:
        return
    return

@app.route("/setPIDOutputLimits", methods = ['POST'])
def setPIDOutputLimits():
    min = request.form["PIDOutMin"]
    max = request.form["PIDOutMax"]
    return

@app.route("/setPIDTargetTemperature", methods = ['POST'])
def setPIDTargetTemperature():
    newTemp = request.form["newTemperature"]
    print(newTemp)
    return """



""" 
def recordExperiementData(stop_event, MFCarray, keithSMU, adcChan):
    global liveData
    sampleRate = 5 #Set as desired, default 5
    while not stop_event.isSet():
        returnData = []
        returnData.append(datetime.datetime.now())
        #MFCs
        returnData.append(MFCarray[0].get())
        returnData.append(MFCarray[1].get())
        returnData.append(MFCarray[2].get())
        returnData.append(MFCarray[3].get())
        #SMU
        returnData.append(keithSMU.smua.measure.i())
        returnData.append(keithSMU.smua.measure.v())
        returnData.append(returnData[5]/returnData[4])
        #ADC
        returnData.append(adcChan[0].voltage)
        returnData.append(adcChan[1].voltage)
        returnData.append(adcChan[2].voltage)
        returnData.append(adcChan[3].voltage)

        resultsTableToSave.append_row(returnData)
        liveData = returnData """



""" def getDataAuto(stop_event, MFCarray, keithSMU):
    global liveData
    sampleRate = 5
    while not stop_event.isSet():
        #print('In the thread')
        start_time = time.time()
        #print(start_time)
        #Poll MFCs
        deviceData = []
        deviceData.append(datetime.datetime.now())
        currentStateMFC1 = MFCarray[0].get()
        deviceData.append(currentStateMFC1)
        currentStateMFC2 = MFCarray[1].get()
        deviceData.append(currentStateMFC2)
        currentStateMFC3 = MFCarray[2].get()
        deviceData.append(currentStateMFC3)
        currentStateMFC4 = MFCarray[3].get()
        deviceData.append(currentStateMFC4)
        #Poll SMU
        deviceData.append(keithSMU.ask("print(smua.measure.i())"))
        deviceData.append(keithSMU.ask("print(smua.measure.v())"))

        liveData = deviceData
        #print(liveData)
        end_time = time.time()
        #print(end_time)
        time_elapsed = end_time - start_time
        #print(time_elapsed)
        time_elapsed = time_elapsed * 1000
        if time_elapsed < (1/sampleRate):
            if time_elapsed < 0:
                time.sleep(0)
            else:
                time.sleep(time_elapsed - 1/sampleRate)
    print('Data not recording') """



#killAutoMode = threading.Event()
#killSMUPID = threading.Event()
#killDataReading = threading.Event()
#autoModeThread = threading.Thread(target=beginExperiment, args=(killAutoMode, MFCs))
#SMUPIDThread = threading.Thread(target=beginExperiment, args=(killSMUPID, keithSMU))
#dataReadingThread = threading.Thread(target=getDataAuto, args=(killDataReading, MFCs, keithSMU))
#dataReadingThread.start()