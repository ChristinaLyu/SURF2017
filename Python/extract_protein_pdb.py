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

newFile = folderPath + '/' + pdbInd + '_protein.pdb'
newFile = open(newFile, 'w')
newFile.close()

atoms = pdbFile.splitlines()
atomIn = []
seList = []
splited = []
for a in range(len(atoms)):
    line = atoms[a]
    if line[ :4] == 'ATOM':
        atomIn.append(a)
   
for c in atomIn:
    splited.append(atoms[c])

listR = []
listI = [0]
listE = []

for n in range(len(splited)):
    line = splited[n]
    if n == 0:
        line = splited[n]
        crtEle = line[13:16]
        listE.append(crtEle)
    if line[ :5] == 'ATOM ' and n != 0 and n != len(splited)-1:
        preline = splited[n-1]
        line = splited[n]
        nextline = splited[n + 1]

        preRes = preline[16:20]
        crtRes = line[16:20]
        nxtRes = nextline[16:20]

        preEle = preline[13:16]
        crtEle = line[13:16]
        nxtEle = nextline[13:16]
        crtEle = crtEle.replace(' ', '')

        if crtRes != preRes:
            listE.append(crtEle)
        else:
            listE[-1] = listE[-1] + crtEle
            
        if crtRes != nxtRes:
            listI.append(n)
            listI.append(n + 1)
            listR.append(crtRes)

            

    if n == len(splited) - 1:
        line = splited[n]
        res = line[16:20]
        ele = line[13:16]
        listR.append(res)
        listI.append(n)
        listE[-1] = listE[-1] + ele

residule = '0'
Num = 0

for j in range(len(listR)):
    residue = listR[j]
    startIn = listI[2*j]
    endIn = listI[2*j + 1]
    previousL = listR[ :j]
    element = listE[j]
    newFile = folderPath + '/' + pdbInd + '_protein.pdb'
    newFile = open(newFile, 'a')
    if element.find('NCACO') != -1:
        atomlist = '\n'.join(splited[startIn:endIn + 1]) + '\n'
        newFile.write(atomlist)
    newFile.close()
