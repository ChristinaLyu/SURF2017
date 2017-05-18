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






