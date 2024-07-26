import logging
import asyncio
import aiohttp
from motor.motor_asyncio import AsyncIOMotorClient
from decouple import config
import gc
import re
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def save_data_to_mongo_db(collection, sku, brand, product, list_price, best_price, card_price, link, image, dsct, card_dsct):
    data = {
        "_id": sku,
        "sku": sku,
        "brand": str(brand),
        "product": str(product),
        "list_price": float(list_price),
        "best_price": float(best_price),
        "card_price": float(card_price),
        "web_dsct": float(dsct),
        "card_dsct": float(card_dsct),
        "link": str(link),
        "image": str(image),
    }
    await collection.update_one({"_id": sku}, {"$set": data}, upsert=True)

async def send_telegram(session, message, foto, bot_token, chat_id, max_retries=5):
    if not foto or len(foto) <= 4:
        foto = "https://image.shutterstock.com/image-vector/no-image-available-sign-absence-260nw-373243873.jpg"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
        'Referer': 'https://home.ripley.com.pe'
    }

    backoff = 1
    for _ in range(max_retries):
        try:
            async with session.get(foto, headers=headers) as response:
                response.raise_for_status()
                photo_data = await response.read()

            async with session.post(
                f'https://api.telegram.org/bot{bot_token}/sendPhoto',
                data={'chat_id': chat_id, 'caption': str(message), "parse_mode": "HTML"},
                files={'photo': ('photo.jpg', photo_data)},
            ) as telegram_response:
                telegram_response.raise_for_status()
            logging.info("Message sent via Telegram.")
            return
        except aiohttp.ClientResponseError as e:
            if e.status == 429:
                logging.warning(f"Error 429: Too Many Requests. Retrying in {backoff} seconds...")
                await asyncio.sleep(backoff)
                backoff *= 2
            else:
                logging.error(f"HTTP Error: {e}")
                break
        except Exception as e:
            logging.error(f"Error sending message: {e}")
            break
    logging.error("Max retries reached. Exiting.")

async def auto_telegram_between_values(session, db, ship_db1, ship_db2, bot_token, chat_id, percentage1, percentage2, collection_name):
    collection = db[collection_name]
    collection_1 = db[ship_db1]
    collection_2 = db[ship_db2]

    query = {
        "$or": [
            {"web_dsct": {"$gte": percentage1, "$lte": percentage2}},
            {"card_dsct": {"$gte": percentage1, "$lte": percentage2}},
        ],
        "date": datetime.now().strftime("%Y-%m-%d"),
    }

    async for i in collection.find(query):
        data_live = {
            "sku": str(i["sku"]),
            "best_price": float(i["best_price"]),
            "list_price": float(i["list_price"]),
            "card_price": float(i["card_price"]),
            "web_dsct": float(i["web_dsct"]),
            "card_dsct": float(i["card_dsct"]),
        }
        
        data_saved = await collection_1.find_one({'sku': i['sku']})
        
        if data_saved and data_live != {k: data_saved[k] for k in data_live}:
            msn = create_message(i)
            foto = i["image"].replace("http:", "https:") if "http:" in i["image"] else i["image"]
            
            await send_telegram(session, msn, foto, bot_token, chat_id)
            await save_data_to_mongo_db(collection_1, **data_live)

def create_message(i):
    # Create message logic here (omitted for brevity)
    pass

async def buscador(config):
    client = AsyncIOMotorClient(config["mongo_db"])
    db = client[config["bd_name"]]

    async with aiohttp.ClientSession() as session:
        while True:
            try:
                await auto_telegram_between_values(
                    session,
                    db,
                    config["bd1"],
                    config["bd2"],
                    config["bot_token"],
                    config["chat_id"],
                    config["dsct"],
                    config["dsct2"],
                    config["collection_name"]
                )
            except Exception as e:
                logging.error(f"An exception occurred: {e}")
            await asyncio.sleep(60)  # Wait for 60 seconds before next iteration

if __name__ == "__main__":
    config = {
        "mongo_db": "192.168.8.66:27017",
        "chat_id": "-1001811194463",
        "bot_token": "6664469425:AAFeuvjckKSK9sM0nsLCKbgGgJomAqXpGLA",
        "collection_name": "scrap",
        "bd_name": "saga",
        "bd1": "bd1",
        "bd2": "bd2",
        "dsct": 30,
        "dsct2": 100,
    }
    
    try:
        asyncio.run(buscador(config))
    except KeyboardInterrupt:
        logging.info("Program interrupted by user")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")