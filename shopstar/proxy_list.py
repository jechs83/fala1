
import random
import sys
sys.path.append('/Users/javier/GIT/fala') 

proxies=[]

f = open("/Users/javier/GIT/fala/shopstar/urls/proxy.txt", "r")
x = f.readlines()
for i in x: 
    proxies.append(i.rstrip())

