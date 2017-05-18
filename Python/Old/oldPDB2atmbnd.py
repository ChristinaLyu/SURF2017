'''
    File:           oldPDB2atmbnd.py
    Author:         Christina Lyu
    Date created:   4/26/17
    Updates:
    Last modified:  5/17/17
    Python Version: 3.5.2

    Description:    output the number of atoms in a mmCIF/pdbx file
    Run format:     python oldPDB2atmbnd.py pathToInputCifFile pathToOutputTextFile
    Run example:    python oldPDB2atmbnd.py /Users/xxx/abc.cif /Users/xxx/
'''

from Bio import PDB
import os
import sys



#JMOL get path to Jmol.jar
JMOL = '/Users/ChristinaLyu/Desktop/Summer2017/External/JmolData.jar'
filename = sys.argv[1]

outfolder = sys.argv[2]

if not os.path.exists(outfolder):
    os.system('mkdir '+ outfolder)

os.system('java -jar '+ JMOL + ' -no  -j "load ' + filename + ' ; select all ; getproperty atomInfo;"  > ' + outfolder + '/atominfo_large.txt')
os.system('java -jar '+ JMOL + ' -no  -j "load ' + filename + ' ; select all ; getproperty bondInfo;"  > ' + outfolder + '/bondinfo_large.txt')

os.system('python /Users/ChristinaLyu/Desktop/Summer2017/Python/Old/oldUibi.py ' + outfolder + '/atominfo_large.txt '+ outfolder + '/bondinfo_large.txt ' + outfolder )




##os.system('mv Atom.xml ' + outfolder)
#os.system('mv bond.bnd ' + outfolder)
'''
script_name = structure + '.spt'
script = open(script_name, 'w')

script.write('load ' + filename + '; getProperty atomInfo; write'
'''








