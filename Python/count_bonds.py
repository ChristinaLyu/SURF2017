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
print outputFileName
try:
    if not os.path.exists(tempFolderPath):   
        os.mkdir(tempFolderPath)
    command = 'java -jar ' + jmolPath + '-no -j "load ' + inputFileName + ' ; select protein; getproperty bondInfo;" > ' + tempFolderPath + '/bondInfo.txt'
    
    child = subprocess.Popen(command, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, shell=True)
    streamdata = child.communicate()[0]
    rc = child.returncode
    if 'ERROR' in streamdata:
        sys.stderr.write('Error in jmol')
        sys.exit(2)
    if rc == 0:
        command_bond = 'python ../Python/OldUibi.py ' + tempFolderPath + '/bondInfo.txt ' + outputFileName
        print command_bond

        child_bond = subprocess.Popen(command_bond, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, shell=True)
        stream_bond = child_bond.communicate()[0]
        rc_bond = child_bond.returncode
        if rc_bond != 0:
            sys.exit(rc_bond)
except Exception:
    sys.exit(-1)
