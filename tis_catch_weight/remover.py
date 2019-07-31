import os
import codecs
script_dir = os.path.dirname(__file__)
script_dir = '/home/jasad/PycharmProjects/cw812_cv/catchw8_2.0_cv'
files=[]
for r, d, f in os.walk(script_dir):
    for file in f:
        if '.txt' and '.py' and not 'remover.py' in file:
            files.append(os.path.join(r, file))
for f in files:
 fileHandler=open(f,'rb')
 listOfLines=fileHandler.readlines()
 print('******',f,'*******')
 fileHandler=open(f,'r+')
 lookup = '#'

 with codecs.open(f,errors='ignore') as fi:
    for num, line in enumerate(fi,1)  :
     if lookup in line:
            print ('found at line:', num)
 
 listOfLines=fileHandler.readlines()
 with open(f,"w") as f:
  for line in listOfLines [:2]:
   f.write(line)
  for line in listOfLines[3:]:
   if not line.strip().startswith('#'):
    f.write(line)
 






 
     
 
