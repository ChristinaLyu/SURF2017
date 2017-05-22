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

inputPythonFilePath = sys.argv[1]
inputDataFolderPath = sys.argv[2]
outputFolderPath = sys.argv[3]

if not os.path.exists(outputFolderPath):
    os.system('mkdir '+ outputFolderPath)

print "Testing start:"


for crtInputFile in os.listdir(inputDataFolderPath):
    print "testing file: " + crtInputFile
    
    crtInputFilePath = inputDataFolderPath + '/' + crtInputFile + ' '
    fileName = crtInputFile.split('.')[0]
    outFilePath = outputFolderPath + '/test' + fileName + '.txt'
    command = 'python ' + inputPythonFilePath + ' ' + crtInputFilePath + outFilePath

    child = subprocess.Popen(command, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, shell=True)
    streamdata = child.communicate()[0]
    rc = child.returncode
    print streamdata
    print 'exit code = ' + str(rc)

print "Testing finished"
