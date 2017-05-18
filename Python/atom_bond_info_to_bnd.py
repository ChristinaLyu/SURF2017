'''
    File:           atom_bond_info_to_bnd.py
    Author:         Ileana Streinu with Christina Lyu
    Date created:   4/26/17
    Updates: 	    5/11/17
    Last modified:  5/11/17
    Python Version: 2.7

    Description:    extracts the atoms and bonds from atomInfo and bondInfo files in an xml bnd format
    Run format:     python atom_bond_info_to_bnd.py pathToInputAtomInfoFile pathToInputBondInfoFile pathToOutputBndFile
    Run example:    python atom_bond_info_to_bnd.py /Users/xxx/atomInfo.txt /Users/xxx/bondInfo.txt /Users/xxx/abc.bnd
'''

import os
import sys

from xml.etree.ElementTree import Element, SubElement, Comment
from xml.etree import ElementTree
from xml.dom import minidom

DEBUG = True
#-----------------------------------------------------------------      Utilities for debugging    ------
def debugMark(message,functionName):
    if DEBUG:
        print(' ')
        print('===============' + message + '  ' + functionName + '===============')
        print(' ')

def debugFun(message,functionName):
    if DEBUG:
        print('............' + message + '  ' + functionName)
        
def debugVar(var,val):
    if DEBUG:
        print(var + " = " + val)  

#-----------------------------------------------------------------      myPrettify   ------
def myPrettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    string = reparsed.toprettyxml(indent="\t")
    return string
#-----------------------------------------------------------------      process_atom_bond_info   ------
def getNr(starLine):
    part2=starLine.split('[')[1]
    nr = int(part2.split(']')[0])
    return nr
    
def getStartLineId(infoLines):
    index = 0
    startLineId = 0
    for line in infoLines:
        index = index + 1
        if line.find('*List') != -1:
            startLineId = index
            nr = getNr(line)
    return startLineId,nr

#-----------------------------------------------------------------      getAtoms   ------
def getAtoms(atomInfoLines):
    i=0
    atomNos=[]
    # atomIds=[]
    atomSyms=[]
    atomXs = []
    atomYs = []
    atomZs = []
    for line in atomInfoLines:
        i=i+1
        if i%33 == 11:
            atomNo=int(line.split('\t')[1])
            atomNos.append(atomNo)
        
        if i%33 == 14:
            atomZ=float(line.split('\t')[1])
            atomZs.append(atomZ)
            
        if i%33 == 15:
            atomY=float(line.split('\t')[1])
            atomYs.append(atomY)
            
        if i%33 == 17:
            atomX=float(line.split('\t')[1])
            atomXs.append(atomX)
            
        if i%33 == 19:
            atomSym=line.split('"')[1].split('"')[0]
            atomSyms.append(atomSym)
            
        # if i%33 == 21:
        #     atomId=int(line.split('\t')[1])
        #     atomIds.append(atomId)

    
    return atomNos,atomSyms,atomXs,atomYs,atomZs

#-----------------------------------------------------------------      getBonds   ------
def getBonds(bondInfoLines):
    i=0
    bondNo1s=[]
    bondNo2s=[]
    bondSyms=[]

    for line in bondInfoLines:
        i=i+1
        if i%17 == 6:
            bondNo1=int(line.split('\t')[1])
            bondNo1s.append(bondNo1)
        
        if i%17 == 11:
            bondNo2=int(line.split('\t')[1])
            bondNo2s.append(bondNo2)
            
        if i%17 == 0:
            bondSym=line.split('"')[1].split('"')[0]
            bondSyms.append(bondSym)

    
    return bondNo1s,bondNo2s,bondSyms

#-----------------------------------------------------------------     makeAtomXml   ------
def makeAtomXml(root,atomNos,atomSyms,atomXs,atomYs,atomZs):
    nrAtoms=len(atomNos)

    atomList = SubElement(root, "atoms")
    atomList.set('nrAtoms',str(nrAtoms))
    
    for i in range(nrAtoms):
        atom = SubElement(atomList, 'atom')
        # atom.set('atomId', str(atomIds[i]))
        atom.set('atomNo', str(atomNos[i]))
        atom.set('sym', atomSyms[i])
        atom.set('x', str(atomXs[i]))
        atom.set('y', str(atomYs[i]))
        atom.set('z', str(atomZs[i]))
    
    return root

#-----------------------------------------------------------------     makeBondXml   ------
def makeBondXml(root,bondNo1s,bondNo2s,bondSyms):
    nrBonds=len(bondNo1s)

    bondList = SubElement(root, "bonds")
    bondList.set('nrBonds',str(nrBonds))
    
    for i in range(nrBonds):
        bond = SubElement(bondList, 'bond')
        bond.set('id', str(i+1))
        bond.set('atomNo1', str(bondNo1s[i]))
        bond.set('atomNo2', str(bondNo2s[i]))
        bond.set('type', bondSyms[i])
    
    return root
    
#-----------------------------------------------------------------      process_atom_bond_info   ------
def process_atom_bond_info(inputAtomInfoFilePath,inputBondInfoFilePath,outputBndFilePath):

    atomInfoFile = open(inputAtomInfoFilePath, 'r')    
    allAtomLines = atomInfoFile.read().splitlines()
    atomInfoFile.close()
    
    startLineId,nrAtoms = getStartLineId(allAtomLines)
    atomInfoLines = allAtomLines[startLineId:]

    atomNos,atomSyms,atomXs,atomYs,atomZs = getAtoms(atomInfoLines)
    
    bondInfoFile = open(inputBondInfoFilePath, 'r')
    allBondLines = bondInfoFile.read().splitlines()
    bondInfoFile.close()
    
    startLineId,nrBonds = getStartLineId(allBondLines)
    bondInfoLines = allBondLines[startLineId:]
    
    bondNo1s,bondNo2s,bondSyms = getBonds(bondInfoLines)
        
    root = Element('bnd')
    root = makeAtomXml(root,atomNos,atomSyms,atomXs,atomYs,atomZs)
    root = makeBondXml(root,bondNo1s,bondNo2s,bondSyms)
    

    myStr=myPrettify(root)
    bndXmlFile = open(outputBndFilePath, 'w')
    bndXmlFile.write(myStr)
    bndXmlFile.close()

#----------------------------------------------------------------------------------  MAIN  ----------
def main():

    debugMark(" START ", "atom_bond_info_to_bnd.py")
    
    inputAtomInfoFilePath = sys.argv[1]
    # debugVar("inputAtomInfoFilePath",inputAtomInfoFilePath)
    inputBondInfoFilePath = sys.argv[2]
    # debugVar("inputBondInfoFilePath",inputBondInfoFilePath)
    outputBndFilePath = sys.argv[3]
    # debugVar("outputBndFilePath",outputBndFilePath)

    process_atom_bond_info(inputAtomInfoFilePath,inputBondInfoFilePath,outputBndFilePath)

    debugMark(" END ", "atom_bond_info_to_bnd.py")
    
#-----------------------------------------------------------------------------------   TOP  ----------
    # TODO: Clean up intermediary files, if necessary
if __name__ == "__main__":
    
    if len(sys.argv) != 4:
        print ('usage: python atom_bond_info_to_bnd.py input_atomInfo_File input_bondInfo_File output_bnd_File')
        sys.exit(-1)

    main()


