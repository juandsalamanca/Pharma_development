from datetime import datetime
from dateutil import parser

def format_date(date_string):
    try:
        # Parse the date string using dateutil's parser, which can handle multiple formats
        parsed_date = parser.parse(date_string)
        # Return the date in the desired format YYYY-MM-DD
        return parsed_date.strftime('%Y-%m-%d')
    except ValueError:
        return ""

def get_most_recent_date_index(date_list):
    try:
        # Convert strings to datetime objects
        date_objects = [datetime.strptime(date, '%Y-%m-%d') for date in date_list]
        # Find the index of the most recent date
        most_recent_index = date_objects.index(max(date_objects))
        return most_recent_index
    except ValueError as e:
        return f"Error: {e}"

def find_all_indexes(text, substring):
    indexes = []
    start = 0
    while start < len(text):
        # Find the next occurrence of the substring
        start = text.find(substring, start)
        if start == -1:
            break  # Exit if no more occurrences are found
        indexes.append(start)
        start += 1  # Move to the next character to continue searching
    return indexes

def get_ashp_urls(ndc):
    """
    Uses Google Custom Search API to find the URL with info from the NDC.
    """
    subquery = "NDC "+ ndc + " ASHP"
    query = f"{subquery} site:https://www.ashp.org/drug-shortages/current-shortages"
    url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={API_KEY}&cx={CX}"

    try:
        response = requests.get(url)
        data = response.json()

        # Extract the first 3 result URLs
        url_list = []
        if "items" in data:
            for item in data["items"]:
                url_list.append(item["link"])
            return url_list
        else:
            #print("[-] No results found")
            return None

    except Exception as e:
        print(f"[-] Error fetching LinkedIn URL: {e}")
        return None

def get_ashp_info_with_custom_search_engine(ndc, num_results):
  shortage = None
  name = None
  recent_date = None
  websites = []
  # Perform the Google search
  target_urls = get_ashp_urls(ndc)
  if target_urls:
    date_list = []
    text_list = []

    for url in target_urls:
      response = requests.get(url)
      date = response.headers["Date"]
      text_list.append(response.text)
      formatted_date = format_date(date)
      date_list.append(formatted_date)
    most_recent_date_idx = get_most_recent_date_index(date_list)
    text = text_list[most_recent_date_idx]
    ndc_indexes = find_all_indexes(text, ndc)
    # If we find the NDC code in the most recent ashp link we check it's shortage status
    if ndc_indexes:
      #print("Found NDC!")
      recent_date = date_list[most_recent_date_idx]
      ndc_idx = None
      # If we find it in the products affected section, it's in shortage
      if "<!-- Begin Products Affected -->" in text:
        begin_affected_idx = text.index("<!-- Begin Products Affected -->")
        end_affected_idx = text.index("<!-- End Products Affected  -->")
        for ndc_index in ndc_indexes:
          if begin_affected_idx < ndc_index <  end_affected_idx:
            #print("ndc found in products affected")
            ndc_idx = ndc_index
            shortage = True
            break
      # If we find it in the available producs section, it's not in shortage
      if "<!-- Begin Available Products -->" in text:
        begin_available_idx = text.index("<!-- Begin Available Products -->")
        end_available_idx = text.index("<!-- End Available Products -->")
        for ndc_index in ndc_indexes:
          if begin_available_idx < ndc_index <  end_available_idx:
            #print("ndc found in available products")
            ndc_idx = ndc_index
            shortage = False
            break

      if ndc_idx:
        start_idx = None
        end_idx = None
        #print(text[ndc_idx-100: ndc_idx+10])
        # Now lets find the generic name of the drug.
        # In each section they have a line of text for each drug, containing name at the beginning and NDC code at the end
        for i in range(0,1000,4):

          start_window = text[ndc_idx-i: ndc_idx-i+10]
          if "<li>" in start_window:
            if start_idx == None:
              start_idx = ndc_idx -i + start_window.index("<li>")

          end_window = text[ndc_idx+i: ndc_idx+i+10]
          if "<li>" in end_window:
            if end_idx == None:
              end_idx = ndc_idx +i + end_window.index("<li>")
          if start_idx and end_idx:
            relevant_text = text[start_idx:end_idx]
            name_start = None
            name_end = None
            for i, ch in enumerate(relevant_text):
              if ch == ">" and not name_start:
                name_start = i+1
              if ch == "," and not name_end:
                name_end = i
            if name_start and name_end:
              name = relevant_text[name_start:name_end]
            break

      return shortage, name, recent_date

  else:

    return None
