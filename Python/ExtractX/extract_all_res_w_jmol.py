__author__ = 'Christina Lyu'

import sys
import os
   
# -----------------------------------------------------------------------------
# Extract all residues from an input pdb file
# -----------------------------------------------------------------------------
# Input: 
#       inputFile: path to a .pdb file containing one or more PRO residues
#       outputFolder: path to the output folder where a ABC_n.pdb file will be created
# TODO: check what happens if there is no protein chain in the input file, or for dna, rna etc.
#
# Description: extracts only the atoms with all residues from the ATOM lines
# TODO: check if it retains the SEQRES and other lines from the input pdb file
# --------------------------------------------------------------------

# JMOL_JAR = '/Users/ChristinaLyu/Git/christina_summer_2017/External/Jmol.jar'
from pathDependencies import JMOLDATA_JAR

pdbPath = sys.argv[1]
folderPath = sys.argv[2]
residue = sys.argv[3]

pdbName = pdbPath.split('/')[-1]
pdbInd = pdbName.split('.')[0]

pdbFile = open(pdbPath, 'r')
pdbFile = pdbFile.read()

#residueList = ['ALA', 'ARG', 'ASN', 'ASP', 'CYS', 'GLN', 'GLU', 'GLY', 'HIS', 'ILE', 'LEU', 'LYS', 'MET', 'PHE', 'PRO', 'SER', 'THR', 'TRP', 'TYR', 'VAL', 'ASX', 'GLX', 'UNK']
tempFolderPath = folderPath + '/temp'
if not os.path.exists(tempFolderPath):
    os.mkdir(tempFolderPath)
try:
    outFile = folderPath + '/' + pdbInd + '_' + residue + '.pdb'
    # tempFile = tempFolderPath + '/atomInfo.txt'
    tempFile = tempFolderPath + '/' + residue + 'Atoms.pdb'
    # command = 'java -jar ' + JMOLDATA_JAR + ' -no -j "load ' + pdbPath + ' ; select ' + residue + '; getproperty atomInfo;" > '+tempFile
    # command = 'java -XX:-UseGCOverheadLimit -jar ' + JMOLDATA_JAR + ' -n -j ' + "'" + 'load ' + pdbPath + '; select ' + residue + '; x=write("PDB"); write VAR x "' + tempFile2 + '";' + "'"
    command = 'java -XX:-UseGCOverheadLimit -jar ' + JMOLDATA_JAR + ' -n -j ' + "'" + 'load ' + pdbPath + '; select ' + residue + '; x=write("PDB"); write VAR x "' + tempFile + '";' + "'"
    
    os.system(command)
    tempFile2 = open(tempFile, 'r')
    tempFile2 = tempFile2.read()
    tempFile2 = tempFile2.splitlines()
    resNo = '0'
    fileNo = 0

    for m in range(len(tempFile2)):
        atom = tempFile2[m]
        clean = atom.split(' ')
        while clean.count('') != 0:
            clean.remove('')
        if clean[0] == 'ATOM':
            resId = clean[5]
            if resNo != resId:
                resNo = resId
                fileNo = fileNo + 1
                newFileName = folderPath + '/' + pdbInd + '_' + residue + '_' + fileNo + '.pdb'
                newFile = open(newFileName, 'w')
                newFile.write(atom + '\n')
                newFile.close()
            else:
                existFileName = folderPath + '/' + pdbInd + '_' + residue + '_' + fileNo + '.pdb'
                existFile = open(existFileName, 'a')
                existFile.write(atom + '\n')
                existFile.close()
except IOError:
    sys.exit(-1)

