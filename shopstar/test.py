urls = ["url1" , "url 2"]
    

websites = []
for i in (urls):
        for e in range(4):
            websites.append(i+str(e+1))
grouped_arrays = [websites[i:i + len(urls)] for i in range(0, len(websites), len(urls))]




print(grouped_arrays)
# count = 0
# for webs in grouped_arrays:

  
#     for web  in webs:
#         count = count +1
#         print(web)
#         print(count)
#         if count == 2:
#             break  # Only exit the inner loop

        
