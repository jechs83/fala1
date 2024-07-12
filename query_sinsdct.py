from pymongo import MongoClient
import itertools

def build_query(conditions, exclusions, date, max_price=None):
    query = {"$and": conditions + [{"date": date}]}
    
    if exclusions:
        for exclusion in exclusions:
            query["$and"].append({"product": {"$not": {"$regex": exclusion, "$options": "i"}}})
    
    if max_price:
        price_conditions = [
            {"list_price": {"$lte": max_price}},
            {"best_price": {"$lte": max_price}},
            {"card_price": {"$lte": max_price}}
        ]
        query["$and"].extend(price_conditions)
    
    query["$or"] = [
        {"list_price": {"$ne": 0}},
        {"best_price": {"$ne": 0}},
        {"card_price": {"$ne": 0}}
    ]
    
    return query

def productos_sin_dsct(ship_db1, ship_db2, bot_token, chat_id, bd_name, collection_name, date):
    client = MongoClient()
    db = client[bd_name]
    collection = db[collection_name]
    collection_1 = db[ship_db1]
    collection_2 = db[ship_db2]

    queries = {
        "laptop_query1": build_query(
            conditions=[
                {"product": {"$regex": r'\b(ryzen\s7|ryzen\s5|ryzen\s9|8gb|16gb|12gb|32gb)\b', "$options": "i"}},
                {"product": {"$regex": r'\b(laptop)\b', "$options": "i"}},
                {"product": {"$regex": r'\b(16GB|12GB)\b', "$options": "i"}},
                {"web_dsct": 0},
                {"card_dsct": 0},
            ],
            exclusions=[r'\b(reacondicionado|refurbished)\b'],
            date=date,
            max_price=2000
        ),
        
        "laptop_query2": build_query(
            conditions=[
                {"product": {"$regex": r'\b(i\s7|i7|i\s5|i5|ci7|ci5|ci9|i\s9|i9)\b', "$options": "i"}},
                {"product": {"$regex": r'\b(laptop)\b', "$options": "i"}},
                {"product": {"$regex": r'\b(16GB|12GB)\b', "$options": "i"}},
                {"web_dsct": 0},
                {"card_dsct": 0},
            ],
            exclusions=[r'\b(reacondicionado|refurbished)\b'],
            date=date,
            max_price=2000
        ),
        "refri_query": build_query(
            conditions=[
                {"product": {"$regex": r'\b(refrigeradora|lavadora|cocina|)\b', "$options": "i"}},
                {"brand": {"$regex": r'\b(samsung|lg|panasonic|sony|philips|hisense|indurama|bosch|oster|electrolux|coldex|daewoo|klimatic|mabe|sole|General\sElectric|Whirpool|frigidaire)\b', "$options": "i"}},
                {"web_dsct": 0},
                {"card_dsct": 0},
            ],
            exclusions=[],
            date=date,
            max_price=1200
        ),
        "celular_query": build_query(
            conditions=[
                {"product": {"$regex": r'\b(smartphone|celular|6gb|8gb|12gb|tablet|ipad)\b', "$options": "i"}},
                {"brand": {"$regex": r'\b(xiaomi|samsung|apple|lg|motorola|realme|oppo|vivo|redmi|honor|google|huawei|)\b', "$options": "i"}},
                {"web_dsct": 0},
                {"card_dsct": 0},
            ],
            exclusions=[r'\b(reacondicionado|refurbished)\b'],
            date=date,
            max_price=1000
        ),
        "tele_query": build_query(
            conditions=[
                {"product": {"$regex": r'\b(televisor|tele|55\"|50\"|60\"|65\"|70\"|75\"|80\"|82\"|85\")\b', "$options": "i"}},
                {"brand": {"$regex": r'\b(samsung|lg|panasonic|sony|philips|hisense|tlc|aoc|xiaomi|aiwa)\b', "$options": "i"}},
                {"web_dsct": 0},
                {"card_dsct": 0},
            ],
            exclusions=[r'\b(reacondicionado|refurbished)\b'],
            date=date,
            max_price=1000
        ),
        "iphone_query": build_query(
            conditions=[
                {"product": {"$regex": r'\b(iphone|pro|pro\smax|air|plus|macbook\spro|macbook)\b', "$options": "i"}},
                {"brand": {"$regex": r'\b(apple)\b', "$options": "i"}},
                {"web_dsct": 0},
                {"card_dsct": 0},
            ],
            exclusions=[r'\b(reacondicionado|refurbished|REACONDICIONADA)\b'],
            date=date,
            max_price=3000
        ),
        "zapatilla_query": build_query(
            conditions=[
                {"product": {"$regex": r'\b(zapatilla|zapatillas)\b', "$options": "i"}},
                {"web_dsct": {"$gte": 50, "$lte": 59}},
                {"card_dsct": {"$gte": 50, "$lte": 59}},
            ],
            exclusions=[],
            date=date
        ),
        "zapatilla_query2": build_query(
            conditions=[
                {"product": {"$regex": r'\b(zapatilla|zapatillas)\b', "$options": "i"}},
                {"web_dsct": 0},
                {"card_dsct": 0},
            ],
            exclusions=[],
            date=date,
            max_price=150
        )
    }

    results = itertools.chain(
        *[collection.find(query) for query in queries.values()]
    )

    for i in results:
        data_live = {
            "sku": i["sku"],
            "best_price": i["best_price"],
            "list_price": i["list_price"],
            "card_price": i["card_price"],
            "web_dsct": i["web_dsct"],
            "card_dsct": i["card_dsct"],
        }

        data_saved = collection_1.find_one({'sku': i['sku']})

        if data_saved:
            data_sv = {
                "sku": data_saved["sku"],
                "best_price": data_saved["best_price"],
                "list_price": data_saved["list_price"],
                "card_price": data_saved["card_price"],
                "web_dsct": data_saved["web_dsct"],
                "card_dsct": data_saved["card_dsct"],
            }
        else:
            data_sv = None

        if data_live != data_sv:
            web_d = "🔥" if i["web_dsct"] >= 70 else "🟢" if i["web_dsct"] > 50 else "🟡"
            card_d = "🔥" if i["card_dsct"] >= 70 else "🟢" if i["card_dsct"] > 50 else "🟡"
            
            list_price = f'🏷 <b>Precio lista:</b> {i["list_price"]}\n' if i["list_price"] != 0 else ""
            best_price = f'👉 <b>Precio web:</b> <b>{i["best_price"]}</b>\n' if i["best_price"] != 0 else ""
            card_price = f'💳 <b>Precio TC:</b> <b>{i["card_price"]}</b>\n' if i["card_price"] != 0 else ""
            card_dsct = f'💥 <b>Descuento TC:</b> %{i["card_dsct"]} {card_d}\n' if i["card_dsct"] != 0 else ""
            web_dsct = f'💵 <b>Descuento web:</b> %{i["web_dsct"]} {web_d}\n' if i["web_dsct"] != 0 else ""

            if any([list_price, best_price, card_price]):
                msn = (
                    "🌟🦙 <b>Detalles del Producto</b> 🦙🌟\n\n"
                    f'{i["image"]}\n'
                    f'✅ <b>Marca:</b> {i["brand"]}\n'
                    f'📦 <b>Producto:</b> {i["product"]}\n\n'
                    f'{list_price}{best_price}{card_price}\n'
                    f'{card_dsct}{web_dsct}'
                    f'🏬 <b
