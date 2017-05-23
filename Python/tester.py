'''
    File:           tester.py
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
testerResult = outputFolderPath + '/testerResult.csv'
badResult = outputFolderPath + '/badResult.csv'
if not os.path.exists(outputFolderPath):
    os.system('mkdir '+ outputFolderPath)

testerResultFile = open(testerResult, 'w')
badResultFile = open(badResult, 'w')
print "Testing start:"


for crtInputFile in os.listdir(inputDataFolderPath):
    print "--- File: " + crtInputFile
    k = k + 1
    
    crtInputFilePath = inputDataFolderPath + '/' + crtInputFile + ' '
    fileName = crtInputFile.split('.')[0]
    outFilePath = outputFolderPath + '/test' + fileName + '.xml'
    command = 'python ' + inputPythonFilePath + ' ' + crtInputFilePath + outFilePath
    
    child = subprocess.Popen(command, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, shell=True)
    streamdata = child.communicate()[0]
    rc = child.returncode
    testerResultFile.write(crtInputFile + ',' + str(rc) + '\n')
    if rc != 0:
        badResultFile.write(crtInputFile + ',' + str(rc) + '\n')

    # err = subprocess.check_output(command, stderr = subprocess.STDOUT, shell = True)
    # err = subprocess.check_output(command, stderr = subprocess.STDERR, shell = True)
    err = subprocess.check_output(command, ,shell = True)
    print "In tester.py: err = " + err
    
    if err != '0':
        print "Error:" + err
    else:
        print "No error!"

print "Testing finished"
testerResultFile.close()
badResultFile.close()
