from numpy import append
from saga import scrap

print("esto es una prueba")
web_url=[]

for i in range(2):
    print("entra al for")
    if i <=0:
        continue
    print(i)
    url = var.current_url2+str(i)
    print(url)

    web_url.append(url)

    #print(web_url)

for idx, val in enumerate(list(web_url)):

   print(val)
   scrap(val)




