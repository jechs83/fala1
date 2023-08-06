urls = ["url1" , "url 2"]
import time  

websites = []
for i in urls:
    temp_array = []  # Create a temporary array for each iteration
    for e in range(4):
        temp_array.append(i + str(e + 1))
    websites.append(temp_array)  # Append the temporary array to the main list

print(websites)
time.sleep(30)
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

        
