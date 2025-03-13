from src.preprocess import get_manufacturer_and_product_codes

def get_product_name(ndc):
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
