# coding=gbk
import codecs

f = codecs.open('intimate.txt','a','utf-8')
f.write(u'����')
s = '����'
f.write(s.decode('gbk'))
f.close()

f = codecs.open('intimate.txt','r','utf-8')
s = f.readlines()
f.close()
for line in s:
    print line.encode('gbk')