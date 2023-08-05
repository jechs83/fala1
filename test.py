import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def render_dynamic_data(urls):
    # Configure Chrome WebDriver with headless option
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920x1080')

    # Path to your Chrome WebDriver executable
    # Download the appropriate version from https://sites.google.com/a/chromium.org/chromedriver/downloads
    driver_path = '/path/to/chromedriver'

    # Create a new Chrome browser instance
    driver = webdriver.Chrome(executable_path=driver_path, options=options)

    for url in urls:
        try:
            # Navigate to the URL
            driver.get(url)

            # Wait for the page to load its dynamic content (adjust the wait time if needed)
            time.sleep(5)

            # Get the dynamic data from the page (use appropriate locators)
            dynamic_data = driver.find_element_by_css_selector('#dynamic-element').text

            # Process or save the dynamic data as needed
            print(f"Data from {url}: {dynamic_data}")

        except Exception as e:
            print(f"Error processing {url}: {e}")

    # Close the browser
    driver.quit()

if __name__ == "__main__":
    # List of URLs with dynamic data
    urls_with_dynamic_data = [
        'https://shopstar.pe/tecnologia/televisores?order=OrderByReleaseDateDESC&page=2',
        # 'https://example.com/page2',
        # Add more URLs as needed
    ]

    render_dynamic_data(urls_with_dynamic_data)

