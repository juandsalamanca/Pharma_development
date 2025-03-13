import streamlit as st

st.head("Shortage Scraper")

st.title("Payroll")
col1, col2, col3, col4 = st.columns([0.15, 0.15, 0.15, 0.55])


#UPLOAD FILES AND PRE-PROCESS THEM

payroll_register = st.file_uploader("Upload the payroll register file")

timelock = st.file_uploader("Upload the timelock file")


def process_data(payroll, timelock, pay_period):
  payroll, timelock, empl_trio = preprocess_files(payroll=payroll_register, timelock=timelock)
  if old != None:
    del empl_trio[old]
  if new_payroll != None:
    empl_trio[new_payroll] = [new_timelock, new_department]
  # Produce the output files:
  VTC, VTE = produce_payroll_output(payroll=payroll, time_file_path=timelock, empl_trio=empl_trio, pay_period=pay_period)
  VTC_excel = VTC.to_csv(index = False).encode("utf-8")
  VTE_excel = VTE.to_csv(index = False).encode("utf-8")
  return VTC_excel, VTE_excel
  
#-----------------------------------------------------------------------------------------
if payroll_register and timelock:

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
