'''
    File:           tester.py
    Author:         Ileana Streinu with Christina Lyu
    Date created:   5/19/17
    Updates: 	    
    Last modified:  5/25/17
    Python Version: 3.2

    Description:    takes a counting python file and runs on its own dataset to check if it runs correctly
    Run format:     python tester.py pathToInputPythonFile interruptTime pathToOutputFile
    Run example:    python tester.py /Users/xxx/abc.py 20 /Users/xxx/abc.txt
'''
import os
import sys
import subprocess
from os.path import isfile
import signal
import time

class TimeoutException(Exception):   # Custom exception class
    pass

def timeout_handler(signum, frame):   # Custom signal handler
    raise TimeoutException

def main():
    inputPythonFilePath = sys.argv[1]
    inputDataFolderPath = sys.argv[2]
    executeTime = int(sys.argv[3])
    outputFolderPath = sys.argv[4]


    testerResult = outputFolderPath + '/testerResult.csv'
    badResult = outputFolderPath + '/badResult.csv'
    timing = outputFolderPath + '/timingFile.csv'
    if not os.path.exists(outputFolderPath):
        os.system('mkdir '+ outputFolderPath)
    testerResultFile = open(testerResult, 'w')
    testerResultFile.write('fileName,exitCode,meaning' + '\n')
    badResultFile = open(badResult, 'w')
    badResultFile.write('fileName,exitCode,meaning' + '\n')
    timingFile = open(timing, 'w')
    timingFile.write('fileName,runTime' + '\n')
    print "Testing start:"
    signal.signal(signal.SIGALRM, timeout_handler)

    for crtInputFile in os.listdir(inputDataFolderPath):
        if isfile(crtInputFile):
            continue

        print "--- File: " + crtInputFile
        crtInputFilePath = inputDataFolderPath + '/' + crtInputFile + ' '
        fileName = crtInputFile.split('.')[0]
        outFilePath = outputFolderPath + '/test' + fileName + '.xml'

        signal.alarm(executeTime)
        try:
            t0 = time.clock()
            command = 'python ' + inputPythonFilePath + ' ' + crtInputFilePath + outFilePath
            child = subprocess.Popen(command, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, shell=True)
            streamdata = child.communicate()[0]
            rc = child.returncode
            t1 = time.clock()
            t = t1 - t0
            if rc == 0:
                testerResultFile.write(crtInputFile + ',' + str(rc) + ',no_error' + '\n')
                timingFile.write(crtInputFile + ',' + str(t) + '\n')
            if rc == 1:
                testerResultFile.write(crtInputFile + ',' + str(rc) + ',error_in_given_file' + '\n')
                badResultFile.write(crtInputFile + ',' + str(rc) + ',error_in_given_file' + '\n')

            if rc == 2:
                testerResultFile.write(crtInputFile + ',' + str(rc) + ',error_in_Jmol' + '\n')
                badResultFile.write(crtInputFile + ',' + str(rc) + ',error_in_Jmol' + '\n')

        except TimeoutException:
            testerResultFile.write(crtInputFile + ',3' + ',program_killed' + '\n')
            badResultFile.write(crtInputFile + ',3' + ',program_killed' + '\n')
            print 'continue'
            continue
    print "Testing finished"
    testerResultFile.close()
    badResultFile.close()

main()



