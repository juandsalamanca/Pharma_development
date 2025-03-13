import pandas as pd

def preprocess(f):
  df = pd.read_excel(f)
  ndc_code_list = df.iloc[3:,0].to_list()
  return ndc_code_list

def get_manufacturer_and_product_codes(text):
  indexes = [i for i, char in enumerate(text) if char == "-"]
  manufacturer_code = text[0: indexes[0]]
  product_code = text[indexes[0]+1:indexes[1]]
  return manufacturer_code, product_code
