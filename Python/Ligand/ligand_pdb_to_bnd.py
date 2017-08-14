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
def getAtoms(atomInfoLines,conect, infoLines):
    bondList = []
    for line in conect:
        splited = line.split(' ')
        while splited.count('') != 0:
            splited.remove('')
        atoms = splited[1: ]
        for atom in atoms:
            if bondList.count(atom) == 0:
                bondList.append(atom)

    atomNos=[]
    atomIds=[]
    atomSyms = []
    atomXs = []
    atomYs = []
    atomZs = []
    ligands = []

    for line in atomInfoLines:
        splited = line.split(' ')
        while splited.count('') != 0:
            splited.remove('')
        atomId = splited[1]
        atomIds.append(atomId)
        atomSym = splited[-1]
        atomSyms.append(atomSym)
        atomX = splited[6]
        atomXs.append(atomX)
        atomY = splited[7]
        atomYs.append(atomY)
        atomZ = splited[8]
        atomZs.append(atomZ)
        ligand = splited[3]
        if splited[0] == 'HETATM':
            ligands.append(ligand)
    i = 0
    newAtomSyms = []
    newAtomXs = []
    newAtomYs = []
    newAtomZs = []
    newLigands = []
    for atId in bondList:
        i = i + 1
        atomNo = str(i)
        atomNos.append(atomNo)
        if atomIds.count(atId) != 0:
            ind = atomIds.index(atId)
            newAtomSyms.append(atomSyms[ind])
            newAtomXs.append(atomXs[ind])
            newAtomYs.append(atomYs[ind])
            newAtomZs.append(atomZs[ind])
            ligand = ligands[ind]
            if newLigands.count(ligand) == 0:
                newLigands.append(ligand)
            
        else:
            atomLine = 'ATOM' + (7-len(atId)) * ' ' + atId
            for line in infoLines:
                if line[ :11] == atomLine:
                    newS = line.split(' ')
                    while newS.count('') != 0:
                        newS.remove('')
                    newAtomSym = newS[-1]
                    newAtomSyms.append(newAtomSym)
                    newAtomX = newS[6]
                    newAtomXs.append(newAtomX)
                    newAtomY = newS[7]
                    newAtomYs.append(newAtomY)
                    newAtomZ = newS[8]
                    newAtomZs.append(newAtomZ)

    return atomNos, bondList, newAtomSyms, newAtomXs, newAtomYs, newAtomZs, newLigands
#-----------------------------------------------------------------     makeAtomXml   ------
def makeAtomXml(root,atomNos,atomIds,atomSyms,atomXs,atomYs,atomZs):
    nrAtoms=len(atomNos)

    atomList = SubElement(root, "atoms")
    atomList.set('nrAtoms',str(nrAtoms))
    
    for i in range(nrAtoms):
        atom = SubElement(atomList, 'atom')
        atom.set('atomNo', str(atomNos[i]))
        atom.set('atomId', str(atomIds[i]))
        atom.set('sym', atomSyms[i])
        atom.set('x', str(atomXs[i]))
        atom.set('y', str(atomYs[i]))
        atom.set('z', str(atomZs[i]))
    
    return root

#-----------------------------------------------------------------      getBonds   ------
def getBonds(bondInfoLines, infoLines, atomNos, atomIds):
    i=0
    bondNo1s=[]
    bondNo2s=[]
    bondSyms=[]

    for line in bondInfoLines:
        i=i+1
        splited = line.split(' ')
        while splited.count('') != 0:
            splited.remove('')
        find = False
        atoms = splited[1: ]
        atom1 = atoms[0]

        ind1 = atomIds.index(atom1)
        bondNo1 = atomNos[ind1]
        
        for atom2 in atoms[1: ]:
            ind2 = atomIds.index(atom2)
            bondNo2 = atomNos[ind2]
            for i in range(len(bondNo1s)):
                bond1 = bondNo1s[i]
                bond2 = bondNo2s[i]
                if (bond1 == bondNo1 and bond2 == bondNo2) or (bond1 == bondNo2 and bond2 == bondNo1):
                    find = True
                    break
                else:
                    find = False
            if find == False:
                bondNo1s.append(bondNo1)
                bondNo2s.append(bondNo2)


    return bondNo1s,bondNo2s

#-----------------------------------------------------------------     makeBondXml   ------
def makeBondXml(root,bondNo1s,bondNo2s):
    nrBonds=len(bondNo1s)

    bondList = SubElement(root, "bonds")
    bondList.set('nrBonds',str(nrBonds))
    
    for i in range(nrBonds):
        bond = SubElement(bondList, 'bond')
        bond.set('id', str(i+1))
        bond.set('atomNo1', str(bondNo1s[i]))
        bond.set('atomNo2', str(bondNo2s[i]))
        #bond.set('type', bondSyms[i])
    
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
    inputFilePath = sys.argv[1]
    outputFolderPath = sys.argv[2]

    index1 = inputFilePath.rfind('/')
    inputFileName = inputFilePath[index1 + 1: ]
    print inputFileName
    index2 = inputFileName.split('.')
    inputLigandId = index2[0]
    outputFilePath = outputFolderPath + inputLigandId + '.bnd'

    atomFile = open(inputFilePath, 'r')
    infoLines = atomFile.read().splitlines()
    atomFile.close()
    
    index = 0
    startLineId = 0
    nr = 0
    for line in infoLines:
        index = index + 1
        if line[ :4] == 'ATOM':
            startLineId = index
            break
    atomInfoLines = infoLines[startLineId: ]

    HET = []
    CON = []
    for k in range(len(infoLines)):
        line = infoLines[k]
        if line[ :6] == 'HETATM':
            HET.append(line)
        if line[ :6] == 'CONECT':
            CON.append(line)
   
    atomNos,atomIds,atomSyms, atomXs,atomYs,atomZs, ligands = getAtoms(HET,CON, infoLines)

    bondNo1s,bondNo2s = getBonds(CON, infoLines, atomNos, atomIds)
        
    root = Element('bnd')
    newLigand = ''
    for ligand in ligands:
        newLigand = newLigand + ligand
    root.set('id', newLigand)
    root.set('file', inputLigandId)
    root = makeAtomXml(root,atomNos,atomIds,atomSyms,atomXs,atomYs,atomZs)
    root = makeBondXml(root,bondNo1s,bondNo2s)
    

    myStr=myPrettify(root)
    bndXmlFile = open(outputFilePath, 'w')
    bndXmlFile.write(myStr)
    bndXmlFile.close()

main()

    
    

    
    
