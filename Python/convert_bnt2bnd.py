'''
    File:           convert_bnt2bnd.py
    Author:         Christina Lyu
    Date created:   6/1/17
    Updates:
    Last modified:  
    Python Version: 3.5.2

    Description:    convert a bnt file to an xml format as bnd
    Run format:     python convert_bnt2bnd.py pathToInputCifFile pathToOutputTextFile
    Run example:    python convert_bnt2bnd.py ers/xxx/abc.cif /Users/xxx/
'''

import os
import sys
#import xml.etree.cElementTree as ET
from xml.etree.ElementTree import Element, SubElement, Comment
#from ElementTree_pretty import prettify
from xml.etree import ElementTree
from xml.dom import minidom

def myPrettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ElementTree.tostring(elem, 'utf-8')
    #print rough_string
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="\t")


inputBnt = sys.argv[1]
outputFolder = sys.argv[2]

bntFile = open(inputBnt, 'r')
bntFile = bntFile.read()

bntFileName = inputBnt.split('/')[-1]
bntName = bntFileName.split('.')[0]
bndName = bntName + '.bnd'
bndFilePath = outputFolder + '/' + bndName

bndFile = open(bndFilePath, 'w')
root = Element('bnd')
root.set('name', bntName)

ind1 = bntFile.find('BONDS')
atoms = bntFile[ :ind1]
bonds = bntFile[ind1: ]

atoms = atoms.splitlines()
atoms = atoms[1: ]
nrAtoms = len(atoms)
bonds = bonds.splitlines()
bonds = bonds[1: ]
nrBonds = len(bonds)

rootAtm = SubElement(root, 'atoms')
rootAtm.set('nrAtoms', str(nrAtoms))

for atom in atoms:
    atom = atom.split(' ')
    while atom.count('') != 0:
        atom.remove('')

    atmId = atom[0]
    misc = atom[1]
    pdbLabel = atom[2]
    element = atom[3]
    valence = atom[4]
    
    atm = SubElement(rootAtm, 'atom')
    atm.set('id', atmId)
    atm.set('misc', misc)
    atm.set('pdbLabel', pdbLabel)
    atm.set('element', element)
    atm.set('valence', valence)


rootBnd = SubElement(root, 'bonds')
rootBnd.set('nrBonds', str(nrBonds))

for bond in bonds:
    bond = bond.split(' ')
    while bond.count('') != 0:
        bond.remove('')

    bndId = bond[0]
    atom1 = bond[1]
    atom2 = bond[2]
    bType = bond[3]
    
    bnd = SubElement(rootBnd, 'bond')
    bnd.set('id', bndId)
    bnd.set('atom1', atom1)
    bnd.set('atom2', atom2)
    bnd.set('type', bType)

Name = myPrettify(root)
bndFile.write(Name)
bndFile.close()
