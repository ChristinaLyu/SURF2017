#bondInfo.py
#file to print txt file of bond information
import sys
def main():
    filename = sys.argv[1]
    print(filename)
    file = open(filename, 'r')
    file = file.read().splitlines()
    
    linelist = []
    printline = []
    for line in file:
        linelist.append(line)
    n = len(linelist)-1
    m = n/18
    printline.append(linelist[0])
    linelist[1:]
    print('Bind number = ' + str(m))

    for k in range(m):
        bondInfo = ''
        atom2numl = linelist[18*k + 6]
        atom2num = atom2numl[-1]
        atom2indl = linelist[18*k + 7]
        atom2ind = atom2indl[-1]
        atom1numl = linelist[18*k + 11]
        atom1num = atom1numl[-1]
        atom1indl = linelist[18*k + 12]
        atom1ind = atom1indl[-1]
        print(bondInfo + 'bondInfo[' + str(k+1) + ']   atom2.atomno = ' + str(atom2num) + '   atom1.atomno = ' + str(atom1num) + '   atom2.index = ' + str(atom2ind) + '   atom1.index = ' + str(atom1ind))
        printline.append(bondInfo)



main()
