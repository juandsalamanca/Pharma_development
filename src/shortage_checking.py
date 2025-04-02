from src.scraping_tools import get_product_name_from_fda_api

def check_drug_shortage_fda(ndc):
  shortage = False
  date = None
  if ndc in fda_ndc_package_code_shortage_list:
    idx = fda_ndc_package_code_shortage_list.index(ndc)
    date = essential_df.loc[idx, "date_of_update"]
    if essential_df.loc[idx, "avail_and_esti_short_dur"] == "Unavailable":
      shortage = True

  return shortage, date

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
