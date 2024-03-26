import requests
from bs4 import BeautifulSoup
from airtable import airtable

# Define the alphabet
ALPHABET = [
    "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
    "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"
]

API_KEY = "patFEYflWzNojudah.dff9465313d999052bd89bc7a58418f603d06b39af88a2e1131768da260e0bfc"
BASE_ID = "appfguAlGNew4NsxC"

at = airtable.Airtable(BASE_ID, API_KEY)

def get_user_content(path):
    url = f"https://vetmed.iastate.edu{path}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Initialize variables with default values
    professional_title = ""
    degrees = ""

    # Attempt to find elements and extract text content
    professional_title_element = soup.select_one('.field-name-field-professional-title .field-item')
    if professional_title_element:
        professional_title = professional_title_element.get_text().strip()

    degrees_element = soup.select_one('.field-name-field-degrees .field-item')
    if degrees_element:
        degrees = degrees_element.get_text().strip()

    return professional_title, degrees

def scrape_directory_page(letter):
    url = f"https://vetmed.iastate.edu/directory/{letter}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    tbody = soup.find('tbody')

    if tbody:
        for row in tbody.find_all('tr'):
            last_name_cell = row.find(class_='views-field-field-c-last-name')
            last_name = last_name_cell.get_text().strip()
            anchor = last_name_cell.find('a')
            href = anchor.get('href') if anchor else ''
            first_name = row.find(class_='views-field-field-c-first-name').get_text().strip()
            department = row.find(class_='views-field-field-department').get_text().strip()
            phone_number = row.find(class_='views-field-field-c-phone').get_text().strip()
            email = row.find(class_='views-field-field-c-email').get_text().strip()
            professional_title, degrees = get_user_content(href)

            at.create('Directory', {
                'Last Name': last_name,
                'First Name': first_name,
                'Department': department,
                'Phone': phone_number,
                'Email': email,
                'Profile Link': f"https://vetmed.iastate.edu{href}",
                'Professional Title': professional_title,
                'Degrees': degrees,
            })
    else:
        print("No tbody found on the page.")

def run():
    print("ISU Vet School Scraper Starting...")

    for letter in ALPHABET:
        print(f"Scraping directory page for letter: {letter}")
        scrape_directory_page(letter)

run()
