import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()


chrome_options.add_argument('--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1')
driver = webdriver.Chrome(options=chrome_options)
driver.get('http://interbankcupones.pe/rappi')
time.sleep(30)