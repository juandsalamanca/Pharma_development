import pandas as pd

def preprocess(f):
  df = pd.read_excel(f)
  ndc_code_list = df.iloc[3:,0].to_list()
  return ndc_code_list
