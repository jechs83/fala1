from selenium import webdriver
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
chrome_driver_path =  "/Users/javier/GIT/fala/buscador/chromedriver"
       
options = Options()
options.add_argument('--headless')
#options.add_argument('--window-size=1920,1080')
try:
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
except:
    driver = webdriver.Chrome(service=Service(chrome_driver_path), options=options)

url = "https://www.vivanda.com.pe/tecnologia/televisores?page=1"

# Use Selenium to load the webpage and fetch the dynamically generated content
driver.get(url)
page_source = driver.page_source
#print(page_source)
driver.quit()

soup = BeautifulSoup(page_source, "html.parser")

tv_listings = soup.select(".product-item-info")

for tv in tv_listings:
    product_name = tv.find("h2", class_="product-name").text
    price = tv.find("span", class_="price").text

    print("Product:", product_name)
    print("Price:", price)
    print("=" * 30)
