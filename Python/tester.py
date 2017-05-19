'''
    File:           test_count.py
    Author:         Ileana Streinu with Christina Lyu
    Date created:   5/19/17
    Updates: 	    
    Last modified:  5/19/17
    Python Version: 3.2

    Description:    takes a counting python file and runs on its own dataset to check if it runs correctly
    Run format:     python test_count.py pathToInputPythonFile pathToOutputFile
    Run example:    python test_count.py /Users/xxx/abc.py /Users/xxx/abc.txt
'''
import os
import sys
import subprocess

inputFile = sys.argv[1]
folder = sys.argv[2]
outPath = sys.argv[3]
k = 0
if not os.path.exists(outPath):
    os.system('mkdir '+ outPath)
outPath = outPath + '/temp'
if not os.path.exists(outPath):
    os.system('mkdir '+ outPath)

print "Testing start:"
for file in os.listdir(folder):
    print "testing file: " + file
    k = k + 1
    testFile = folder + '/' + file + ' '
    first = file.split('.')[0]
    outFile = outPath + '/test' + first + '.txt'
    command = 'python ' + inputFile + ' ' + testFile + outFile

    err = subprocess.check_output(command, stderr = subprocess.STDOUT, shell = True)
    if err != "":
        print "Output:" + err
    else:
        print "no error!"

