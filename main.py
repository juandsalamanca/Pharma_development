import streamlit as st
import pandas as pd
from src.preprocess import *
from src.scraping_tools import *
from src.shortage_checking import *
from src.google_scraping import *

st.header("Shortage Scrape")

reset = st.button("Reset") 
if reset:
  st.session_state.fda_data_df = None
  st.session_state.processed = False
  st.session_state.final_data

if "fda_data" not in st.session_state:
  st.session_state.fda_data_df = scrape_data_from_fda()
elif st.session_state.fda_data_df == None:
  st.session_state.fda_data_df = scrape_data_from_fda()

def get_shortage_info(ndc_code_list):
  real_ndc_code_list = []
  generic_name_list = []
  brand_name_list = []
  ashp_shortage_list = []
  fda_shortage_list = []
  fda_date_list = []
  ashp_date_list = []
  no_match_codes = []
  error_codes = []
  google_search_uses = 0
  fda_ndc_package_code_shortage_list = st.session_state.fda_data_df["package_ndc_code"].to_list()

  progress_text = "Finding shortage information. Please wait."
  percent_complete = 0
  my_bar = st.progress(percent_complete, text=progress_text)
  delta = 100/len(ndc_code_list)
  for i, ndc_code in enumerate(ndc_code_list):
    try:
      data = fix_ndc_codes(ndc_code)
    except Exception as e:
      data = None
    generic_name = None
    if data:
      # Get correct names and ndc codes
      real_ndc_code, generic_name, brand_name = data
      real_ndc_code_list.append(real_ndc_code)
      brand_name_list.append(brand_name)

      # Check shortages:
      fda_shortage, date_of_update = check_drug_shortage_fda(real_ndc_code, fda_ndc_package_code_shortage_list)
      fda_shortage_list.append(fda_shortage)
      fda_date_list.append(date_of_update)

    # If there's no data matched with the FDA API we use google search
    else:
      no_match_codes.append(ndc_code)
      google_search_uses +=1
      real_ndc_code_list.append(ndc_code)
      brand_name_list.append(None)
      fda_shortage_list.append(None)
      fda_date_list.append(None)

    try:
      ashp_data = get_ashp_info_with_custom_search_engine(ndc_code, 3)
      if ashp_data:
        ashp_shortage, ashp_generic_name, date_of_update = ashp_data
        if ashp_generic_name != None:
          generic_name = ashp_generic_name
        ashp_shortage_list.append(ashp_shortage)
        ashp_date_list.append(date_of_update)
      else:
        ashp_shortage_list.append(None)
        ashp_date_list.append(None)
      time.sleep(1)

    except Exception as e:
      error_codes.append([ndc_code, str(e)])
      ashp_shortage_list.append(None)
      ashp_date_list.append(None)

    generic_name_list.append(generic_name)
    percent_complete += delta
    progress_text = f"Processed {i} samples"
    my_bar.progress(percent_complete + 1, text=progress_text)

  return real_ndc_code_list, generic_name_list, brand_name_list, ashp_shortage_list, fda_shortage_list, fda_date_list, ashp_date_list, error_codes

def process_data(data):
  colin_df, ndc_code_list = preprocess(data)
  shortage_data = get_shortage_info(ndc_code_list)
  real_ndc_code_list, generic_name_list, brand_name_list, ashp_shortage_list, fda_shortage_list, fda_date_list, ashp_date_list, error_codes = shortage_data
  new_data_df = pd.DataFrame({"New_NDC_code":real_ndc_code_list, 
                              "FDA_shortage":fda_shortage_list, 
                              "ASHP-shortage":ashp_shortage_list, 
                              "Generic_name": generic_name_list, 
                              "Brand_name":brand_name_list, 
                              "FDA_Update":fda_date_list, 
                              "ASHP_Update":ashp_date_list})
  final_df = pd.concat((colin_df[["Date", "NDC", "QTY", "Price"]], new_data_df), axis=1)
  shortage_info = final_df.to_csv(index = False).encode("utf-8")
  return shortage_info
  
#-----------------------------------------------------------------------------------------


drug_data = st.file_uploader("Upload your file")

if drug_data:

  run = st.button("Process file")

  if "processed" not in st.session_state:
    st.session_state.processed = False
    
  if run:

    st.session_state.final_data = process_data(drug_data)
    st.session_state.processed = True

  if st.session_state.processed == True:
  
    st.download_button(
        label="Download the output file",
        data=st.session_state.final_data,
        file_name="Updated_shortage_data.csv",
        mime="text/csv",
    )
