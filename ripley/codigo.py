
import requests
from bs4 import BeautifulSoup
import os
import sys
from urllib import response 

def ripley(categoria, base_url): 
    ''' 
    base_url ejemplo = https://simple.ripley.com.pe/tecnologia/celulares/celulares-y-smartphones?source=menu&page=__PG__ 
    ''' 
    data = {'Categoria':[],'Tienda':[],'Titulo':[],'URL':[],'P_Normal': [],'P_Oferta': [],'P_Tarjeta':[],'Descuento':[]} 
    pg = 1 
    while pg <= 30: 
        url = base_url.replace("__PG__", str(pg)) 
        headers = funcs_scraper.get_user_agent() 
        r = requests.get(url, headers=headers) 
        s = BeautifulSoup(r.text, 'lxml') 
        #  Test si página no existe 
        if s.find('div', attrs={'class': 'catalog-container'}) is None: break 
        try:  
            if 'ya no se encuentra disponible' in s.find('div', attrs={'class': 'error-page'}).get_text().lower(): break 
        except: pass 
         
        #  2 maneras de mostrar los productos, depende de cada categoría 
        productos = s.find('div', attrs={'class': 'catalog-container'}).find_all('a', attrs={'class': 'catalog-product-item'}) 
        if len(productos) == 0: 
            productos = s.find('div', attrs={'class': 'catalog-container'}).find_all('div', attrs={'class': 'ProductItem'}) 
             
        for producto in productos: 
            try: 
                #  Verificar fura de stock, modo 1 
                agotado = producto.find('div', attrs={'class': 'catalog-product-details__tag'}).get_text().lower() 
                if 'agotado' in agotado or 'no disponible' in agotado or 'pronto disponible' in agotado: 
                    del agotado 
                    continue 
            except: 
                pass 
            try: 
                #  Verificar fura de stock, modo 2 
                agotado = producto.find('div', attrs={'class': 'ProductItem__BuyButton--disabled'}).get_text().lower() 
                if 'agotado' in agotado or 'no disponible' in agotado or 'pronto disponible' in agotado: 
                    del agotado 
                    continue 
            except: 
                pass 
 
            try: 
                p_name = producto.find('div', attrs={'class': 'catalog-product-details__name'}).get_text().title() 
            except: 
                p_name = producto.find('div', attrs={'class': 'ProductItem__Name'}).get_text().title() 
            try: 
                p_oferta = producto.find('li', attrs={'title': 'Precio Internet'}).get_text() 
                p_oferta = float(funcs_scraper.reemplazar_cadena(p_oferta, [",","S/."," ","S/","&nbsp"])) 
            except: 
                continue 
            # 
            try: 
                p_normal = producto.find('li', attrs={'title': 'Precio Normal'}).get_text() 
                p_normal = float(funcs_scraper.reemplazar_cadena(p_normal, [",","S/."," ","S/","&nbsp"])) 
            except: 
                p_normal = p_oferta 
            try: 
                p_tarjeta = producto.find('li', attrs={'title': 'Precio Ripley'}).get_text() 
                p_tarjeta = float(funcs_scraper.reemplazar_cadena(p_tarjeta, [",","S/."," ","S/","&nbsp"])) 
            except: 
                p_tarjeta = p_oferta 
            try: 
                p_url = producto.find('div',attrs={'class':'ProductItem__Name'}).find('div',attrs={'class':'ProductItem__Name'}).get('href') 
                p_url =  "".join(["https://simple.ripley.com.pe", p_url])  
            except: 
                p_url = "".join(["https://simple.ripley.com.pe", producto.get('href')]) 
            descuento = round(float((p_normal - p_tarjeta) / p_normal * 100), 2) 
 
            if funcs_scraper.filtros_personal(categoria, p_tarjeta, descuento, p_name.lower()) is False: continue 
 
            #  Saving products in the lists created at first 
            data['Categoria'].append(categoria) 
            data['Tienda'].append("Ripley") 
            data['Titulo'].append(p_name) 
            data['URL'].append(p_url) 
            data['P_Normal'].append(p_normal) 
            data['P_Oferta'].append(p_oferta) 
            data['P_Tarjeta'].append(p_tarjeta) 
            data['Descuento'].append(descuento)


         
    data = pd.DataFrame(data) 
    #  Delete repeated urls 
    data = data.drop_duplicates(subset=['URL'], keep='first') 
    return data