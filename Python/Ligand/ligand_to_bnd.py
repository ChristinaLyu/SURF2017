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
def getAtoms(hetatm,conect, infoLines):
    atomNos = []
    ligands = []
    atomIds = []
    atomSyms = []
    atomXs = []
    atomYs = []
    atomZs = []
    for atom in hetatm:
        splited = atom.split(' ')
        while splited.count('') != 0:
            splited.remove('')
        atomId = splited[1]
        atomSym = splited[-1]
        ligand = splited[3]
        atomX = splited[6]
        atomY = splited[7]
        atomZ = splited[8]
        if ligands.count(ligand) != 0:
            ind = ligands.index(ligand)
            atomNo = atomNos[ind]
            lastNo = atomNo[-1]
            newNo = lastNo + 1
            atomNo.append(newNo)
            Ids = atomIds[ind]
            Syms = atomSyms[ind]
            Xs = atomXs[ind]
            Ys = atomYs[ind]
            Zs = atomZs[ind]
            Ids.append(atomId)
            Syms.append(atomSym)
            Xs.append(atomX)
            Ys.append(atomY)
            Zs.append(atomZ)
        else:
            ligands.append(ligand)
            newId = []
            newSym = []
            newX = []
            newY = []
            newZ = []
            newNo = []
            newNo.append(1)
            atomNos.append(newNo)
            newId.append(atomId)
            newSym.append(atomSym)
            newX.append(atomX)
            newY.append(atomY)
            newZ.append(atomZ)
            atomIds.append(newId)
            atomSyms.append(newSym)
            atomXs.append(newX)
            atomYs.append(newY)
            atomZs.append(newZ)

    return atomNos, atomIds, atomSyms, atomXs, atomYs, atomZs, ligands
#-----------------------------------------------------------------     makeAtomXml   ------
def makeAtomXml(root, atomNos, atomIds,atomSyms,atomXs,atomYs,atomZs):
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
def getBonds(conect, atomNos, atomIds):
    
    i=0
    bondNo1s=[]
    bondNo2s=[]
    bondSyms=[]


    for line in conect:
        i=i+1
        splited = line.split(' ')
        while splited.count('') != 0:
            splited.remove('')
        find = False
        atoms = splited[1: ]
        atom1 = atoms[0]

        for atom2 in atoms[1: ]:

            for i in range(len(bondNo1s)):
                bond1 = bondNo1s[i]
                bond2 = bondNo2s[i]
                if (bond1 == atom1 and bond2 == atom2) or (bond1 == atom2 and bond2 == atom1):
                    find = True
                    break
                else:
                    find = False
            if find == False:
                bondNo1s.append(atom1)
                bondNo2s.append(atom2)

    newBondNo1s = []
    newBondNo2s = []
    for atom in atomIds:
        bondList1 = []
        bondList2 = []
        newBondNo1s.append(bondList1)
        newBondNo2s.append(bondList2)

    
    for i in range(len(bondNo1s)):
        bnd1 = bondNo1s[i]
        bnd2 = bondNo2s[i]

        for k in range(len(atomIds)):
            atomId = atomIds[k]
            atomNo = atomNos[k]
            newBondNo1 = newBondNo1s[k]
            newBondNo2 = newBondNo2s[k]

            if atomId.count(bnd1) != 0 and atomId.count(bnd2) != 0:

                ind1 = atomId.index(bnd1)
                ind2 = atomId.index(bnd2)
                bndNo1 = atomNo[ind1]
                bndNo2 = atomNo[ind2]

                newBondNo1.append(bndNo1)

                newBondNo2.append(bndNo2)
                
                break

    return newBondNo1s,newBondNo2s

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

    HET = []
    CON = []
    for k in range(len(infoLines)):
        line = infoLines[k]
        if line[ :6] == 'HETATM':
            HET.append(line)
        if line[ :6] == 'CONECT':
            CON.append(line)
   
    atomNos, atomIds, atomSyms, atomXs,atomYs,atomZs, ligands = getAtoms(HET,CON, infoLines)
    
    bondNo1s,bondNo2s = getBonds(CON, atomNos, atomIds)
    root = Element('bnd')

    for i in range(len(ligands)):
        atomNo = atomNos[i]
        atomId = atomIds[i]
        ligand = ligands[i]
        atomSym = atomSyms[i]
        atomX = atomXs[i]
        atomY = atomYs[i]
        atomZ = atomZs[i]
        bondNo1 = bondNo1s[i]
        bondNo2 = bondNo2s[i]
        rootI = SubElement(root, 'bnd')
        rootI.set('id', ligand)
        rootI.set('file', inputLigandId)
        rootI = makeAtomXml(rootI,atomNo, atomId,atomSym,atomX,atomY,atomZ)
        rootI = makeBondXml(rootI,bondNo1,bondNo2)
    

    myStr=myPrettify(root)
    bndXmlFile = open(outputFilePath, 'w')
    bndXmlFile.write(myStr)
    bndXmlFile.close()

main()

    
    

    
    
