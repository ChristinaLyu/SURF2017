'''
    File:           jmol_to_bond.py
    Author:         Ileana Streinu with Christina Lyu
    Date created:   5/19/17
    Updates: 	    
    Last modified:  5/19/17
    Python Version: 3.2

    Description:    takes a cif/pdbx file and executes Jmol to get the number of bonds
    Run format:     python jmol_to_bond.py pathToInputPythonFile pathToOutputFile
    Run example:    python jmol_to_bond.py /Users/xxx/abc.xx /Users/xxx/abc.txt
'''
import os
import sys

inputFileName = sys.argv[1]
outputFileName = sys.argv[2]

jmolPath = '../External/JmolData.jar '
tempFolderPath = '/'.join(outputFileName.split('/')[:-1]) + '/temp'
if not os.path.exists(tempFolderPath):
    os.mkdir(tempFolderPath)


command = 'java -jar ' + jmolPath + '-no -j "load ' + inputFileName + ' ; select protein; getproperty bondInfo;: > ' + tempFolderPath + 'bondInfo.txt'
os.system(command)
command2 = 'python ../Python/oldUibi.py ' + tempFolderPath + '/bondInfo.txt ' + outputFileName
os.system(command2)
