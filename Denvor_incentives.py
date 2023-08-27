import time
import csv
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd

# List of zip codes to iterate over
zip_codes = [
    80010, 80011, 80012, 80013, 80014, 80015, 80016, 80017, 80018, 80019, 80020, 80020, 
    80021, 80022, 80026, 80027, 80030, 80031, 80033, 80107, 80108, 80109, 80110, 80111, 
    80112, 80113, 80116, 80123, 80120, 80121, 80122, 80123, 80124, 80125, 80126, 80127, 
    80128, 80129, 80130, 80134, 80135, 80137, 80138, 80215, 80222, 80228, 80234, 80240, 
    80202, 80203, 80204, 80205, 80206, 80207, 80209, 80210, 80211, 80212, 80214, 80215, 
    80216, 80218, 80219, 80220, 80221, 80222, 80223, 80224, 80225, 80226, 80227, 80228, 
    80229, 80230, 80231, 80232, 80233, 80235, 80236, 80237, 80238, 80239, 80241, 80246, 
    80247, 80249, 80260, 80301, 80302, 80303, 80304, 80305, 80401, 80403, 80465, 80501, 
    80503, 80601, 80602, 80603, 80614, 80640
]

# Set up the Chrome WebDriver (you can use other WebDriver options if desired)
driver = webdriver.Chrome()

# Iterate over each zip code
for zip_code in zip_codes:
    print(f"Processing data for zip code: {zip_code}")

    # Step 1: Visit the initial page with the list of programs
    url = f"https://programs.dsireusa.org/system/program?zipcode={zip_code}"
    driver.get(url)

    # Wait for the dynamic content to load (you might need to adjust the wait time depending on the page)
    time.sleep(3)

    # Get the page source after the dynamic content has loaded
    page_source = driver.page_source

    # Step 2: Parse the page source with BeautifulSoup to get the links to individual program pages
    soup = BeautifulSoup(page_source, "html.parser")

    # Find the table containing the data
    table = soup.find("table")

    if table:
        # Find all rows in the table except the header row
        rows = table.find_all("tr")[1:]

        # Initialize an empty list to store the structured data
        structured_data = []

        # Extract data from each row
        for row in rows:
            cells = row.find_all(["th", "td"])
            link = cells[0].find("a")["href"]  # Get the link to the program page
            program_name = cells[0].text.strip()

            # Step 3: Visit the individual program page
            program_url = f"https://programs.dsireusa.org{link}"
            driver.get(program_url)

            # Wait for the dynamic content to load (you might need to adjust the wait time depending on the page)
            time.sleep(2)

            # Get the page source after the dynamic content has loaded
            program_page_source = driver.page_source

            # Step 4: Parse the program page to extract the data from the "program-detail wrapper" division
            program_soup = BeautifulSoup(program_page_source, "html.parser")
            program_detail_div = program_soup.find("div", {"class": "programOverview"})

            if program_detail_div:
                # Find all points in the "program-detail wrapper" division
                points = program_detail_div.find_all("li")

                # Create a dictionary to store the details of the current program
                program_details = {
                    "Program Name": program_name
                }

                # Extract and store the details in the dictionary
                for point in points:
                    parts = point.get_text(strip=True).split(":", 1)
                    if len(parts) == 2:
                        key, value = parts
                        program_details[key.strip()] = value.strip()

                # Append the dictionary to the structured_data list
                structured_data.append(program_details)
            else:
                print(f"No 'program-detail wrapper' division found on the program page for '{program_name}'.")

        # CSV file path to save the data C:\Users\a_704\Desktop\Denvor incentive data
        csv_file_path = f"/Users/a_704/Desktop/Denvor incentive data/CO_Denver_incentive_details_{zip_code}.csv"

        # Use pandas to normalize (flatten) the nested dictionaries
        flattened_data = pd.json_normalize(structured_data)

        # Write the flattened data to a CSV file
        flattened_data.to_csv(csv_file_path, index=False, encoding="utf-8")

        print(f"CSV file for zip code {zip_code} has been created successfully.")
    else:
        print(f"No table found on the initial page for zip code {zip_code}.")

# Close the browser
driver.quit()