# coding=utf8
# controllerLibrary
from maya import cmds
import os
import json

USERAPPDIR = cmds.internalVar(userAppDir=True)
# u'C:/Users/ATX/Documents/maya/'
DIRECTORY = os.path.join(USERAPPDIR, "cat")
# u'C:/Users/ATX/Documents/maya/cat'
# print '<'*100


def createDirectory(directory=DIRECTORY):
    if not os.path.exists(directory):
        if not os.path.exists(directory):
            os.mkdir(directory)


class ControllerLibrary(dict):
    def find(self, directory=DIRECTORY):
        self.clear()
        if not os.path.exists(directory):
            return
        # files = os.listdir(directory)
        files = list()
        mayaFiles = []
        for item in os.walk(directory):
            for i in item[2]:
                files.append(i)
                if i.endswith('.ma'):
                    source = os.path.join(item[0], i)

                    mayaFiles.append(source)
        # print files[0]
        # print len(files), '<'*100
        # print mayaFiles[0]
        # print len(mayaFiles), '<'*100
        # mayaFiles = [f for f in files if f.endswith('.ma')]
        # [dog.ma,...]
        for ma in mayaFiles:
            file_name = os.path.basename(ma)
            name, ext = os.path.splitext(file_name)
            # maya.ma -- maya, ma
            # path = os.path.join(directory, ma)
            path = os.path.dirname(ma)
            path_ma = os.path.normpath(path) + '/' + file_name
            # ../../dog.ma
            infoFile = '%s.json' % name
            # name.json
            if infoFile in files:
                infoFile = os.path.join(path, infoFile)
                # infoFile is full_path
                try:
                    with open(infoFile, 'r') as f:
                        # json_str = f.read()
                        info = json.load(f)
                        # pprint.pprint(info)
                except:
                    pass
            else:
                info = {}

            screenshot = '%s.jpg' % name
            if screenshot in files:
                info['screenshot'] = os.path.join(directory, screenshot)

            info['name'] = name
            info['path'] = path_ma

            self[name] = info

    def load(self, name):
        try:
            path = self[name]['path']
        except:
            path = ''
        # print path
        return path