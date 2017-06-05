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
residueName = sys.argv[3]

pdbName = pdbPath.split('/')[-1]
pdbInd = pdbName.split('.')[0]

pdbFile = open(pdbPath, 'r')
pdbFile = pdbFile.read()

atoms = pdbFile.splitlines()
atomIn = []
for a in range(len(atoms)):
    line = atoms[a]
    if line[ :4] == 'ATOM':
        atomIn.append(a)
    if line[ :6] == 'HETATM':
        atomIn.append(a)
splited = atoms[atomIn[0]:atomIn[-1] + 1]

lis = []
for line in splited:
    if line.find('ATOM') != -1 and line.find(residueName) != -1:
        lis.append(line)

residule = '0'
Num = 0
newFile = folderPath + '/' + pdbInd + '_' + residueName.upper() + '_' + str(Num) + '.pdb'
while len(lis) != 0:
    first = lis[0]
    cleaned = first.split(' ')
    while cleaned.count('') != 0:
        cleaned.remove('')
    
    if cleaned[5] != residule:
        residule = cleaned[5]
        Num = Num + 1
        newFile = folderPath + '/' + pdbInd + '_' + residueName.upper() + '_' + str(Num) + '.pdb'
        File = open(newFile, 'w')
        File.write(first + '\n')
        lis.remove(first)
    else:
        File = open(newFile, 'a')
        File.write(first + '\n')
        lis.remove(first)
