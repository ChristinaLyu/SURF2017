# For this file to work, you must set
# PYTHONPATH to point to the Settings folder containing this file.
#
# On Mac / Linux you add the following to your .bash_profile or .bashrc file:
#
# export PYTHONPATH=$PYTHONPATH:/var/www/KinariSvr/Kernel/Settings/:/var/www/KinariSvr/Kernel/Lib/
#
# on MAMP create a file called envvars in /MAMP/Library/bin with the following line
#
# export PYTHONPATH=/Users/johnbowers/Documents/Kinari/src/KinariSvr/Kernel/Settings/:/Users/johnbowers/Documents/Kinari/src/KinariSvr/Kernel/Lib/
#
# (except replace /Users/johnbowers with your home folder.)
#

from os.path import dirname, abspath

KINARISVR_PATH = dirname(dirname(dirname(abspath(__file__))))

EXTERNAL_PATH = KINARISVR_PATH + "/External/"

JMOL_PATH = EXTERNAL_PATH + "jmol/"
JMOLDATA_JAR = JMOL_PATH + "JmolData.jar"

LIB = KINARISVR_PATH + "/Mojtaba/pebble/python/code/lib/"