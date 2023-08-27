import requests
from bs4 import BeautifulSoup

# Send a GET request to the URL
url = 'https://www.yellowpages.com/denver-co/mip/republic-garages-888520?lid=1002108131447'
response = requests.get(url)

# Parse the HTML content of the page with BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Find the specific element that contains the business name
# The tag and class of the element will depend on the structure of the webpage
# Based on the content extracted, it seems like the business name might be in a 'h1' tag
name_element = soup.find('h1')

# Extract the business name from the element
business_name = name_element.text.strip()

# Find the specific element that contains the email address
email_element = soup.find('a', {'class': 'email-business'})

# Extract the email address from the element
email_address = email_element['href'].replace('mailto:', '')

# Find the specific element that contains the services offered
services_element = soup.find('div', {'class': 'categories'})

# Extract the services from the element
services_offered = [a.text for a in services_element.find_all('a')]

# Find the specific element that contains the website link
website_element = soup.find('a', {'class': 'website-link'})

# Extract the website link
website = website_element['href']

# Find the specific element that contains the address
address_element = soup.find('a', {'class': 'directions'})

# Extract the address from the element
address = address_element.find('span', {'class': 'address'}).text.strip()

print(f'Business Name: {business_name}')
print(f'Email Address: {email_address}')
print(f'Services Offered: {services_offered}')
print(f'Address: {address}')
