import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd

# Create an empty list to store the results
results = []

# Initialize the result count
result_count = 1

for page_number in range(1, 101):  # Change the range as per your requirement
    # Create the URL with the updated page number
    # Denver.CO
    # https://www.yellowpages.com/search?search_terms=contractor&geo_location_terms=Denver%2C%20CO&page=

    # Cleveland
    # https://www.yellowpages.com/search?search_terms=contractor&geo_location_terms=Cleveland%2C%20OH&page=

    # Orlando
    # https://www.yellowpages.com/search?search_terms=contractor&geo_location_terms=Orlando%2C%20FL&page=

    # Atlanta
    # https://www.yellowpages.com/search?search_terms=contractor&geo_location_terms=Atlanta%2C%20GA&page=

    # Phoenix
    # https://www.yellowpages.com/search?search_terms=contractor&geo_location_terms=Phoenix%2C%20AZ&page=
    url = f'https://www.yellowpages.com/search?search_terms=contractor&geo_location_terms=Denver%2C%20CO&page={page_number}'

    # Send a GET request to the URL
    response = requests.get(url)

    # Parse the HTML content of the page with BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the container that holds the search results
    results_container = soup.find('div', {'class': 'search-results organic'})

    # Find all individual result elements
    result_elements = results_container.find_all('div', {'class': 'result'})

    # Loop through each result element and click into it to extract the desired information
    for result_element in result_elements:

        # Initialize a dictionary to store the result data
        result_data = {}

        print(f'Result #{result_count}')

        # Extract the link to the individual result page
        result_link = result_element.find('a', {'class': 'business-name'})['href']
        absolute_link = urljoin(url, result_link)

        # Send a GET request to the individual result page
        result_response = requests.get(absolute_link)

        # Parse the HTML content of the individual result page
        result_soup = BeautifulSoup(result_response.text, 'html.parser')

        # Extract the business name
        try:
            name_element = result_soup.find('h1')
            business_name = name_element.text.strip()
        except AttributeError:
            business_name = 'N/A'

        # Extract the phone number
        try:
            phone_element = result_soup.find('a', {'class': 'phone'})
            phone_number = phone_element.find('strong').text.strip()
        except AttributeError:
            phone_number = 'N/A'

        # Extract the email address
        email_element = result_soup.find('a', {'class': 'email-business'})
        email_address = email_element['href'].replace('mailto:', '') if email_element else 'N/A'

        # Extract the services offered
        try:
            services_element = result_soup.find('dd', {'class': 'features-services'})
            services_offered = [span.text for span in services_element.find_all('span')]
        except AttributeError:
            services_offered = 'N/A'

        # Extract the services categories
        try:
            categories_element = result_soup.find('dd', {'class': 'categories'})
            categories = [a.text for a in categories_element.find_all('a')]
        except AttributeError:
            categories = 'N/A'

        # Extract the address
        try:
            address_element = result_soup.find('a', {'class': 'directions'})
            address = address_element.find('span', {'class': 'address'}).text.strip()
        except AttributeError:
            address = 'N/A'

        # Extract the website link
        website_element = result_soup.find('a', {'class': 'website-link'})
        website = website_element['href'] if website_element else 'N/A'

        print(f'Business Name: {business_name}')
        print(f'Services Offered: {services_offered}')
        print(f'Phone Number: {phone_number}')
        print(f'Email Address: {email_address}')
        print(f'Website: {website}')
        print(f'Address: {address}')
        print(f'Category: {categories}')
        print('---')  # Separating each result

        # Store the result data in the dictionary
        result_data['Business Name'] = business_name
        result_data['Services Offered'] = services_offered
        result_data['Phone Number'] = phone_number
        result_data['Email Address'] = email_address
        result_data['Website'] = website
        result_data['Address'] = address
        result_data['Categories'] = categories

        # Append the result data to the list of results
        results.append(result_data)

        # Increment the result count
        result_count += 1

    try:
        # Create a DataFrame from the list of results
        df = pd.DataFrame(results)

        # Export the DataFrame to an Excel file
        filename = f'Constructors_Denver.xlsx'
        df.to_excel(filename, index=False)

        print('Data exported successfully.')

    except Exception as e:
        print(f'Error occurred: {str(e)}')
        print('Exporting collected data...')

        # Raise the exception again to stop the program execution
        raise e
