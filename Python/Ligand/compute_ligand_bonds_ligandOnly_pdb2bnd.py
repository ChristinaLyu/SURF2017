'''
    File:           xk2_cif_bnd.py
    Author:         Christina Lyu
    Date created:   8/9/17
    Updates: 	    8/18/17
    Last modified:  8/18/17
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

#JMOLDATA_JAR = '/Users/ChristinaLyu/Git/christina_summer_2017/External/Jmol.jar'
#-----------------------------------------------------------------      getAtoms   ------
def getAtoms(hetatm,conect, infoLines):
    atomNos = []
    ligands = []
    atomIds = []
    chains = []
    atomSyms = []
    atomNames = []
    atomXs = []
    atomYs = []
    atomZs = []
    ligandChains = []
    for atom in hetatm:
        splited = atom.split(' ')
        while splited.count('') != 0:
            splited.remove('')
        atomId = splited[1]
        atomSym = splited[-1]
        atomName = splited[2]
        atomChain = splited[4]
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
            chain = chains[ind]
            Xs = atomXs[ind]
            Ys = atomYs[ind]
            Zs = atomZs[ind]
            names = atomNames[ind]
            names.append(atomName)
            Ids.append(atomId)
            chain.append(atomChain)
            Syms.append(atomSym)
            Xs.append(atomX)
            Ys.append(atomY)
            Zs.append(atomZ)
        else:
            ligands.append(ligand)
            ligandChains.append(atomChain)
            newName = []
            newChain = []
            newId = []
            newSym = []
            newX = []
            newY = []
            newZ = []
            newNo = []
            if len(atomNos) >= 1:
                lastNo = atomNos[-1]
                no = lastNo[-1] + 1
                newNo.append(no)
            else:
                newNo.append(1)
            newName.append(atomName)
            newChain.append(atomChain)
            atomNos.append(newNo)
            newId.append(atomId)
            newSym.append(atomSym)
            newX.append(atomX)
            newY.append(atomY)
            newZ.append(atomZ)
            atomIds.append(newId)
            atomSyms.append(newSym)
            atomNames.append(newName)
            atomXs.append(newX)
            atomYs.append(newY)
            chains.append(newChain)
            atomZs.append(newZ)

    return atomNos, atomIds, atomSyms, atomXs, atomYs, atomZs, atomNames, chains, ligands, ligandChains
#-----------------------------------------------------------------     makeAtomXml   ------
def makeAtomXml(root, atomNos, atomIds,atomSyms,atomXs,atomYs,atomZs, atomNames, chains, atomList, conectBonds, ligands):
    nrAtoms = 0
    for m in range(len(atomNos)):
        nrAtoms=len(atomNos[m]) + nrAtoms

    atomL = SubElement(root, "atoms")
    atomL.set('nrAtoms',str(nrAtoms))
    atomL.set('nrProperAtoms', str(nrAtoms))
    atomL.set('nrVirtualAtoms', str(0))
    for k in range(len(atomNos)):
        n = k + 1
        atomId = atomIds[k]
        atomNo = atomNos[k]
        atomName = atomNames[k]
        chain = chains[k]
        atomSym = atomSyms[k]
        ligand = ligands[k]
        atomX = atomXs[k]
        atomY = atomYs[k]
        atomZ = atomZs[k]
        for i in range(len(atomNo)):
            atomI = atomId[i]

            ind = atomList.index(atomI)
            bondCount = conectBonds[ind]
            atom = SubElement(atomL, 'atom')
            atom.set('id', str(atomNo[i]))
            atom.set('pdbAtomId', str(atomId[i]))
            atom.set('pdbAtomName', atomName[i])
            atom.set('pdbBondCount', str(bondCount))
            atom.set('pdbChainId', chain[i])
            atom.set('pdbChainId2', str(n))
            atom.set('pdbElement', atomSym[i])
            atom.set('pdbResidueId', str(1))
            atom.set('pdbResidueName', ligand)
            atom.set('seqValency', str(bondCount))
            atom.set('virtual', 'False')
            atom.set('x', str(atomX[i]))
            atom.set('y', str(atomY[i]))
            atom.set('z', str(atomZ[i]))
    
    return root

#-----------------------------------------------------------------      getBondCount   ------

#-----------------------------------------------------------------      getBonds   ------
def getBonds(conect, atomNos, atomIds):
    
    i=0
    bondNo1s=[]
    bondNo2s=[]
    bondSyms=[]
    atomList = []
    conectBonds = []

    for line in conect:
        i=i+1
        atoms = []
        atomsList = line[6: ]
        length = len(atomsList)
        number = length/5
        for j in range(number):
            withSpace = atomsList[j * 5:(j + 1) * 5]
            withSpace = withSpace.replace(' ', '')
            if len(withSpace) != withSpace.count(' '):
                atoms.append(withSpace)

        find = False

        atom1 = atoms[0]
        atomList.append(atom1)
        conectBonds.append(len(atoms[1: ]))
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

    return newBondNo1s,newBondNo2s, atomList, conectBonds

#-----------------------------------------------------------------     makeChainXml   ------
def makeChainXml(root,ligands,ligandChains):
    nrChains = len(ligands)
    chainList = SubElement(root, "chains")
    chainList.set('nrChains',str(nrChains))
    
    for i in range(nrChains):
        chain = SubElement(chainList, 'chain')
        chain.set('id', str(i+1))
        chain.set('name', ligandChains[i])
        residue = SubElement(chain, 'residue')
        residue.set('id', '1')
        residue.set('name', ligands[i])

        #bond.set('type', bondSyms[i])
    
    return root
#-----------------------------------------------------------------     makeBondXml   ------
def makeBondXml(root,bondNo1s,bondNo2s):
    nrBonds = 0
    for k in range(len(bondNo1s)):
        
        nrBonds=len(bondNo1s[k]) + nrBonds

    bondList = SubElement(root, "bonds")
    bondList.set('nrBonds',str(nrBonds))
    bondList.set('nrProperBonds', str(nrBonds))
    bondList.set('nrVirtualBonds', str(0))
    for k in range(len(bondNo1s)):
        bondNo1 = bondNo1s[k]
        bondNo2 = bondNo2s[k]
        chainId = k + 1
        for i in range(len(bondNo1)):
            bond = SubElement(bondList, 'bond')
            bond.set('id', str(i+1))
            bond.set('atomNo1', str(bondNo1[i]))
            bond.set('atomNo2', str(bondNo2[i]))
            bond.set('chainId', str(chainId))
            bond.set('virtual', "False")
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
   
    atomNos, atomIds, atomSyms, atomXs,atomYs,atomZs, atomNames, chains, ligands, ligandChains = getAtoms(HET,CON, infoLines)
    
    bondNo1s,bondNo2s, atomList, conectBonds = getBonds(CON, atomNos, atomIds)
    root = Element('bnd')
    root.set('type', 'finite')
    root.set('file', inputFileName)

    rootC = makeChainXml(root, ligands, ligandChains)
##    for i in range(len(ligands)):
##        atomNo = atomNos[i]
##        atomId = atomIds[i]
##        ligand = ligands[i]
##        atomSym = atomSyms[i]
##        atomName = atomNames[i]
##        atomX = atomXs[i]
##        atomY = atomYs[i]
##        atomZ = atomZs[i]
##        bondNo1 = bondNo1s[i]
##        bondNo2 = bondNo2s[i]
##        ligandChain = ligandChains[i]
##        chain = chains[i]

    rootA = makeAtomXml(root,atomNos, atomIds,atomSyms,atomXs,atomYs,atomZs, atomNames, chains,atomList, conectBonds, ligands)
    rootB = makeBondXml(root,bondNo1s,bondNo2s)
    

    myStr=myPrettify(root)
    bndXmlFile = open(outputFilePath, 'w')
    bndXmlFile.write(myStr)
    bndXmlFile.close()

main()

    
    

    
    
