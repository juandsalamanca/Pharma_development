import pandas as pd

def preprocess(f):
  colin_df = pd.read_excel("/content/drive/MyDrive/Pharma/skype data 2.0.xlsx", sheet_name="Sheet1")
  ndc_code_list = colin_df["NDC"].to_list()
  return colin_df, ndc_code_list


def get_manufacturer_and_product_codes(text):
  indexes = [i for i, char in enumerate(text) if char == "-"]
  manufacturer_code = text[0: indexes[0]]
  product_code = text[indexes[0]+1:indexes[1]]
  package_code = text[indexes[1]+1:]
  return manufacturer_code, product_code, package_code
