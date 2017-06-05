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

ind1 = pdbFile.find('ATOM      1')
atoms = pdbFile[ind1: ]

splited = atoms.splitlines()
m = 0
for k in range(len(splited)):
    if splited[k].find('ATOM') == -1 and splited[k].find('HETATM') == -1:
        if k != len(splited) - 1:
            if splited[k+1].find('ATOM') == -1 and splited[k+1].find('HETATM') == -1:
                m = k
                break
        else:
            m = k
splited = splited[ : m]
listR = []
listI = [0]

for n in range(len(splited)):

    if splited[n].find('ATOM') != -1 and n != 0 and n != len(splited)-1:
        line = splited[n]
        nextline = splited[n + 1]

        cleanL = line.split(' ')
        while cleanL.count('') != 0:
            cleanL.remove('')
        cleanN = nextline.split(' ')
        while cleanN.count('') != 0:
            cleanN.remove('')

        crtRes = cleanL[3]
        nxtRes = cleanN[3]
        if crtRes != nxtRes:
            listI.append(n)
            listI.append(n + 1)
            listR.append(crtRes)

    if n == len(splited) - 1:
        line = splited[n]
        cleanL = line.split(' ')
        while cleanL.count('') != 0:
            cleanL.remove('')
        res = cleanL[3]
        listR.append(res)
        listI.append(n)

residule = '0'
Num = 0

print len(listI)
print len(listR)

for j in range(len(listR)):
    residue = listR[j]
    startIn = listI[2*j]
    endIn = listI[2*j + 1]
    previousL = listR[ :j]
    index = previousL.count(residue) + 1
    newFile = folderPath + '/' + pdbInd + '_' + residue + '_' + str(index) + '.pdb'
    newFile = open(newFile, 'w')
    atomlist = '\n'.join(splited[startIn:endIn + 1])
    newFile.write(atomlist)

