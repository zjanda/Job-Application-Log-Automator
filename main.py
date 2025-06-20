import json
import warnings
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials


def get_state(city):
    if city == 'Remote':
        return ''
    
    return { # TODO: add more cities as needed
        'Irvine': 'CA',
        'San Jose': 'CA',
        'Sunnyvale': 'CA',
        'Hawthorne': 'CA',
        'Santa Ana': 'CA',
        'San Diego': 'CA',
        'Costa Mesa': 'CA',
        'Culver City': 'CA',
        'Lake Forest': 'CA',
        'Los Angeles': 'CA',
        'Laguna Hills': 'CA',
        'Santa Monica': 'CA',
        'San Francisco': 'CA',
        'Newport Beach': 'CA',
        'San Francisco Bay Area': 'CA',
        'Seattle': 'WA',
        'Houston': 'TX',
        'Austin': 'TX',
        'New York': 'NY',
        'Manhattan': 'NY',
        'Boston': 'MA',
        'Denver': 'CO'
    }[city]

        
def throw_error(message):
    raise ValueError(message)

def convert_to_sheet_line(job_details):
    return [ 
        job_details['company_name'],
        job_details['position'],
        job_details['role'],
        job_details['date'],
        job_details['city'],
        job_details['state'],
        job_details['country'],
        job_details['position_type'],
        job_details['location_type'],
        job_details['gov'],
        job_details['salary'],
        job_details['fav'],
        job_details['start_date'],
        job_details['response']
    ]

def scrape_job_listing(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')

        job_title, company_name = soup.find(attrs={'data-testid': 'job-title'}).get_text().split(', ') if soup.find(attrs={'data-testid': 'job-title'}) else ('Unknown Position', 'Unknown Company')
        location_tag = soup.find(attrs={'data-testid': 'job-location-tag'}).get_text() if soup.find(attrs={'data-testid': 'job-location-tag'}) else 'Remote'
        if location_tag.startswith('Remote'):
            parts = location_tag.split(' ')
            city = 'Remote'
            state = ''
            country = parts[-1]
            country = 'USA' if country == 'US' else country
        else:
            city = location_tag
            state = get_state(city)
            country = 'USA' if state else input(f"Enter the country for the city {city}: ")

        today = datetime.now()
        date_formatted = f"{today.month}/{today.day}/{today.year}"
        job_details = {
            'company_name': company_name,
            'position': job_title,
            'role': 'Job',
            'date': date_formatted,
            'city': city,
            'state': state,
            'country': country,
            'position_type': 'Full-Time',
            'location_type': 'Remote' if soup.find(text=re.compile(r'\bremote\b', re.IGNORECASE)) else 
                             'Hybrid' if soup.find(text=re.compile(r'\bhybrid\b', re.IGNORECASE)) else 
                             'On-site',
            'gov': 'No',
            'salary': re.search(r'\$\d+(\.\d+)?-\d+k', soup.get_text()).group() if re.search(r'\$\d+(\.\d+)?-\d+k', soup.get_text()) else '',
            'fav': '',
            'start_date': soup.find('meta', property='job:start_date')['content'] if soup.find('meta', property='job:start_date') else '',
            'response': '?'
        }

        return job_details
    except requests.RequestException as e:
        print('Error fetching the job listing:', e)

def send_to_sheet(job_details, sheet_name, worksheet_name):
    creds = Credentials.from_service_account_file('google-sheet-api.json', scopes=[
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
    ])
    gc = gspread.authorize(creds)

    sheet = gc.open(sheet_name).worksheet(worksheet_name)

    row = convert_to_sheet_line(job_details)

    # Append to the sheet
    col_values = sheet.col_values(6)  # Get all values from column F
    first_empty_row = len(col_values) + 1  # Find the first empty row
    
    # sheet.insert_row(row, first_empty_row)  # Insert the row at the first empty row
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        sheet.update(f'F{first_empty_row}:S{first_empty_row}', [row])
        
    print(f"Added {job_details['company_name']} to {sheet_name} > {worksheet_name} at row {first_empty_row}.")

while True:
    try:
        sheet_info = json.load(open('sheet-info.json'))
        sheet_name = sheet_info['sheet_name']
        worksheet_name = sheet_info['worksheet_name']
        URL = input('Enter the URL of the job listing or press O for options or X to exit: ')
        if URL == 'O' or URL == 'o':
            print('Options:')
            print('1. Change sheet name')
            print('2. Change worksheet name')
            print('3. Go back to the main menu')
            print('4. Exit')
            option = input('Enter the number of the option you want to choose: ')
            if option == '1':
                sheet_name = input('Current sheet name: ' + sheet_name + '\nEnter the new sheet name: ')
            elif option == '2':
                worksheet_name = input('Current worksheet name: ' + worksheet_name + '\nEnter the new worksheet name: ')
            elif option == '3':
                continue
            elif option == '4' or option == 'X' or option == 'x':
                print('Exiting...')
                exit()
            else:
                print('Invalid option')
        elif URL == 'X' or URL == 'x':
            print('Exiting...')
            exit()
        else:
            print('Scraping job listing...')
            job_details = scrape_job_listing(URL)
            print('Sending to sheet...')
            send_to_sheet(job_details, sheet_name, worksheet_name)
    except Exception as e:
        print(f"Error: {e}")
        break


