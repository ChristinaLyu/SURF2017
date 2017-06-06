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
seqCode = sys.argv[4]

pdbName = pdbPath.split('/')[-1]
pdbInd = pdbName.split('.')[0]

pdbFile = open(pdbPath, 'r')
pdbFile = pdbFile.read()

atoms = pdbFile.splitlines()
atomIn = []
seList = []
splited = []
for a in range(len(atoms)):
    line = atoms[a]
    if line[ :4] == 'ATOM':
        atomIn.append(a)
    if line[ :6] == 'HETATM':
        atomIn.append(a)
    if line[ :6] == 'SEQRES':
        seList.append(a)

for c in atomIn:
    splited.append(atoms[c])

seqres = atoms[seList[0]:seList[-1] + 1]
resList = []
chainList = []
resIndex = []
resIn = 0
for line in seqres:
    clear = line.split(' ')
    while clear.count('') != 0:
        clear.remove('')
        chain = ' '.join(clear[1:3])
    if len(chain) == 3:
        chain = ' ' + chain
    if chain.count(' 1 ') != 0:
        resIn = 0
    for resid in clear[4:]:
        resList.append(resid)
        chainList.append(chain)
        resIn = resIn + 1
        resIndex.append(resIn)


if residueName != 'AllRes' and residueName != 'AllGrp':

    newChainList = []
    for resIndex in range(len(resList)):
        res = resList[resIndex]
        if res == residueName.upper():
            newChain = chainList[resIndex]
            newChainList.append(newChain)
        
    lis = []
    for line in splited:
        if line[17:20] == residueName.upper():
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
            if seqCode == 'seqres':
                chain = newChainList[0]
                seqLine = 'SEQRES  ' + chain + '  ' + residule + '  ' + residueName.upper()
                File.write(seqLine + '\n')
                newChainList.remove(chain)
            File.write(first + '\n')
            lis.remove(first)
        else:
            File = open(newFile, 'a')
            File.write(first + '\n')
            lis.remove(first)

if residueName == 'AllGrp':
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

    for j in range(len(listR)):
        residue = listR[j]
        startIn = listI[2*j]
        endIn = listI[2*j + 1]
        previousL = listR[ :j]
        resFile = folderPath + '/' + pdbInd + '_' + residue + '.pdb'
        if previousL.count(residue) == 0:
            newFile = open(resFile, 'w')
            if j < len(resList):
                seqLine = 'SEQRES  ' + chainList[j] + '  ' + str(resIndex[j]) + '  ' + residue
                newFile.write(seqLine + '\n')
            atomlist = '\n'.join(splited[startIn:endIn + 1])
            newFile.write(atomlist + '\n')
        else:
            existFile = open(resFile, 'a')
            atomlist = '\n'.join(splited[startIn:endIn + 1])
            existFile.write(atomlist + '\n')

if residueName == 'AllRes':
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

    for j in range(len(listR)):
        residue = listR[j]
        startIn = listI[2*j]
        endIn = listI[2*j + 1]
        previousL = listR[ :j]
        index = previousL.count(residue) + 1
        newFile = folderPath + '/' + pdbInd + '_' + residue + '_' + str(index) + '.pdb'
        newFile = open(newFile, 'w')

        if j < len(resList):
            seqLine = 'SEQRES  ' + chainList[j] + '  ' + str(resIndex[j]) + '  ' + residue
            newFile.write(seqLine + '\n')
        atomlist = '\n'.join(splited[startIn:endIn + 1])
        newFile.write(atomlist)
        newFile.close()

    
