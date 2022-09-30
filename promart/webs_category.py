import sys
sys.path.append('/Users/javier/GIT/fala') 
from wong.g_var import path_promart


array_tec=[]

f = open(path_promart, "r")
x = f.readlines()

for i in x:
   array_tec.append(i.rstrip()) 

