'''
    File:           ligand_to_bnd.py
    Author:         Christina Lyu
    Date created:   8/18/17
    Updates: 	    8/18/17
    Last modified:  8/18/17
    Python Version: 2.7

    Description:    extracts the atoms and bonds from pdb file
    Run format:     python xk2_cif_bnd.py pathToInputPDBFile pathToOutputBndFile
    Run example:    python xk2_cif_bnd.py /Users/xxx/ligand.pdb /Users/xxx/abc.bnd
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
    outputFilePath = outputFolderPath + inputLigandId + '.txt'

    atomFile = open(inputFilePath, 'r')
    infoLines = atomFile.read()
    infoList = infoLines.split(';')

    outputFile = open(outputFilePath, 'w')
    containAtoms = ''
    for k in range(len(infoList)):
        lines = infoList[k]
        if lines.find('_cell_angle_alpha') != -1:
            lineL = lines.splitlines()
            for line in lineL:
                if line.find('_cell_angle_alpha') != -1:
                    outputFile.write(line + '\n')
                elif line.find('_cell_angle_beta') != -1:
                    outputFile.write(line + '\n')
                elif line.find('_cell_angle_gamma') != -1:
                    outputFile.write(line + '\n')
                elif line.find('_cell_length_a') != -1:
                    outputFile.write(line + '\n')
                elif line.find('_cell_length_b') != -1:
                    outputFile.write(line + '\n')
                elif line.find('_cell_length_c') != -1:
                    outputFile.write(line + '\n')
        if lines.find('_atom_site') != -1:
            containAtoms = lines
         
    atomQ = []
    atomL = []
    if containAtoms != '':
        atomS = ''
        atoms = containAtoms.split('loop_')
        for k in atoms:

            if k[2:18] == '_atom_site_label':
                atomS = k

        atomS = atomS.split('\n')

        for atom in atomS:
            if atom.find('atom') != -1:
                atomQ.append(atom)
            else:
                atomL.append(atom)

    labelInd = atomQ.index('_atom_site_label\r')
    xInd = atomQ.index('_atom_site_fract_x\r')
    yInd = atomQ.index('_atom_site_fract_y\r')
    zInd = atomQ.index('_atom_site_fract_z\r')
    symInd = -1
    if atomQ.count('_atom_site_type_symbol\r') != 0:
        symInd = atomQ.index('_atom_site_type_symbol\r')
    elif atomQ.count('_atom_site_type\r') != 0:
        symInd = atomQ.index('_atom_site_type\r')
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

        atomLabel = splited[labelInd]
        atomX = splited[xInd]
        atomY = splited[yInd]
        atomZ = splited[zInd]
        atomSym = ''
        if symInd != -1:
            atomSym = splited[symInd]
        newLine = atomLabel + '\t' + atomX + '\t' + atomY + '\t' + atomZ + '\t' + atomSym + '\n'
        outputFile.write(newLine)
    atomFile.close()


main()
