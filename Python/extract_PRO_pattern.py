__author__ = 'Christina Lyu'

import sys
import os
   
# -----------------------------------------------------------------------------
# Extract the atom label from an input pdb file
# -----------------------------------------------------------------------------
# Input: 
#       inputFile: path to a .pdb file containing one or more atoms
#       outputFolder: path to the output folder where a _PRO_n.txt file will be created
# Description: extracts only the atom label from the ATOM lines
# --------------------------------------------------------------------

inputFilePath = sys.argv[1]
outputFolder = sys.argv[2]

inputFile = open(inputFilePath, 'r')
inFile = inputFile.read()
inFile = inFile.splitlines()

outFileName = inputFilePath.split('/')[-1]
outFileName = outFileName.split('.')[0] + '.txt'
outFilePath = outputFolder + '/' + outFileName

outFile = open(outFilePath, 'w')

for line in inFile:
    splited = line.split(' ')
    while splited.count('') != 0:
        splited.remove('')
    
    label = splited[2]
    outFile.write(label + '\n')



