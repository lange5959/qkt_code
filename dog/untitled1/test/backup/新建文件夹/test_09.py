#coding=utf-8
with open(r'C:\Users\jack\Documents\shelf_lb.txt','r') as txCahe:
    fullScrp=txCahe.read()
    txCahe.close
import re
reRex=re.compile(r'label=.*, p=projInfo,')
print(reRex.findall(fullScrp))