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

from ConfigParser import SafeConfigParser
config = SafeConfigParser()
config.read('../../../Settings/configchristina.ini')
if config.has_section('paths'):
    JMOL_JAR = os.path.abspath(config.get('paths', 'path_to_jmol_jar_from_christina_python'))
    CHRISTINA_PYTHON=config.get('paths', 'path_to_christina_python')

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

os.system('java -jar ' + JMOL_JAR + ' -no -j "load ' + inputPdbFilePath + ' ; select protein; getproperty atomInfo;" > '+tempFolderPath+ 'atominfo.txt')
os.system('java -jar ' + JMOL_JAR + ' -no -j "load ' + inputPdbFilePath + ' ; select protein; getproperty bondInfo;" > '+tempFolderPath+'bondinfo.txt')
os.system('python '+CHRISTINA_PYTHON+'/atom_bond_info_to_bnd.py '+tempFolderPath+'atominfo.txt '+tempFolderPath+'bondinfo.txt ' + outputFilePath)









