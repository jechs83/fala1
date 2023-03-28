import matplotlib.pyplot as plt
import pandas as pd
from pymongo import MongoClient
import os
import pymongo
import mpld3
from bokeh.resources import CDN
from decouple import config
import pandas as pd
from bokeh.embed import file_html
from bokeh.io import save

import numpy as np
from bokeh.plotting import figure, show, output_file
from bokeh.models import HoverTool, ColumnDataSource


client = MongoClient(config("MONGO_DB"))
db5 = client["scrap"]
collection5 = db5["scrap"] 

date_list = []
price_list=[]


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


    # Find the index of the minimum price value
    min_price_index = np.argmin(price_list)

    # Create a ColumnDataSource object
    source = ColumnDataSource(data={
      
        'date': df['date'],
        'price': df['price'],
        
        'size': [12 if i == min_price_index else 8 for i in range(len(df))]
    })

    # Create a Figure object
    p = figure(title='Precio Historico \n'+ brand+"  "+name, x_axis_label='Fecha', y_axis_label='Precio', x_axis_type='datetime')

    # Plot the data
    p.line('date', 'price', source=source, line_width=2, line_color='blue')
    p.circle('date', 'price', source=source, size='size', fill_color='white', line_width=2, line_color='blue', legend_label='Precio')

    #  # Highlight the marker for the minimum price value
    # p.circle(df.loc[min_price_index, 'date'], df.loc[min_price_index, 'price'], size=12, fill_color='green', line_width=2, line_color='black', legend_label='Precio minimo')


    # Create a HoverTool object
    hover = HoverTool(
        tooltips=[
            ('Fecha', '@date{%F}'),
            ('Precio', '$@price{0.00}'),
        ],
        formatters={'@date': 'datetime'},
        mode='vline'
    )

    # Add the HoverTool to the figure
    p.add_tools(hover)

    # Save the chart as an HTML file
    save(p, output_file('/Users/javier/GIT/fala/buscador/historical.html'))

    html = file_html(p, CDN, "Precio Historico \n"+brand+"  "+name)

    # Return the HTML string
   
    return html
    # # Show the chart
    #show(p)
  


#historic_table("116264156")