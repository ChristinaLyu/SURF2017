'''
    File:           cif2out.py
    Author:         Christina Lyu
    Date created:   8/18/17
    Updates: 	    8/18/17
    Last modified:  8/22/17
    Python Version: 2.7

    Description:    extracts cell angles, lengths, the atoms and bonds from cif file
    Run format:     python cif2out.py pathToInputCifFile pathToOutputFolder
    Run example:    python cif2out.py /Users/xxx/ABW.cif /Users/Output/
'''
import os
import sys
from xml.etree.ElementTree import Element, SubElement, Comment
from xml.etree import ElementTree
from xml.dom import minidom

def main():
    
    inputFilePath = sys.argv[1]
    outputFolderPath = sys.argv[2]

    index1 = inputFilePath.rfind('/')
    inputFileName = inputFilePath[index1 + 1: ]

    index2 = inputFileName.split('.')
    inputLigandId = index2[0]
    outputFilePath = outputFolderPath + inputLigandId + '.out'

    atomFile = open(inputFilePath, 'r')
    infoLines = atomFile.read()
    infoList = infoLines.split(';')

    outputFile = open(outputFilePath, 'w')

    t = '\t'
    containAtoms = ''
    alpha = ''
    beta = ''
    gamma = ''
    a = ''
    b = ''
    c = ''
    for k in range(len(infoList)):
        lines = infoList[k]
        if lines.find('_cell_angle_alpha') != -1:
            lineL = lines.splitlines()
            for line in lineL:
                if line.find('_cell_angle_alpha') != -1:
                    if line.find('\t') != -1:
                        splited = line.split(t)
                    else:
                        splited = line.split(' ')

                    while splited.count('') != 0:
                        splited.remove('')
                    second = splited[1]
                    if second.find('(') != -1:
                        left = second.find('(')
                        alpha = second[ :left] + '000'
                    else:
                        alpha = second
                elif line.find('_cell_angle_beta') != -1:
                    if line.find('\t') != -1:
                        splited = line.split(t)
                    else:
                        splited = line.split(' ')
                    while splited.count('') != 0:
                        splited.remove('')
                    second = splited[1]
                    if second.find('(') != -1:
                        left = second.find('(')
                        beta = second[ :left] + '000'
                    else:
                        beta = second
                elif line.find('_cell_angle_gamma') != -1:
                    if line.find('\t') != -1:
                        splited = line.split(t)
                    else:
                        splited = line.split(' ')
                    while splited.count('') != 0:
                        splited.remove('')
                    second = splited[1]
                    if second.find('(') != -1:
                        left = second.find('(')
                        gamma = second[ :left] + '000'
                    else:
                        gamma = second
                elif line.find('_cell_length_a') != -1:
                    if line.find('\t') != -1:
                        splited = line.split(t)
                    else:
                        splited = line.split(' ')
                    while splited.count('') != 0:
                        splited.remove('')
                    
                    second = splited[1]
                    if second.find('(') != -1:
                        left = second.find('(')
                        a = second[: left] + '000'
                    else:
                        a = second
                elif line.find('_cell_length_b') != -1:
                    if line.find('\t') != -1:
                        splited = line.split(t)
                    else:
                        splited = line.split(' ')
                    while splited.count('') != 0:
                        splited.remove('')
                    second = splited[1]
                    if second.find('(') != -1:
                        left = second.find('(')
                        b = second[: left] + '000'
                    else:
                        b = second
                elif line.find('_cell_length_c') != -1:
                    if line.find('\t') != -1:
                        splited = line.split(t)
                    else:
                        splited = line.split(' ')
                    while splited.count('') != 0:
                        splited.remove('')
                    second = splited[1]
                    if second.find('(') != -1:
                        left = second.find('(')
                        c = second[ :left] + '000'
                    else:
                        c = second
            cellLine = a + t + b + t + c + t + alpha + t + beta + t + gamma + '\n'
            outputFile.write(cellLine)
        if lines.find('_atom_site') != -1:
            containAtoms = lines
    bondS = ''
    bondQ = []
    bondL = []
    atomQ = []
    atomL = []
    if containAtoms != '':
        atomS = ''
        atoms = containAtoms.split('loop_')
        for k in atoms:
            dashInd = k.find('_')
            if k[dashInd:dashInd + 16] == '_atom_site_label':
                atomS = k

            elif k[dashInd:dashInd + 28] == '_geom_bond_atom_site_label_1':

                bondS = k
        if bondS.find('\n') != -1:
            bondS = bondS.split('\n')
        else:
            bondS = bondS.split('\r')
        for bond in bondS:
            if bond.find('bond') != -1:
                bondQ.append(bond)
            else:
                bondL.append(bond)
        if atomS.find('\n') != -1:
            atomS = atomS.split('\n')
        else:
            atomS = atomS.split('\r')
        for atom in atomS:
            if atom.find('atom') != -1:
                atomQ.append(atom)
            else:
                atomL.append(atom)
    labelInd = -1
    xInd = -1
    yInd = -1
    zInd = -1
    if atomQ.count('_atom_site_label') != 0:
        labelInd = atomQ.index('_atom_site_label')
    else:
        labelInd = atomQ.index('_atom_site_label\r')
    if atomQ.count('_atom_site_fract_x') != 0:
        xInd = atomQ.index('_atom_site_fract_x')
    else:
        xInd = atomQ.index('_atom_site_fract_x\r')
    if atomQ.count('_atom_site_fract_y') != 0:
        yInd = atomQ.index('_atom_site_fract_y')
    else:
        yInd = atomQ.index('_atom_site_fract_y\r')
    if atomQ.count('_atom_site_fract_z') != 0:
        zInd = atomQ.index('_atom_site_fract_z')
    else:
        zInd = atomQ.index('_atom_site_fract_z\r')
    symInd = -1
    atomNo = []
    atomId = []
    i = 0
    if atomQ.count('_atom_site_type_symbol') != 0:
        symInd = atomQ.index('_atom_site_type_symbol')
    elif atomQ.count('_atom_site_type_symbol\r') != 0:
        symInd = atomQ.index('_atom_site_type_symbol\r')
    elif atomQ.count('_atom_site_type') != 0:
        symInd = atomQ.index('_atom_site_type')
    elif atomQ.count('_atom_site_type\r') != 0:
        symInd = atomQ.index('_atom_site_type\r')
    elif atomQ.count('_atom_site_symbol') != 0:
        symInd = atomQ.index('_atom_site_symbol')
    elif atomQ.count('_atom_site_symbol\r') != 0:
        symInd = atomQ.index('_atom_site_symbol\r')
    while atomL.count('') != 0:
        atomL.remove('')
    while atomL.count('\r') != 0:
        atomL.remove('\r')
    for atommm in atomL:
        splited = atommm.split(' ')
        while splited.count('') != 0:
            splited.remove('')
    
        i = i + 1
        atomNo.append(str(i))
        atomLabel = splited[labelInd]
        if atomLabel.find('(') != -1:
            ind = atomLabel.find('(')
            atomLabel = atomLabel[ :ind] + '000'
        atomId.append(atomLabel)
        atomX = splited[xInd]
        if atomX.find('(') != -1:
            ind = atomX.find('(')
            atomX = atomX[ :ind] + '000'
        atomY = splited[yInd]
        if atomY.find('(') != -1:
            ind = atomY.find('(')
            atomY = atomY[ :ind] + '000'
        atomZ = splited[zInd]
        if atomZ.find('(') != -1:
            ind = atomZ.find('(')
            atomZ = atomZ[ :ind] + '000'
        atomSym = ''
        if symInd != -1:
            atomSym = splited[symInd]
            if atomSym.find('(') != -1:
                ind = atomSym.find('(')
                atomSym = atomSym[ :ind]
        newLine = str(i) + t + atomLabel + '\t' + atomX + '\t' + atomY + '\t' + atomZ + '\t' + atomSym + '\n'
        outputFile.write(newLine)

    label1 = -1
    label2 = -1
    if bondQ.count('_geom_bond_atom_site_label_1') != 0:
        label1 = bondQ.index('_geom_bond_atom_site_label_1')
    else:
        label1 = bondQ.index('_geom_bond_atom_site_label_1\r')
    if bondQ.count('_geom_bond_atom_site_label_2') != 0:
        label2 = bondQ.index('_geom_bond_atom_site_label_2')
    else:
        label2 = bondQ.index('_geom_bond_atom_site_label_2\r')

    while bondL.count('') != 0:
        bondL.remove('')
    while bondL.count('\r') != 0:
        bondL.remove('\r')
    for bondd in bondL:
        splited = bondd.split(' ')
        while splited.count('') != 0:
            splited.remove('')
        bondId1 = splited[label1]
        bondId2 = splited[label2]
        ind1 = atomId.index(bondId1)
        ind2 = atomId.index(bondId2)
        bondNo1 = atomNo[ind1]
        bondNo2 = atomNo[ind2]
        bondLine = bondNo1 + t + bondNo2 + t + bondId1 + t + bondId2 + '\n'
        outputFile.write(bondLine)
    atomFile.close()
main()
