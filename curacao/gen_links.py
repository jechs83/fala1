urls = open ("/Users/javier/GIT/fala/curacao/test.txt", "r" )
t = urls.readlines()

part = "&pageSize=12&pageGroup=Category&urlLangId=-24"



for idx,v in enumerate( t):
    f = 12
    for i in range (100):
        print()
        print(v+str(f*(i+1))+part)

