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

def fix_ndc_codes(ndc):
  codes = get_manufacturer_and_product_codes(ndc)
  name = get_product_name(ndc)
  time.sleep(2)
  if name:
    ndc_code = ndc
    brand_name, generic_name = name
    return ndc_code, generic_name, brand_name
  for i, code in enumerate(codes):
    if code[0] == "0":
      new_code = code[1:]
      if i == 0:
        ndc_code = new_code +"-"+codes[1]+"-"+codes[2]
      elif i == 1:
        ndc_code = codes[0] +"-"+new_code+"-"+codes[2]
      else:
        ndc_code = codes[0] +"-" + codes[1] +"-" + new_code
      name = get_product_name(ndc_code)
      time.sleep(2)
      if name:
        generic_name, brand_name = name
        return ndc_code, generic_name, brand_name
