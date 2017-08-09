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


pdbPath = sys.argv[1]
folderPath = sys.argv[2]

pdbName = pdbPath.split('/')[-1]
pdbInd = pdbName.split('.')[0]

pdbFile = open(pdbPath, 'r')
pdbFile = pdbFile.read()

newFileName = folderPath + '/' + pdbInd + '_not_sol.pdb'
newFile = open(newFileName, 'w')


atoms = pdbFile.splitlines()
atomIn = []
seList = []
splited = []
for a in range(len(atoms)):
    line = atoms[a]
    if line[ :5] == 'ATOM ':
        atomIn.append(a)
    if line[ :7] == 'HETATM ':
        atomIn.append(a)
for c in atomIn:
    splited.append(atoms[c])

for n in range(len(splited)):
    line = splited[n]
    res = line[16:20]
    if res.find('HOH') == -1:
        newFile.write(line + '\n')
newFile.close()
