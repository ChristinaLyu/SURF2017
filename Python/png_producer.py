'''
    File:           png_producer.py
    Author:         Christina Lyu
    Date created:   5/25/17
    Updates: 	    
    Last modified:  5/26/17
    Python Version: 3.2

    Description:    runs tester.py and produce plots based on the csv files it produces
    Run format:     python png_producer.py pathToTesterFile pathToInputPythonFile interrupt_time pathToOutputFile 
    Run example:    python png_producer.py /Users/xxx/abc.py 20 /Users/xxx/abc.txt
'''

import os
import sys


inputPythonFilePath = sys.argv[1]
inputDataFolderPath = sys.argv[2]
executeTime = sys.argv[3]
outputFolderPath = sys.argv[4]

testerCommand = 'python ../Python/tester.py ' + inputPythonFilePath + ' ' + inputDataFolderPath + ' ' + executeTime + ' ' + outputFolderPath
os.system(testerCommand)

testerResult = outputFolderPath + '/testerResult.csv'
badResult = outputFolderPath + '/badResult.csv'
timing = outputFolderPath + '/timingFile.csv'
print testerResult
pieCommand = 'RScript /Users/ChristinaLyu/Git/christina_summer_2017/R/pieChartCreator.R ' + testerResult + ' /Users/ChristinaLyu/Git/christina_summer_2017/Run/Output/Xml/PNG/testerResult.png'
os.system(pieCommand)

badCommand = 'RScript /Users/ChristinaLyu/Git/christina_summer_2017/R/pieChartCreator.R ' + badResult + ' /Users/ChristinaLyu/Git/christina_summer_2017/Run/Output/Xml/PNG/badResult.png'
os.system(badCommand)

timingCommand = 'RScript /Users/ChristinaLyu/Git/christina_summer_2017/R/basicRuntimePlot.R ' + timing + ' /Users/ChristinaLyu/Git/christina_summer_2017/Run/Output/Xml/PNG/runTime.png'
os.system(timingCommand)
