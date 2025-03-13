import requests
from bs4 import BeautifulSoup
import pandas as pd
from src.preprocess import get_manufacturer_and_product_codes

def get_product_name_from_fda_api(ndc):
  FOO, BAR = get_manufacturer_and_product_codes(ndc)
  endpoint = f'https://api.fda.gov/drug/ndc.json?search=product_ndc:"{FOO}-{BAR}"'
  response = requests.get(endpoint)
  if response.status_code == 200:
    data = response.json()
    if "results" in data:
        for result in data["results"]:
            brand_name = result.get('brand_name')
            generic_name = result.get('generic_name')

        return brand_name, generic_name

    else:
        print("No results found for the given NDC code.")
  else:
      print(f"Failed to fetch data: {response.status_code} - {response.text}")

def scrape_data_from_ashp():
  
  # URL of the page with the table
  url = "https://www.ashp.org/drug-shortages/current-shortages/drug-shortages-list?page=CurrentShortages"
  
  # Fetch the page content
  response = requests.get(url)
  soup = BeautifulSoup(response.content, 'html.parser')
  
  # Find the table (you might need to specify the class or id if there are multiple tables)
  table = soup.find('table')  # or soup.find('table', {'class': 'your-class-name'})
  
  # Extract headers
  headers = [header.text.strip() for header in table.find_all('th')]
  
  # Extract rows
  rows = []
  for row in table.find_all('tr'):
    cells = row.find_all(['td', 'th'])  # 'th' is included in case there are headers in rows
    rows.append([cell.text.strip() for cell in cells])
  
  # Convert to DataFrame
  df = pd.DataFrame(rows[1:], columns=rows[0])  # Assuming first row is the header

  return df

def scrape_data_from_fda():

  # === 1. Initiate the session for the scraping ===

  main_page_url = "https://dps.fda.gov/drugshortages"
  
  session = requests.Session()
  session.get(main_page_url)
  
  # === 2. Retrieve the Token ===
  
  # In order to download the data we'll need to post a request with a token in the payload.
  # We get that token by posting the following request
  token_url = "https://dps-admin.fda.gov/drugshortages/oauth/token"
  token_payload = {
      "grant_type": "client_credentials",
      "client_id": "-c9QHYzXZP-r-2Sr93I1lxvi8gpjjT2-eu60p4_6ik8",
      "client_secret": "62dbaabd987139e84ff1ad6beb1b7945"
  }
  
  token_headers = {
      "Accept": "*/*",
      "Content-Type": "application/x-www-form-urlencoded",
      "Origin": "https://dps.fda.gov",
      "Referer": "https://dps.fda.gov/drugshortages",
      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
      "Cache-Control": "no-cache",
      "Pragma": "no-cache",
      "Sec-Fetch-Dest": "empty",
      "Sec-Fetch-Mode": "cors",
      "Sec-Fetch-Site": "same-site",
      "Sec-Ch-Ua": '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
      "Sec-Ch-Ua-Platform": '"Windows"',
      "Sec-Ch-Ua-Mobile": "?0"
  }
  
  token_response = session.post(token_url, headers=token_headers, data=token_payload)
  if token_response.status_code == 200:
      token = token_response.json().get("access_token")
      print("Token retrieved successfully:", token)
  else:
      print("Failed to retrieve token:", token_response.text)
      exit()

  # === 3. Retrieve the Data ===

  # Now we can use the token to get the shortage data from the backend API that the FDA website calls
  headers = {
      "accept": "*/*",
      "accept-language": "es-ES,es;q=0.9",
      "cache-control": "no-cache",
      "content-type": "application/x-www-form-urlencoded",
      "origin": "https://dps.fda.gov",
      "pragma": "no-cache",
      "referer": "https://dps.fda.gov/drugshortages",
      "sec-ch-ua": '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
      "sec-ch-ua-mobile": "?0",
      "sec-ch-ua-platform": '"Windows"',
      "sec-fetch-dest": "empty",
      "sec-fetch-mode": "cors",
      "sec-fetch-site": "same-origin",
      "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
  }

  # The following cookie was gotten looking at the posted request by the FDA webpage using Chrome DevTools
  # Unlike the token, the cookie doesn't expire so no need to get it dynamically
  
  cookies = {
      "_ga": "GA1.1.1657651770.1741641438",
      "_abck": "E6ED3D122E0784696162C5BFEBC79B99~0~YAAQCJYqF6raooWVAQAAKtuBhw1mzxdr3mwom1fG8lt1KJeo9miaM3/sdxg9rB2UIctHwSEm8VN4mgbK2tDXUzZXNl5i1hEA0Gsh16/5JE/6NV4tmZLh62eMgfDrpJuIA8b6rsNgn/RKjCyxKEhf2Iz5vnXoXsJlCroow89UXiniZcrWQ7osKN1rM6sQxWHlUvY4Kp0S69E70FOmIUHlC1a6bMlzagOV+5Ik27dlHlX4JeSdFPRE6cRuhrfD4+wptKvB3XOV3cxSrNkPPHOcsnIbt2czMsd9VESW4e3mnY/R6upsiXckfwLorHFxIZzYEyoKPr+oN0iWvBS459zC/ygV0iCZGXEmf6BSt4GG3WtDCnK7FI+kQEyQa0qZ3ms8BDLw0TkftvEWcUa3xojZiCMZb6br3s2bRcZ7dmbDQ4ZE1yPRLJ4iGE02qM78SgNXtLM1KJiVAizfjvI0AJtNRixpanVriLsR05Z3z1oX5m507ufCzPi/2A==~-1~-1~-1",
  }
  
  data = {
      "pageEndpoint": "https://dps-admin.fda.gov/drugshortages/api/products?download=dshors",
      "token": token,
  }
  
  download_url = "https://dps.fda.gov/api/data"
  response = requests.post(download_url, headers=headers, cookies=cookies, json=data)
  df = pd.json_normalize(response.json()["data"])
  essential_df = df[["avail_and_esti_short_dur", "package_ndc_code"]]

  return essential_df
