import logging
from pymongo import MongoClient
from decouple import config
import time
import gc
import re
import requests
from datetime import date, datetime
import pytz

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

mongo = "192.168.8.66:27017"
client = MongoClient(mongo)

bot_tokens = [
    "6664469425:AAFeuvjckKSK9sM0nsLCKbgGgJomAqXpGLA",
    "6747921067:AAG0frH1swAvpVjn_nc4mQ2ND_dm014njLI"
]
chat_id = "-1001811194463"

date_now = date.today().strftime("%d/%m/%Y")

def get_next_bot_token(index):
    return bot_tokens[index % len(bot_tokens)]

def save_data_to_mongo_db(sku, brand, product, list_price,
                          best_price, card_price, link, image, dsct, card_dsct, data_base, collection_db):
    db = client[data_base]
    collection = db[collection_db]

    data = {
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

    collection.update_one({"sku": sku}, {"$set": data}, upsert=True)

def send_telegram(message, foto, bot_token, chat_id, max_retries=5):
    if not foto or len(foto) <= 4:
        foto = "https://image.shutterstock.com/image-vector/no-image-available-sign-absence-260nw-373243873.jpg"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
        'Referer': 'https://home.ripley.com.pe'
    }

    retries = 0
    backoff = 1

    while retries < max_retries:
        try:
            response = requests.get(foto, headers=headers)
            response.raise_for_status()
            photo_data = response.content

            telegram_response = requests.post(
                f'https://api.telegram.org/bot{bot_token}/sendPhoto',
                data={'chat_id': chat_id, 'caption': str(message), "parse_mode": "HTML"},
                files={'photo': ('photo.jpg', photo_data)},
            )

            telegram_response.raise_for_status()
            logging.info("Message sent via Telegram.")
            return

        except requests.exceptions.HTTPError as e:
            if telegram_response.status_code == 429:
                retries += 1
                logging.warning(f"Error 429: Too Many Requests. Retrying in {backoff} seconds...")
                time.sleep(backoff)
                backoff *= 2
            else:
                logging.error(f"HTTP Error: {e}")
                break
        except requests.exceptions.RequestException as e:
            logging.error(f"Request Error: {e}")
            break
        except Exception as e:
            logging.error(f"Error sending message: {e}")
            break

    logging.error("Max retries reached. Exiting.")

def auto_telegram_between_values(ship_db1, ship_db2, bot_tokens, chat_id, porcentage1, porcentage2, data_base, collection_db):
    logging.info("Searching for products...")
    db = client[data_base]
    collection = db[collection_db]
    collection_1 = db[ship_db1]
    collection_2 = db[ship_db2]

    scrap_search = collection.find({
        "$or": [
            {"web_dsct": {"$gte": porcentage1, "$lte": porcentage2}},
            {"card_dsct": {"$gte": porcentage1, "$lte": porcentage2}},
        ],
        "date": date_now,
    })

    logging.info("Retrieved data from main database")
    message_count = 0

    for i in scrap_search:
        data_live = {
            "sku": str(i["sku"]),
            "best_price": float(i["best_price"]),
            "list_price": float(i["list_price"]),
            "card_price": float(i["card_price"]),
            "web_dsct": float(i["web_dsct"]),
            "card_dsct": float(i["card_dsct"]),
        }

        try:
            data_saved = collection_1.find_one({'sku': str(i['sku'])})
            data_sv = {
                "sku": str(data_saved["sku"]),
                "best_price": float(data_saved["best_price"]),
                "list_price": float(data_saved["list_price"]),
                "card_price": float(data_saved["card_price"]),
                "web_dsct": float(data_saved["web_dsct"]),
                "card_dsct": float(data_saved["card_dsct"]),
            }
        except:
            data_sv = None

        if data_live != data_sv:
            # Prepare message (using the existing logic)
            web_d = "🟡" if i["web_dsct"] <= 50 or i["card_dsct"] <= 50 else "🟢" if 50 < i["web_dsct"] <= 69 or 50 < i["card_dsct"] <= 69 else "🔥🔥🔥🔥🔥🔥🔥"
            
            list_price = '🏷 <b>Precio lista:</b> ' + str(i["list_price"]) + "\n" if i["list_price"] != 0 else ""
            best_price = '👉 <b>Precio web:</b> <b>' + str(i["best_price"]) + "</b>" + "\n" if i["best_price"] != 0 else ""
            card_price = '💳 <b>Precio TC:</b> <b>' + str(i["card_price"]) + "</b>" + "\n" if i["card_price"] != 0 else ""
            card_dsct = "💥 <b>Descuento TC:</b> %" + str(i["card_dsct"]) + "\n" if i["card_dsct"] != 0 else ""
            web_dsct = "💵 <b>Descuento web:</b> %" + str(i["web_dsct"]) + web_d + "\n" if i["web_dsct"] != 0 else ""

            foto = i["image"]
            if "http:" in foto:
                foto = foto.replace("http:", "https:")
            if len(foto) < 5:
                foto = "https://westsiderc.org/wp-content/uploads/2019/08/Image-Not-Available.png"

            msn = (
                "🌟🦙 <b>Detalles del Producto</b> 🦙🌟\n\n" +
                "# sku: " + str(i["sku"]) + "\n" +
                "✅ <b>Marca:</b> " + str(i["brand"]) + "\n" +
                "📦 <b>Producto:</b> " + str(i["product"]) + "\n\n" +
                list_price + best_price + card_price + "\n" +
                card_dsct + web_dsct +
                "🏬 <b>Market:</b> " + str(i["market"]) + "\n" +
                "🕗 <b>Fecha y Hora:</b> " + str(i["date"]) + " " + str(i["time"]) + "\n" +
                "🔗 <b>Enlace:</b> <a href='" + str(i["link"]) + "'>Link aquí</a>\n\n"
            )

            save_data_to_mongo_db(i["sku"], i["brand"], i["product"], i["list_price"],
                                  i["best_price"], i["card_price"], i["link"], i["image"],
                                  i["web_dsct"], i["card_dsct"], data_base, ship_db1)

            bot_token = get_next_bot_token(message_count // 20)
            send_telegram(msn, foto, bot_token, chat_id)
            message_count += 1

            logging.info("Product data changed and sent to Telegram")
        else:
            logging.info("Product data unchanged, skipping")

    logging.info("Search completed")
    gc.collect()

def buscador(market, dsct, bot_tokens, chat_id):
    client = MongoClient(mongo)
    db = client[market]
    collection = db["scrap"]

    while True:
        try:
            auto_telegram_between_values(
                "bd1",
                "bd2",
                bot_tokens,
                chat_id,
                dsct,
                100,
                market,
                "scrap"
            )
        except Exception as e:
            logging.error(f"An exception occurred: {e}")

def main(market, dsct, bot_tokens, chat_id):
    try:
        buscador(market, dsct, bot_tokens, chat_id)
    except KeyboardInterrupt:
        logging.info("Program interrupted by user")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")

if __name__ == "__main__":
    main("plazavea", 40, bot_tokens, chat_id)