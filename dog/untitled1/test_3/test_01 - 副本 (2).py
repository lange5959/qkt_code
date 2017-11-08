# coding=ascii
# def main():
#     name = '1'
#     # name = name.encode('utf-8')
#     for i in range(10):
#         with open("test_%s.py" % i, "wb") as f:
#             f.write(name)
#
# main()
# #

import codecs
f = codecs.open('intimate2.bat','w','ascii')
name = '1'
print type(name)

f.write(name)

f.close()

import sys
print sys.getfilesystemencoding()