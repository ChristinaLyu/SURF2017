'''
    File:           xk2_cif_bnd.py
    Author:         Christina Lyu
    Date created:   8/01/17
    Updates: 	    8/01/17
    Last modified:  8/01/17
    Python Version: 2.7

    Description:    extracts the atoms from xk2.cif
    Run format:     python xk2_cif_bnd.py pathToInputXk2CifFile pathToOutputBndFile
    Run example:    python xk2_cif_bnd.py /Users/xxx/xk2.cif /Users/xxx/abc.bnd
'''

import os
import sys
from xml.etree.ElementTree import Element, SubElement, Comment
from xml.etree import ElementTree
from xml.dom import minidom
#from pathDependencies import JMOLDATA_JAR

JMOLDATA_JAR = '/Users/ChristinaLyu/Git/christina_summer_2017/External/Jmol.jar'
#-----------------------------------------------------------------      getAtoms   ------
def getAtoms(atomInfoLines):
    i=0
    atomNos=[]
    atomIds=[]
    atomSyms=[]
    atomXs = []
    atomYs = []
    atomZs = []
    for line in atomInfoLines:
        i=i+1
        splited = line.split(' ')
        while splited.count('') != 0:
            splited.remove('')
        atomNo = splited[-1]
        atomNos.append(atomNo)
        atomId = splited[1]
        atomIds.append(atomId)
        atomSym = splited[3]
        atomSyms.append(atomSym)
        atomX = splited[9]
        atomXs.append(atomX)
        atomY = splited[10]
        atomYs.append(atomY)
        atomZ = splited[11]
        atomZs.append(atomZ)
    
    return atomNos,atomIds, atomSyms,atomXs,atomYs,atomZs
#-----------------------------------------------------------------      getBonds   ------
def getBonds(bondInfoLines, atomNos, atomIds):
    i=0
    bondNo1s=[]
    bondNo2s=[]
    bondSyms=[]

    for line in bondInfoLines:
        i=i+1
        splited = line.split(' ')
        while splited.count('') != 0:
            splited.remove('')
        No1 = splited[1]
        ind1 = atomIds.index(No1)
        bondNo1 = atomNos[ind1]
        bondNo1s.append(bondNo1)
        No2 = splited[2]
        ind2 = atomIds.index(No2)
        bondNo2 = atomNos[ind2]
        bondNo2s.append(bondNo2)
        bondSym = splited[3]
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

#-----------------------------------------------------------------      myPrettify   ------
def myPrettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    string = reparsed.toprettyxml(indent="\t")
    return string

#-----------------------------------------------------------------      main   ------

def main():
    inputFileName = sys.argv[1]
    outputFilePath = sys.argv[2]

    atomFile = open(inputFileName, 'r')
    infoLines = atomFile.read().splitlines()
    atomFile.close()
    
    index = 0
    startLineId = 0
    nr = 0
    for line in infoLines:
        index = index + 1
        if line.find('_chem_comp_atom.pdbx_ordinal') != -1:
            startLineId = index
    atomInfoLines = infoLines[startLineId: ]
    index = -1
    endLineId = 0
    for line in atomInfoLines:
        index = index + 1
        if line.find('#') != -1:
            endLineId = index
            break
    atomInfoLines = atomInfoLines[ :endLineId]

    index2 = 0
    startLineId2 = 0
    for line in infoLines:
        index2 = index2 + 1
        if line.find('_chem_comp_bond.pdbx_ordinal ') != -1:
            startLineId2 = index2
            break
    bondInfoLines = infoLines[startLineId2: ]
    index = -1
    endLineId2 = 0
    for line in bondInfoLines:
        index = index + 1
        if line.find('#') != -1:
            endLineId2 = index
            break
    bondInfoLines = bondInfoLines[ :endLineId2]
    
    
    atomNos,atomIds, atomSyms,atomXs,atomYs,atomZs = getAtoms(atomInfoLines)

    bondNo1s,bondNo2s,bondSyms = getBonds(bondInfoLines, atomNos, atomIds)
        
    root = Element('bnd')
    root = makeAtomXml(root,atomNos,atomSyms,atomXs,atomYs,atomZs)
    root = makeBondXml(root,bondNo1s,bondNo2s,bondSyms)
    

    myStr=myPrettify(root)
    bndXmlFile = open(outputFilePath, 'w')
    bndXmlFile.write(myStr)
    bndXmlFile.close()

main()

    
    

    
    
