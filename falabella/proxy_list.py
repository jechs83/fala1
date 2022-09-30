

proxies=[]
path='/Users/javier/GIT/fala/ripley/urls/proxies.txt'
f = open(path, "r")
x = f.readlines()
for i in x: 
    proxies.append(i.rstrip())
