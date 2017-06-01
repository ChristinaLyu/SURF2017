__author__ = 'Christina Lyu'

import os
import sys
import subprocess
from os.path import isfile
import signal
import time
   
# -----------------------------------------------------------------------------
# Extract the atom label of PRO residue from an input pdb file
# -----------------------------------------------------------------------------
# Input: 
#       inputFile: path to folder with .pdb files containing one or more PRO residues
#       outputFolder: path to the output folder where a _PRO_n.txt file will be created
# Description: extracts only the atom label from the ATOM lines
# --------------------------------------------------------------------

inputDataPath = sys.argv[1]
outputFolderPath = sys.argv[2]

command1 = 'python ../Python/extract_PRO.py '
for crtInputFile in os.listdir(inputDataPath):
    if isfile(crtInputFile):
        continue
    crtInputFilePath = inputDataPath + '/' + crtInputFile
    os.system(command1 + crtInputFilePath + ' ' + outputFolderPath)

command2 = 'python ../Python/extract_PRO_pattern.py '
for newInputFile in os.listdir(outputFolderPath):
    if isfile(newInputFile):
        continue

    newInputFilePath = outputFolderPath + '/' + newInputFile
    os.system(command2 + newInputFilePath + ' ' + outputFolderPath)
