'''
    File:           apply_certain_symmetries_cif2out_folder.py
    Author:         Christina Lyu
    Date created:   8/27/17
    Updates: 	    8/27/17
    Last modified:  8/27/17
    Python Version: 2.7

    Description:    extracts atoms and write into crystal
    Run format:     python cif2crystal.py pathToInputCifFile pathToOutputFolder
    Run example:    python cif2crystal.py /Users/xxx/ABW.cif /Users/Output/
'''
import os
import sys
from xml.etree.ElementTree import Element, SubElement, Comment
from xml.etree import ElementTree
from xml.dom import minidom

# --------------------------------------------------------------------
PYFILE_NAME = 'cif2crystal.py'
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

#-----------------------------------------------------------------      strim   ------
def getLabel(cifAtomLabel):
    numberList = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    cifAtomLabelList = list(cifAtomLabel)
    labelList = []
    for char in cifAtomLabelList:
        if numberList.count(char) == 0:
            labelList.append(char)
    label = ''.join(labelList)
    return label
#-----------------------------------------------      getOutputFilePath   ------
def getOutputFilePath(inputFilePath, outputFolder, extension):
    index1 = inputFilePath.rfind('/')
    inputFileWExtension = inputFilePath[index1 + 1: ]
    index2 = inputFileWExtension.rfind('.')
    inputFileWtExtension = inputFileWExtension[ :index2]
    outputFilePath = outputFolder + inputFileWtExtension + extension
    return outputFilePath

#------------------------------------- parse atom headers and lines --------
def parseAtomHeadersAndLinesWriteToOutput(atomHeaderLines,atomLines):
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
        
    # create lists of atomIds and labels for future use
    cifAtomLabelList = []
    atomSymList = []
    atomXList = []
    atomYList = []
    atomZList = []
    # get atom information from each line of the atom list
    for line in atomLines:
        splitedLine = line.split(' ')
        while splitedLine.count('') != 0:
            splitedLine.remove('')
        
        # remove the () in numbers
        atomLabel = strim(splitedLine[labelInd])
        cifAtomLabelList.append(atomLabel)
        
        # remove the () in numbers
        atomX = strim(splitedLine[xInd])
        atomXList.append(atomX)
        atomY = strim(splitedLine[yInd])
        atomYList.append(atomY)
        atomZ = strim(splitedLine[zInd])
        atomZList.append(atomZ)

        atomSym = ''
        if symInd != -1:
            atomSym = strim(splitedLine[symInd])
            atomSymList.append(atomSym)
        
    return cifAtomLabelList, atomSymList, atomXList, atomYList, atomZList


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

#-----------------------------------------------------------------      main   ------
def main(inputFilePath,outputFolderPath, wantedSymmetries):
    # get output file path
    outputFilePath = getOutputFilePath(inputFilePath, outputFolderPath, '.out')
    # open input and output files
    openInputCifFile = open(inputFilePath, 'r')
    openOutputOutFile = open(outputFilePath, 'w')
    
    cifFile = openInputCifFile.read()
    loopSections = cifFile.split('loop_')
    symmetrySection = ''
    atomSection = ''
    for section in loopSections:
        dashInd = section.find('_')
        if section[dashInd:dashInd + 26] == '_symmetry_equiv_pos_as_xyz':
            symmetrySection = section
        elif section[dashInd:dashInd + 16] == '_atom_site_label':
            atomSection = section
    
    # parse the symmetry section
    symmetryWtSep = symmetrySection.splitlines()
    while symmetryWtSep.count('') != 0:
        symmetryWtSep.remove('')
    symmetryList = []
    for line in symmetryWtSep[1: ]:
        noSep = line.strip('\n\r')
        symmetryList.append(noSep)
    
    # parse the atom section
    atomHeaders, atomLines = extractAtomHeadersAndLines(atomSection)

    cifAtomLabelList, atomSymList, atomXList, atomYList, atomZList = parseAtomHeadersAndLinesWriteToOutput(atomHeaders,atomLines)
    
    newCifAtomLabelList = []
    newAtomLabelList = []
    newAtomSymList = []
    newAtomCoordsList = []
    newAtomLabelList = []
    for i in range(len(cifAtomLabelList)):
        newCifAtomLabelList.append(cifAtomLabelList[i])
        newAtomLabelList.append(getLabel(cifAtomLabelList[i]))
        newAtomSymList.append(atomSymList[i])
        atomCoords = [atomXList[i], atomYList[i], atomZList[i]]
        newAtomCoordsList.append(atomCoords)

    for n in range(len(cifAtomLabelList)):
        cifAtomLabel = cifAtomLabelList[n]
        atomLabel = getLabel(cifAtomLabel)
        atomSym = atomSymList[n]
        atomX = atomXList[n]
        atomY = atomYList[n]
        atomZ = atomZList[n]
        for sym in wantedSymmetries:
            if sym == '0':
                for symm in symmetryList:
                    symmetry = '[' + symm[1:-1] + ']'
                    function = lambda x, y, z: eval('[' + symm[1:-1] + ']')
                    xx=float(atomX)
                    yy=float(atomY)
                    zz=float(atomZ)
                    newCoords = function(xx, yy, zz)

                    if newAtomCoordsList.count(newCoords) == 0:
                        newAtomCoordsList.append(newCoords)
                        newAtomSymList.append(atomSym)
                        newAtomLabelList.append(atomLabel)
            else:
                symm = symmetryList[int(sym) - 1]
                symmetry = '[' + symm[1:-1] + ']'
                function = lambda x, y, z: eval('[' + symm[1:-1] + ']')
                xx=float(atomX)
                yy=float(atomY)
                zz=float(atomZ)
                newCoords = function(xx, yy, zz)

                if newAtomCoordsList.count(newCoords) == 0:
                    newAtomCoordsList.append(newCoords)
                    newAtomSymList.append(atomSym)
                    newAtomLabelList.append(atomLabel)
            

    t = '\t'

    for g in range(len(newAtomLabelList)):
        newAtomLabel = newAtomLabelList[g]
        newAtomSym = newAtomSymList[g]
        newAtomCoords = newAtomCoordsList[g]
        
        labelIndex = newAtomLabelList[ :g + 1].count(newAtomLabel)
        finalLabel = newAtomLabel + str(labelIndex)

        atomLine = finalLabel + t + newAtomSym + t + str(newAtomCoords[0]) + t + str(newAtomCoords[1]) + t + str(newAtomCoords[2]) + '\n'
        openOutputOutFile.write(atomLine)

    symmetry2 = symmetryList[-1]
    sym = '[' + symmetry2[1:-1] + ']'
    newF = lambda x, y, z: eval('[' + symmetry2[1:-1] + ']')
    fList = newF(0.5, 0.5, 0.5)
    print fList
    newG = lambda x, y, z: eval(str('[1/2+x,+y,1/2-z]'))
    gList = newG(0.5, 0.5, 0.5)
    print 'gList', gList

#----------------------------------------------- top call to MAIN ---------------
if __name__ == "__main__":

    if len(sys.argv) < 3:
        print ERROR_1
        sys.exit(-1)
        
    # get input file and output folder paths
    inputFilePath = sys.argv[1]
    outputFolderPath = sys.argv[2]
    if len(sys.argv) > 3:
        wantedSymmetries = sys.argv[3: ]
    else:
        wantedSymmetries = ['0']

    main(inputFilePath,outputFolderPath, wantedSymmetries)
