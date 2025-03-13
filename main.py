import streamlit as st
from src.preprocess import *
from src.scraping_tools import *
from src.shortage_checking import *

st.head("Shortage Scraper")

st.title("Payroll")
col1, col2, col3, col4 = st.columns([0.15, 0.15, 0.15, 0.55])


#UPLOAD FILES AND PRE-PROCESS THEM

drug_data = st.file_uploader("Upload the payroll register file")

def process_data(payroll, timelock, pay_period):
  ndc_code_list, ndc_count_list = preprocess(drug_data)
  fda_data = scrape_data_from_fda()
  ashp_data = scrape_data_from_ashp()
  
  
  
#-----------------------------------------------------------------------------------------
if drug_data:

  run = st.button("Process files")

  if "processed" not in st.session_state:
    st.session_state.processed = False
    
  if run:
    st.session_state.processed = True
    
    VTC_excel, VTE_excel = process_data(payroll=payroll_register, timelock=timelock, pay_period=pay_period)
    st.session_state.VTC = VTC_excel
    st.session_state.VTE = VTE_excel

  if st.session_state.processed == True:
  
    st.download_button(
        label="Download the VTC_output",
        data=st.session_state.VTC,
        file_name=f"VTC_output_{current_year}_{current_month}_{str(s_day)}_to_{str(e_day)}.csv",
        mime="text/csv",
    )
    
    st.download_button(
        label="Download the VTE_output",
        data=st.session_state.VTE,
        file_name=f"VTE_output_{current_year}_{current_month}_{str(s_day)}_to_{str(e_day)}.csv",
        mime="text/csv",
    )
