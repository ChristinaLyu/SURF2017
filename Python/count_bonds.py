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
import subprocess
 
inputFileName = sys.argv[1]
outputFileName = sys.argv[2]

jmolPath = '../External/JmolData.jar '
tempFolderPath = '/'.join(outputFileName.split('/')[:-1]) + '/temp'
if not os.path.exists(tempFolderPath):
    try:
        os.mkdir(tempFolderPath)
    except Exception:
        sys.exit(-1)

bondInfo = tempFolderPath + '/bondInfo.txt'
command = 'java -jar ' + jmolPath + '-no -j "load ' + inputFileName + ' ; select protein; getproperty bondInfo;" > ' + tempFolderPath + '/bondInfo.txt'
#command = 'java -jar ../External/JmolData.jar -no -j "load ../Data/Test_xml/5i4l.xml ; select protein; getproperty bondInfo;" > ../Run/Output/bondInfo4.txt'
child = subprocess.Popen(command, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, shell=True)
streamdata = child.communicate()[0]

if 'ERROR' in streamdata:
    sys.stderr.write('Error in jmol')
    sys.exit(2)

#command2 = 'python ../Python/oldUibi.py ' + tempFolderPath + '/bondInfo.txt ' + outputFileName
