'''
    File:           pdb_jmol_to_bnd.py
    Author:         Ileana Streinu with Christina Lyu
    Date created:   4/26/17
    Updates: 	    
    Last modified:  4/26/17
    Python Version: 2.7

    Description:    runs jmol on a pdb file, then extracts the atoms and bonds in an xml bnd format
    Run format:     python pdb_jmol_to_bnd.py pathToInputPdbFile pathToOutputJsonFile
    Run example:    python pdb_jmol_to_bnd.py /Users/xxx/abc.pdb /Users/xxx/abc.json
'''

import sys
import os
import subprocess
from pathDependencies import JMOLDATA_JAR

CHRISTINA_PYTHON=''


# print 'CHRISTINA_PYTHON='+CHRISTINA_PYTHON

inputPdbFilePath = sys.argv[1]
outputFilePath = sys.argv[2]
nrdash = outputFilePath.rfind('/')
outputFolderPath = outputFilePath[ : nrdash]
# print 'outputFolderPath='+outputFolderPath
outputFileName = outputFilePath[nrdash + 1: ]
# print 'outputFileName='+outputFileName

tempFolderPath = outputFolderPath +'/temp/'
if not os.path.exists(tempFolderPath):
    os.mkdir(tempFolderPath)

command_atom = 'java -jar ' + JMOLDATA_JAR + ' -no -j "load ' + inputPdbFilePath + ' ; select protein; getproperty atomInfo;" > '+tempFolderPath+ 'atominfo.txt'
command_bond = 'java -jar ' + JMOLDATA_JAR + ' -no -j "load ' + inputPdbFilePath + ' ; select protein; getproperty bondInfo;" > '+tempFolderPath+'bondinfo.txt'
child_atom = subprocess.Popen(command_atom, stderr = subprocess.STDOUT, stdout = subprocess.PIPE, shell = True)
stream_atom = child_atom.communicate()[0]
if 'ERROR' in stream_atom:
    sys.stderr.write('Error in jmol')
    sys.exit(2)
child_bond = subprocess.Popen(command_atom, stderr = subprocess.STDOUT, stdout = subprocess.PIPE, shell = True)
stream_bond = child_atom.communicate()[0]
if 'ERROR' in stream_bond:
    sys.stderr.write('Error in jmol')
    sys.exit(2)
os.system('python '+CHRISTINA_PYTHON+'/atom_bond_info_to_bnd.py '+tempFolderPath+'atominfo.txt '+tempFolderPath+'bondinfo.txt ' + outputFilePath)









