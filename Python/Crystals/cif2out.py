'''
    File:           cif2out.py
    Author:         Christina Lyu
    Date created:   8/18/17
    Updates: 	    8/18/17
    Last modified:  8/23/17
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

#-----------------------------------------------------------------      strim   ------
def strim(splited, index):
    item = splited[index]
    if item.find('(') != -1:
        ind = item.find('(')
        item = item[ :ind]
    return item

#-----------------------------------------------------------------      getIndex   ------
def getIndex(queue, keyword):
    if queue.count(keyword) != 0:
        Index = queue.index(keyword)
    else:
        Index = queue.index(keyword + '\r')
    return Index

#-----------------------------------------------------------------      getCellInfo   ------
def getCellInfo(line):
    if line.find('\t') != -1:
        splited = line.split('\t')
    else:
        splited = line.split(' ')
    while splited.count('') != 0:
        splited.remove('')
    second = splited[1]
    if second.find('(') != -1:
        left = second.find('(')
        cellInfo = second[ :left]
    else:
        cellInfo = second
    return cellInfo

#-----------------------------------------------------------------      getOutputFilePath   ------
def getOutputFilePath(inputFilePath, outputFolder, extension):
    index1 = inputFilePath.rfind('/')
    inputFileWExtension = inputFilePath[index1 + 1: ]
    index2 = inputFileWExtension.rfind('.')
    inputFileWtExtension = inputFileWExtension[ :index2]
    outputFilePath = outputFolder + inputFileWtExtension + extension
    return outputFilePath

#-----------------------------------------------------------------      main   ------
def main():
    # get input file and output path, then get output file
    inputFilePath = sys.argv[1]
    outputFolderPath = sys.argv[2]
    outputFilePath = getOutputFilePath(inputFilePath, outputFolderPath, '.out')
    atomFile = open(inputFilePath, 'r')
    lines = atomFile.read()
    outputFile = open(outputFilePath, 'w')
    # try to get the lines with cell infomations
    t = '\t'
    lineL = lines.splitlines()
    for line in lineL:
        if line.find('_cell_angle_alpha') != -1:
            alpha = getCellInfo(line)
        elif line.find('_cell_angle_beta') != -1:
            beta = getCellInfo(line)
        elif line.find('_cell_angle_gamma') != -1:
            gamma = getCellInfo(line)
        elif line.find('_cell_length_a') != -1:
            a = getCellInfo(line)
        elif line.find('_cell_length_b') != -1:
            b = getCellInfo(line)
        elif line.find('_cell_length_c') != -1:
            c = getCellInfo(line)
    # write cell info line
    cellLine = a + t + b + t + c + t + alpha + t + beta + t + gamma + '\n'
    outputFile.write(cellLine)
    # split up the file by "loop_" into different sections
    bondQ = []
    bondL = []
    atomQ = []
    atomL = []
    atoms = lines.split('loop_')
    for k in atoms:
        dashInd = k.find('_')
        # find the atoms section
        if k[dashInd:dashInd + 16] == '_atom_site_label':
            atomS = k
        # find the bonds section
        elif k[dashInd:dashInd + 28] == '_geom_bond_atom_site_label_1':
            bondS = k
    # remove spaces
    if bondS.find('\n') != -1:
        bondS = bondS.split('\n')
    else:
        bondS = bondS.split('\r')
    if atomS.find('\n') != -1:
        atomS = atomS.split('\n')
    else:
        atomS = atomS.split('\r')
    # put the labels into one list and actual atoms and bonds into another
    for atom in atomS:
        if atom.find('atom') != -1:
            atomQ.append(atom)
        else:
            atomL.append(atom)
    for bond in bondS:
        if bond.find('bond') != -1:
            bondQ.append(bond)
        else:
            bondL.append(bond)
    # get the index of infomation in the list
    labelInd = getIndex(atomQ, '_atom_site_label')
    xInd = getIndex(atomQ, '_atom_site_fract_x')
    yInd = getIndex(atomQ, '_atom_site_fract_y')
    zInd = getIndex(atomQ, '_atom_site_fract_z')
    # find the symbol
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
    # get atom information from each line of the atom list
    for atommm in atomL:
        splited = atommm.split(' ')
        while splited.count('') != 0:
            splited.remove('')
        i = i + 1
        atomNo.append(str(i))
        atomLabel = strim(splited, labelInd)
        atomId.append(atomLabel)
        atomX = strim(splited, xInd)
        atomY = strim(splited, yInd)
        atomZ = strim(splited, zInd)
        atomSym = ''
        if symInd != -1:
            atomSym = splited[symInd]
            if atomSym.find('(') != -1:
                ind = atomSym.find('(')
                atomSym = atomSym[ :ind]
        newLine = str(i) + t + atomLabel + '\t' + atomX + '\t' + atomY + '\t' + atomZ + '\t' + atomSym + '\n'
        outputFile.write(newLine)
    # write bond information with indexes and the lines with bonds
    label1 = -1
    label2 = -1
    label1 = getIndex(bondQ, '_geom_bond_atom_site_label_1')
    label2 = getIndex(bondQ, '_geom_bond_atom_site_label_2')
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
    outputFile.close()
main()
