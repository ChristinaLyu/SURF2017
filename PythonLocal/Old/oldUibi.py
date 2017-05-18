
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

atomInfoName = sys.argv[1]
bondInfoName = sys.argv[2]
outfolder = sys.argv[3]


atomInfofile = open(atomInfoName, 'r')
bondInfofile = open(bondInfoName, 'r')

#atomOut = open("atom.atm",'w')
#bondOut = open("bond.bnd", 'w')
filename = outfolder + '/testBond.xml'
Atomxml = open(filename, 'w')
#root = ET.Element("Atom+Bond")
root = Element('molecule')

#atom.atm
atomInfo = atomInfofile.read().splitlines()
startline = 0
index = 0
nrAtoms = 0
for line in atomInfo:
    index = index + 1
    #print line
    if line.find('*List') != -1:
        par = 'atomInfo	*List['
        par2 = ']'
        
        line = line.replace(par, '')
        line = line.replace(par2, '')
        atomnum = SubElement(root, "atomList")
        atomnum.set('nrAtoms', line)
        
        print "atomnum = ", atomnum
        #atomOut.write(line + '\n')
        startline = index
        nrAtoms = int(line)
atomInfo = atomInfo[startline:]

for k in range(nrAtoms):

    nom = 'atomInfo['+str(k+1)+'].atomno	'

    _z = 'atomInfo['+str(k+1)+'].z	'
    _y = 'atomInfo[' + str(k+1) + '].y	'
    _x = 'atomInfo[' + str(k+1) + '].x	'
    ID = 'atomInfo[' + str(k+1) + '].atomID	'
    atomNo = atomInfo[10]
    atom_ID = atomInfo[20]
    atom_X = atomInfo[16]
    atom_Y = atomInfo[14]
    atom_Z = atomInfo[13]
    atomID = atom_ID.replace(ID, '')
    atomno = atomNo.replace(nom, '')

    atom_x = atom_X.replace(_x, '')
    atom_y = atom_Y.replace(_y, '')
    atom_z = atom_Z.replace(_z, '')
    atomBigIn = SubElement( atomnum, 'atom')
    atomIn = SubElement(atomBigIn, 'atom')
    atomIn.set('atomId', atomID)
    atomIn.set('atomNo', atomno)
    atomIn.set('x', atom_x)
    atomIn.set('y', atom_y)
    atomIn.set('z', atom_z)
    if len(atomInfo) > 33:
        atomInfo = atomInfo[33:]

#bond.bnd
bondInfo = bondInfofile.read().splitlines()
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
bondInfo = bondInfo[startline:]

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
    atomIn.set('atom1ind', atom1ind)
    atomIn.set('atom2ind', atom2ind)
    if len(bondInfo) > 18:
        bondInfo = bondInfo[18:]



atomInfofile.close()
bondInfofile.close()



myStr=myPrettify(root)
Atomxml.write(myStr)
Atomxml.close()

