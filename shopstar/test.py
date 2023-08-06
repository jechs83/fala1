urls = [("https://shopstar.pe/tecnologia/computo?order=OrderByReleaseDateDESC&page="),
        
        ("https://shopstar.pe/tecnologia/televisores?order=OrderByReleaseDateDESC&page=")
        ]

websites = []
for i,v in enumerate  (urls) :
        for e in range(2):
            websites.append(v+str(e+1))
grouped_arrays = [websites[i:i + len(urls)] for i in range(0, len(websites), len(urls))]

print(grouped_arrays)
for webs in grouped_arrays:

    for web  in webs:

        print(web)
