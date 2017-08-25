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

# --------------------------------------------------------------------
PYFILE_NAME = 'cif2out.py'
# --------------------------------------------------------------------
ERROR_PREFIX = 'ERROR:' + PYFILE_NAME + ': '
ERROR_1 = ERROR_PREFIX + 'Usage: python ' + PYFILE_NAME + ' inputCifFile outputFolderPath'

#-----------------------------------------------------------------      strim   ------
def strim(item):
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



#------------------------------------- parse atom headers and lines --------
def parseAtomHeadersAndLinesWriteToOutput(atomHeaderLines,atomLines,openOutputOutFile):
    # input lines are already stripped of \n and \r
    
    # get the positions (indices) of information in the header list
    labelInd = getIndex(atomHeaderLines, '_atom_site_label')
    xInd = getIndex(atomHeaderLines, '_atom_site_fract_x')
    yInd = getIndex(atomHeaderLines, '_atom_site_fract_y')
    zInd = getIndex(atomHeaderLines, '_atom_site_fract_z')
    # the atom symbol may be named differently, so try several possibilities
    symInd = -1   
    if atomHeaderLines.count('_atom_site_type_symbol') != 0:
        symInd = atomHeaderLines.index('_atom_site_type_symbol')
    elif atomHeaderLines.count('_atom_site_type') != 0:
        symInd = atomHeaderLines.index('_atom_site_type')
    elif atomHeaderLines.count('_atom_site_symbol') != 0:
        symInd = atomHeaderLines.index('_atom_site_symbol')
        
    # each line corresponds to an atom; give it a new atom id
    id = 0
    # create lists of atomIds and labels for future use
    atomIdList = []
    cifAtomLabelList = []
    
    # get atom information from each line of the atom list
    for line in atomLines:
        splitedLine = line.split(' ')
        while splitedLine.count('') != 0:
            splitedLine.remove('')
        id = id + 1
        atomIdList.append(str(id))
        
        # remove the () in numbers
        atomLabel = strim(splitedLine[labelInd])
        cifAtomLabelList.append(atomLabel)
        
        # remove the () in numbers
        atomX = strim(splitedLine[xInd])
        atomY = strim(splitedLine[yInd])
        atomZ = strim(splitedLine[zInd])
        
        atomSym = ''
        if symInd != -1:
            atomSym = strim(splitedLine[symInd])
        
        t = '\t'
        newLine = str(id) + t + atomLabel + t + atomX + t + atomY + t + atomZ + t + atomSym + '\n'
        openOutputOutFile.write(newLine)
        
    return atomIdList,cifAtomLabelList

#------------------------------------- parse bond headers and lines --------
def parseBondHeadersAndLinesWriteToOutput(bondHeaderLines,bondLines,atomIdList,cifAtomLabelList,openOutputOutFile):

    # write bond information with indexes and the lines with bonds
    label1 = -1
    label2 = -1
    label1 = getIndex(bondHeaderLines, '_geom_bond_atom_site_label_1')
    label2 = getIndex(bondHeaderLines, '_geom_bond_atom_site_label_2')
    t='\t'
    
    for line in bondLines:
        splitedLine = line.split(' ')
        while splitedLine.count('') != 0:
            splitedLine.remove('')
        bondId1 = splitedLine[label1]
        bondId2 = splitedLine[label2]
        ind1 = cifAtomLabelList.index(bondId1)
        ind2 = cifAtomLabelList.index(bondId2)
        bondNo1 = atomIdList[ind1]
        bondNo2 = atomIdList[ind2]
        bondLine = bondNo1 + t + bondNo2 + t + bondId1 + t + bondId2 + '\n'
        openOutputOutFile.write(bondLine)
        

#------------------------------------- extract atom headers and lines --------
def extractAtomHeadersAndLines(atomSectionString):
    
    atomLineList = atomSectionString.splitlines()
    
    atomHeaders=[]
    atomLines=[]
    # put the headers into one list and actual atoms into another
    for atomLine in atomLineList:
        stripped_atom_line=atomLine.strip('\n\r')
        if stripped_atom_line.find('atom') != -1:
            atomHeaders.append(stripped_atom_line)
        elif stripped_atom_line!='':
            atomLines.append(stripped_atom_line)
    return atomHeaders, atomLines
    
#------------------------------------- extract bond headers and lines --------
def extractBondHeadersAndLines(bondSectionString):           
    bondLineList = bondSectionString.splitlines()
    
    bondHeaderLines=[]
    bondLines=[]
    for bondLine in bondLineList:
        stripped_bond_line=bondLine.strip('\n\r')
        if stripped_bond_line.find('bond') != -1:
            bondHeaderLines.append(stripped_bond_line)
        elif stripped_bond_line != '':
            bondLines.append(stripped_bond_line)

    return bondHeaderLines,bondLines
            
