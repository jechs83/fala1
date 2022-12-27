from decouple import config


import random
urls = []
lista = open("/Users/javier/GIT/fala/hiraoka/x.txt", "r")
for i in lista:
    urls.append(i)
#web_url = random.choice(config("PROXY"))

web_url = random.choice(urls)

print(web_url)