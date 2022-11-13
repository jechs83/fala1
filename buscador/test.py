

array_a = [{"a","b","c"},{ "h","t","y","u"}, {"s","x","f"}]

array_b = [{"a","b","c","d"},{ "h","t","y","u"}, {"s","x","f"}]

new=[]
for i in array_a:
    if i not in array_b:
        new.append(i)

print(new)



