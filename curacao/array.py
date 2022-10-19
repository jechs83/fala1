array_tec=[]
arg_ = "/Users/javier/GIT/fala/curacao/urls/link1.txt"

# f = open(arg_, "r")
# x = f.readlines()

# for i in x:
#     array_tec.append(i.rstrip()) 


# print(array_tec)

with open(arg_) as load_file:
    data = [tuple(line.split()) for line in load_file]


for i in data:
    print()
    print(i[0])
    print()
    print(i[1])
