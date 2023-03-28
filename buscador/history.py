import pandas as pd
from pymongo import MongoClient
import io
from decouple import config

# client = MongoClient(config("MONGO_DB"))
# db5 = client["scrap"]
# collection5 = db5["scrap"]

# date_list = []
# price_list = []

# def historic_table(sku):
#     cod = collection5.find({"sku":str(sku)})
#     for i in cod:
#         date_list.append(i["date"])
#         price_list.append(i["best_price"])
#         name = (i["product"])
#         brand = i["brand"]

#     # Create a DataFrame
#     data = {'date': date_list, 'price': price_list}
#     df = pd.DataFrame(data)
#     df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y')

#     # Convert DataFrame to HTML table
#     html_table = df.to_html()

#     # Write HTML table to file
#     with io.open('/Users/javier/GIT/fala/buscador/historical.html', 'w', encoding='utf-8') as f:
#         f.write(html_table)

# Example usage#
#historic_table('116264156')



client = MongoClient(config("MONGO_DB"))
db5 = client["scrap"]
collection5 = db5["scrap"]

date_list = []
price_list = []

def historic_table(sku):
    cod = collection5.find({"sku":str(sku)})
    for i in cod:
        date_list.append(i["date"])
        price_list.append(i["best_price"])
        name = (i["product"])
        brand = i["brand"]

    # Create a DataFrame
    data = {'date': date_list, 'price': price_list}
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y')

    # Find index of row with minimum price
    min_price_idx = df['price'].idxmin()

    # Add CSS styles to HTML table
    styles = [
        {
            'selector': 'table',
            'props': [
                ('border-collapse', 'collapse'),
                ('width', '100%'),
                ('font-family', 'Arial, sans-serif'),
                ('font-size', '14px')
            ]
        },
        {
            'selector': 'th, td',
            'props': [
                ('border', '1px solid #dddddd'),
                ('text-align', 'left'),
                ('padding', '8px')
            ]
        },
        {
            'selector': 'th',
            'props': [
                ('background-color', '#dddddd')
            ]
        },
        {
            'selector': 'tr:nth-child(' + str(min_price_idx + 1) + ')',
            'props': [
                ('background-color', 'green'),
                ('color', 'white')
            ]
        }
    ]

    # Convert DataFrame to HTML table with CSS styles
    html_table = df.to_html(classes='table', index=False, border=0, escape=False)
    html_table = '<style>' + ''.join([f'{s["selector"]} {{ {"; ".join([f"{p[0]}: {p[1]}" for p in s["props"]])} }}' for s in styles]) + '</style>\n' + html_table

    # Write HTML table to file
    with io.open('/Users/javier/GIT/fala/buscador/historical.html', 'w', encoding='utf-8') as f:
        f.write(html_table)

# Example usage
#historic_table('example_sku')
