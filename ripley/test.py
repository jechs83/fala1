from random import random
import sys
sys.path.append('/Users/javier/GIT/fala') 
from wong.g_var import path_ripley_links


array_tec=[]

f = open(path_ripley_links, "r")
x = f.readlines()

for i in x:
    array_tec.append(i.rstrip()) 

webs= []
for i,v in enumerate(array_tec):
    for i in range (3):
        webs.append(v+(str(i+1)))

x= print(random.choice(webs))