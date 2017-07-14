from pymel.core import *
from lib import MyTimer
# @MyTimer.measure_time
import re
print '*'*100
path = sceneName()

version_str = path.split('.')[-2].lstrip('v')
type(version_str)

try:
    version_int = int(version_str)
except:
    path_split = path.split('.')
    path_split.insert(-1, 'v001')
    version_str = path_split[-2].lstrip('v')
    version_int = int(version_str)
    path = '.'.join(path_split)
new_version_str = str(version_int+1).zfill(3)
new_path = path.replace('.v%s.' % version_str, '.v%s.' % new_version_str)

saveAs(new_path)


