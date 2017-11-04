import os
import sys
print 111

def displayFile(file):
    unPath = sys.executable
    unPath = unPath[0: unPath.rfind(os.sep)]
    newname = file[0:file.rfind('.')] + '.py'
    command = "python -u " + unPath + "\scripts\uncompyle2 " + file + ">" + newname
    try:
        os.system(command)
    except:
        pass

print 'init'

displayFile('C:\\Users\\jack\\Downloads\\pyc\\NE_class.pyc')
print 'finished'