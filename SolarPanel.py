from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd

# Create an empty list to store the results
results = []

# Initialize the result count
result_count = 1

# URL for the first page
url = 'https://www.sunhub.com/shop/find/ca_solar-panels?page_no=1'

# Create a new instance of the Chrome driver in headless mode
options = Options()
options.add_argument('--headless')
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")
driver = webdriver.Chrome(options=options)

# Go to the URL
driver.get(url)

# Wait for the products to load
# Wait for the products to load
wait = WebDriverWait(driver, 20)  # Increase the timeout period to 20 seconds
products = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.product.product-list')))


# Get the page source and parse it with BeautifulSoup
soup = BeautifulSoup(driver.page_source, 'html.parser')

# Find the container that holds the search results
results_container = soup.find('div', {'class': 'products mb-3'})

# Find all individual result elements
result_elements = results_container.find_all('div', {'class': 'product product-list'})

# Loop through each result element and extract the desired information
for result_element in result_elements:

    # Initialize a dictionary to store the result data
    result_data = {}

    print(f'Result #{result_count}')

    # Extract the product name
    name_element = result_element.find('h3', {'class': 'product-title'})
    product_name = name_element.text.strip() if name_element else 'N/A'

    # Extract the product price
    price_element = result_element.find('div', {'class': 'product-price'})
    product_price = price_element.text.strip() if price_element else 'N/A'

    print(f'Product Name: {product_name}')
    print(f'Product Price: {product_price}')
    print('---')  # Separating each result

    # Store the result data in the dictionary
    result_data['Product Name'] = product_name
    result_data['Product Price'] = product_price

    # Append the result data to the list of results
    results.append(result_data)

    # Increment the result count
    result_count += 1

# Close the browser window
driver.quit()

try:
    # Create a DataFrame from the list of results
    df = pd.DataFrame(results)

    # Export the DataFrame to an Excel file
    filename = f'SolarPanels_CA.xlsx'
    df.to_excel(filename, index=False)

    print('Data exported successfully.')

except Exception as e:
    print(f'Error occurred: {str(e)}')
    print('Exporting collected data...')

    # Raise the exception again to stop the program execution
    raise e
