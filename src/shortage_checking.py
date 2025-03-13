from src.scraping_tools import get_product_name_from_fda_api

def check_drug_shortage_fda(ndc, essential_df):
  ndc_list = essential_df["package_ndc_code"].to_list()
  if ndc in ndc_list:
    idx = ndc_list.index(ndc)
    if essential_df.loc[idx, "avail_and_esti_short_dur"] == "Unavailable":
      return True
  return False

def check_drug_shortage_ashp(ndcm, df):

  shortage = False
  names = get_product_name_from_fda_api(ndc)
  if names:
    brand_name, generic_name = names
    for name in df["Generic Name"]:
      if brand_name and brand_name in name :
        shortage = True
      if generic_name and generic_name in name:
        shortage = True
  return shortage
