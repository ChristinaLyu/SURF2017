'''
    File:           oldUibi.py
    Author:         Christina Lyu
    Date created:   4/26/17
    Updates:
    Last modified:  5/16/17
    Python Version: 3.5.2

    Description:    output the number of atoms in a mmCIF file
    Run format:     python oldUibi.py pathToInputCifFile pathToOutputTextFile
    Run example:    python oldUibi.py /Users/xxx/abc.cif /Users/xxx/
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
    #return rough_string
##
##atomInfoName = sys.argv[1]
bondInfoName = sys.argv[1]
outFile = sys.argv[2]
##
##
##atomInfofile = open(atomInfoName, 'r')
bondInfofile = open(bondInfoName, 'r')

#atomOut = open("atom.atm",'w')
#bondOut = open("bond.bnd", 'w')

Atomxml = open(outFile, 'w')
#root = ET.Element("Atom+Bond")
root = Element('molecule')

#atom.atm
##atomInfo = atomInfofile.read().splitlines()
##startline = 0
##index = 0
##nrAtoms = 0
##for line in atomInfo:
##    index = index + 1
##    #print line
##    if line.find('*List') != -1:
##        par = 'atomInfo	*List['
##        par2 = ']'
##        
##        line = line.replace(par, '')
##        line = line.replace(par2, '')
##        atomnum = SubElement(root, "atomList")
##        atomnum.set('nrAtoms', line)
##        nrAtoms = int(line)
##
##        startline = index
##atomInfo = atomInfo[startline:]
##
##for k in range(nrAtoms):
##
##    nom = 'atomInfo['+str(k+1)+'].atomno	'
##
##    _z = 'atomInfo['+str(k+1)+'].z	'
##    _y = 'atomInfo[' + str(k+1) + '].y	'
##    _x = 'atomInfo[' + str(k+1) + '].x	'
##    ID = 'atomInfo[' + str(k+1) + '].atomID	'
##    atomNo = atomInfo[10]
##    atom_ID = atomInfo[20]
##    atom_X = atomInfo[16]
##    atom_Y = atomInfo[14]
##    atom_Z = atomInfo[13]
##    atomID = atom_ID.replace(ID, '')
##    atomno = atomNo.replace(nom, '')
##
##    atom_x = atom_X.replace(_x, '')
##    atom_y = atom_Y.replace(_y, '')
##    atom_z = atom_Z.replace(_z, '')
##    atomBigIn = SubElement( atomnum, 'atom')
##    atomIn = SubElement(atomBigIn, 'atom')
##    atomIn.set('atomId', atomID)
##    atomIn.set('atomNo', atomno)
##    atomIn.set('x', atom_x)
##    atomIn.set('y', atom_y)
##    atomIn.set('z', atom_z)
##    if len(atomInfo) > 33:
##        atomInfo = atomInfo[33:]

#bond.bnd
bondInfo = bondInfofile.read()
if bondInfo.find('*List') != -1:
    indS = 0
    indE = 0
    bondInfo = bondInfo.splitlines()
    startlineb = 0
    indexb = 0
    nrBonds = 0
    for line in bondInfo:
        indexb = indexb + 1
        if line.find('*List') != -1:
            bondnum = SubElement(root, "BondList")
            string = 'bondInfo	*List['
            string2 = ']'
            line = line.replace(string, '')
            line = line.replace(string2, '')
            bondnum.set('nrBonds', line)
            nrBonds = int(line)
            startlineb = indexb
        if line.find('bondInfo[1].colix') != -1:
            indS = indexb-1
        if line.find('bondInfo[2].colix') != -1:
            indE = indexb -1
    bondInfo = bondInfo[startlineb:]
    nrItems = indE - indS
    for k in range(nrBonds):
        atom2n = 'bondInfo[' + str(k + 1) + '].atom2.atomno	'
        atom1n = 'bondInfo[' + str(k + 1) + '].atom1.atomno	'
        atom2in = 'bondInfo[' + str(k + 1) + '].atom2.atomIndex	'
        atom1in = 'bondInfo[' + str(k + 1) + '].atom1.atomIndex	'
        atom2no = bondInfo[5].replace(atom2n, '')
        atom2ind = bondInfo[6].replace(atom2in, '')
        atom1no = bondInfo[10].replace(atom1n, '')
        atom1ind = bondInfo[11].replace(atom1in, '')
        bondBIn = SubElement( bondnum, 'bond')
        bondIn = SubElement(bondBIn, 'bond')
        bondIn.set('atomNo1', atom1no)
        bondIn.set('atomNo2', atom2no)
        bondIn.set('atom1ind', atom1ind)
        bondIn.set('atom2ind', atom2ind)
        if len(bondInfo) > nrItems - 1:
            bondInfo = bondInfo[nrItems:]
else:
    sys.exit(1)
##atomInfofile.close()
bondInfofile.close()



myStr=myPrettify(root)
Atomxml.write(myStr)
Atomxml.close()


