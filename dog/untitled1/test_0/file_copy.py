import os, re

def fileRename(source, target):
    if not os.path.isfile(source):
        raise Exception('Can not find path %s' % source)
    dir_path = os.path.dirname(target)
    if not os.path.isdir(dir_path):
        os.makedirs(dir_path)
    os.rename(source, target)

source_dir = 'D:/assets_library'
target_dir = 'C:\Users\jack\Pictures\qkt\dog'
file_filters = ['bird', 'dog']

files = dict()
for item in os.walk(source_dir):
    for i in item[2]:
        for f in file_filters:
            if re.match('.*%s.*' % f, i):
                source = os.path.join(item[0], i)
                target = os.path.join(target_dir, f, i)
                files[source] = target
                break
for source, target in files.items():
    print source
    # fileRename(source, target)


