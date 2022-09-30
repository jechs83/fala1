
import random
import sys
sys.path.append('/Users/javier/GIT/fala') 

proxies=[]

f = open("/Users/javier/GIT/fala/ripley/urls/proxies.txt", "r")
x = f.readlines()
for i in x: 
    proxies.append(i.rstrip())


x = random.choice(proxies)
print(x)