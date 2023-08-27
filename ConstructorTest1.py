from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Chrome()  # or use webdriver.Chrome() if you prefer

results = []

for i in range(1, 101):  # Loop through pages 1 to 100
    driver.get(f"https://www.yellowpages.com/search?search_terms=contractor&geo_location_terms=Denver%2C%20CO&page={i}")

    elements = driver.find_elements_by_xpath('//*[@id="main-content"]/div[2]/div[1]/*')

    for element in elements:
        name = element.find_element_by_css_selector('.business-name span').text
        phone = element.find_element_by_css_selector('.phone.primary').text
        categories = 'N/A'
        category_elements = element.find_elements_by_css_selector('.categories a')
        if category_elements:
            categories = ', '.join([category.text for category in category_elements])

        results.append({
            'name': name,
            'phone': phone,
            'categories': categories
        })

    time.sleep(1)  # Sleep for a while to avoid making too many requests in a short period of time

driver.quit()

# Now 'results' contains the scraped data
for result in results:
    print(result)
