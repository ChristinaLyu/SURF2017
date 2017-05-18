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
filename = sys.argv[3]

atomInfofile = open(atomInfoName, 'r')
bondInfofile = open(bondInfoName, 'r')

#atomOut = open("atom.atm",'w')
#bondOut = open("bond.bnd", 'w')
Atomxml = open(filename, 'w')
#root = ET.Element("Atom+Bond")
root = Element('molecule')

#atom.atm
atomInfo = atomInfofile.read().splitlines()
startline = 0
index = 0
for line in atomInfo:
    index = index + 1
    #print line
    if line.find('*List') != -1:
        par = 'atomInfo	*List['
        par2 = ']'
        print "List line = ", line
        line = line.replace(par, '')
        line = line.replace(par2, '')
        atomnum = SubElement(root, "atomList")
        atomnum.set('nrAtoms', line)
        print "atomnum = ", atomnum
        #atomOut.write(line + '\n')
        startline = index
atomInfo = atomInfo[startline:]
#print "length", len(atomInfo)
filelen = (len(atomInfo)) / 33
#print "filelen = ", filelen

#atomOut.write('atomno    atomID      atom.x    atom.y    atom.z' + '\n')

for k in range(filelen):
#    atomels = atomInfo[1 + 33 * k + 4]
#    atomel = atomels[-1]
    nom = 'atomInfo['+str(k+1)+'].atomno	'
    _z = 'atomInfo['+str(k+1)+'].z	'
    _y = 'atomInfo[' + str(k+1) + '].y	'
    _x = 'atomInfo[' + str(k+1) + '].x	'
    ID = 'atomInfo[' + str(k+1) + '].atomID	'
    
    for j in range(33):
        
        each = atomInfo[k * 33 + j]
        if each.find('atomno') != -1:           
            atomno = each.replace(nom,'')
        if each.find('.z') != -1:
            atom_z = each.replace(_z,'')
        if each.find('.y') != -1:
            atom_y = each.replace(_y,'')
        if each.find('.x') != -1:
            
            atom_x = each.replace(_x,'')
        if each.find('atomID') != -1:
            
            atomID = each.replace(ID,'')
    atomBigIn = SubElement( atomnum, 'atom')
    atomIn = SubElement(atomBigIn, 'atom')
    atomIn.set('atomId', atomID)
    atomIn.set('atomNo', atomno)
    atomIn.set('x', atom_x)
    atomIn.set('y', atom_y)
    atomIn.set('z', atom_z)
    #atomOut.write(atomno + '      ' + atomID + '     ' + atom_x + '    ' + atom_y + '    ' + atom_z + '     ' + '\n')


#bond.bnd
bondInfo = bondInfofile.read().splitlines()
startlineb = 0
indexb = 0
for line in bondInfo:
    indexb = indexb + 1
    if line.find('*List') != -1:
        bondnum = SubElement(root, "bondList")
        string = 'bondInfo	*List['
        string2 = ']'
        line = line.replace(string, '')
        line = line.replace(string2, '')
        bondnum.set('nrBonds', line)
        #bondOut.write(line + '\n')
        startlineb = indexb
bondInfo = bondInfo[startline:]

filelen = (len(bondInfo)) / 18
#bondOut.write('bondno    atom1no   atom1ind    atom2no   atom2ind' + '\n')
for k in range(filelen):
#    atomels = atomInfo[1 + 33 * k + 4]
#    atomel = atomels[-1]
    atom2n = 'bondInfo[' + str(k + 1) + '].atom2.atomno	'
    atom1n = 'bondInfo[' + str(k + 1) + '].atom1.atomno	'
    atom2in = 'bondInfo[' + str(k + 1) + '].atom2.atomIndex	'
    atom1in = 'bondInfo[' + str(k + 1) + '].atom1.atomIndex	'

    for j in range(18):
        each = bondInfo[k * 18 + j]
        if each.find('atom2.atomno') != -1:           
            atom2no = each.replace(atom2n,'')
        if each.find('atom1.atomno') != -1:
            atom1no = each.replace(atom1n,'')
        if each.find('atom2.atomIndex') != -1:
            atom2ind = each.replace(atom2in,'')
        if each.find('atom1.atomIndex') != -1:
            
            atom1ind = each.replace(atom1in,'')
    bondBIn = SubElement( bondnum, 'bond')
    bondIn = SubElement(bondBIn, 'bond')
    bondIn.set('atomNo1', atom1no)
    bondIn.set('atomNo2', atom2no)
    #atomIn.set('atom1ind', atom1ind)
    #atomIn.set('atom2ind', atom2ind)

    #bondOut.write(str(k+1) + '        ' + atom1no + '         ' + atom1ind + '       ' + atom2no + '         ' + atom2ind + '\n')





#atomOut.write('a'+'\n')
#bondOut.write('b' + '\n')


atomInfofile.close()
bondInfofile.close()

#tree = ET.ElementTree("Atom+Bond")
#tree.write("Atom.xml")

myStr=myPrettify(root)
Atomxml.write(myStr)
Atomxml.close()
#atomOut.close()
#bondOut.close()
