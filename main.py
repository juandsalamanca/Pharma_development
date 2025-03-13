import streamlit as st
import pandas as pd
from src.preprocess import *
from src.scraping_tools import *
from src.shortage_checking import *

st.head("Shortage Scraper")

if "fda_data" not in st.session_state:
  st.session_state.fda_data = scrape_data_from_fda()

if "ashp_data" not in st.session_state:
  st.session_state.ashp_data = scrape_data_from_ashp()

def process_data(data):
  ndc_code_list, ndc_count_list = preprocess(data)
  fda_shortage_list = []
  ashp_shortage_list = []
  for ndc_code in ndc_code_list:
    fda_shortage = check_drug_shortage_fda(ndc_code, st.session_state.fda_data)
    fda_shortage_list.append(fda_shortage)
    ashp_shortage = check_drug_shortage_ashp(ndc_code, st.session_state.ashp_data)
    ashp_shortage_list.append(ashp_shortage)
    
  updated_data = {"NDC_code": ndc_code_list, "NDC_count": ndc_count_list, "FDA_shortage": fda_shortage_list, "ASHP_shortage": ashp_shortage_list}
  final_data = pd.DataFrame(updated_data)
  return final_data


#-----------------------------------------------------------------------------------------
if drug_data:

  run = st.button("Process file")

  if "processed" not in st.session_state:
    st.session_state.processed = False
    
  if run:
    st.session_state.processed = True
    
    final_data = process_data(drug_data)
    st.session_state.final_data = final_data

  if st.session_state.processed == True:
  
    st.download_button(
        label="Download the VTC_output",
        data=st.session_state.final_data,
        file_name="Updated_shortage_data.csv",
        mime="text/csv",
    )