#------------------------------------- extract atom section and bond section --------
def extractAtomSectionAndBondSection(loopSeparatedSections):
    for section in loopSeparatedSections:
        dashInd = section.find('_')
        # find the loopSeparatedSections section
        if section[dashInd:dashInd + 16] == '_atom_site_label':
            atomS = section
        # find the bonds section
        elif section[dashInd:dashInd + 28] == '_geom_bond_atom_site_label_1':
            bondS = section
    return atomS,bondS
            
#------------------------------------- extract cell and data info from cif file --------
def makeCellLineFromCifLineList(lineListInCifFile):
    
    alpha = ''; beta = ''; gamma = ''; a = ''; b = ''; c = ''; data_info = '';
    
    for line in lineListInCifFile:
        stripped_line=line.strip('\n\r \t')
        if len(stripped_line)>=5 and stripped_line[0:5]=='_cell':
            split_line=stripped_line.split()
            if len(split_line)>=2:
                line_header=split_line[0]
                line_info=split_line[1]
                # eliminate approx. part of each number, enclosed in parentheses
                if line_header == '_cell_length_a':
                    a = line_info.split('(')[0]
                elif line_header == '_cell_length_b':
                    b = line_info.split('(')[0]
                elif line_header == '_cell_length_c':
                    c = line_info.split('(')[0]
                elif line_header == '_cell_angle_alpha':
                    alpha = line_info.split('(')[0]
                elif line_header == '_cell_angle_beta':
                    beta = line_info.split('(')[0]
                elif line_header == '_cell_angle_gamma':
                    gamma = line_info.split('(')[0]                
    t = '\t'
    cellLine = a + t + b + t + c + t + alpha + t + beta + t + gamma + '\n'
    
    return cellLine


#-----------------------------------------------      getOutputFilePath   ------
def getOutputFilePath(inputFilePath, outputFolder, extension):
    index1 = inputFilePath.rfind('/')
    inputFileWExtension = inputFilePath[index1 + 1: ]
    index2 = inputFileWExtension.rfind('.')
    inputFileWtExtension = inputFileWExtension[ :index2]
    inputExtension = inputFileWExtension[index2: ]
    outputFilePath = outputFolder + inputFileWtExtension + extension
    return outputFilePath, inputExtension

#-----------------------------------------------------------------      main   ------
def main(inputFilePath,outputFolderPath):
    # get output file path    
    outputFilePath, inputExtension = getOutputFilePath(inputFilePath, outputFolderPath, '.out')
    # open input and output files
    openInputCifFile = open(inputFilePath, 'r')
    openOutputOutFile = open(outputFilePath, 'w')
    
    fileContentsString = openInputCifFile.read()
    
    # parse the lines with cell info and write to output
    lineList = fileContentsString.splitlines()
    firstLine = lineList[0]
    if firstLine[ :5] == 'data_':
        data = firstLine[5: ] + inputExtension
        openOutputOutFile.write(data + '\n')

        
    cellLine=makeCellLineFromCifLineList(lineList)
    openOutputOutFile.write(cellLine)

    # split input lines into sections separated by loop_
    loopSeparatedSections = fileContentsString.split('loop_')
            
    # ASSUMPTION: there should be exactly one atom section and one bond section
    # TO CHECK
    atomSectionString, bondSectionString = extractAtomSectionAndBondSection(loopSeparatedSections)
    
    
    atomHeaderLines, atomLines = extractAtomHeadersAndLines(atomSectionString)
    bondHeaderLines, bondLines = extractBondHeadersAndLines(bondSectionString)

    atomIdList,cifAtomLabelList = parseAtomHeadersAndLinesWriteToOutput(atomHeaderLines,atomLines,openOutputOutFile)
    
    parseBondHeadersAndLinesWriteToOutput(bondHeaderLines,bondLines,atomIdList,cifAtomLabelList,openOutputOutFile)
    openInputCifFile.close()
    openOutputOutFile.close()

#----------------------------------------------- top call to MAIN ---------------


if __name__ == "__main__":

    if len(sys.argv) != 3:
        print ERROR_1
        sys.exit(-1)
        
    # get input file and output folder paths
    inputFilePath = sys.argv[1]
    outputFolderPath = sys.argv[2]

    main(inputFilePath,outputFolderPath)
