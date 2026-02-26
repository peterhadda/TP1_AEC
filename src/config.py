from pathlib import Path

BASE_DIR=Path(__file__).resolve().parent.parent
RAW_PATH=BASE_DIR /"data"/"raw"


KEY_PROVINCE = "A5..1.350.1"
URL_PROVINCE= f"https://api.statcan.gc.ca/census-recensement/profile/sdmx/rest/data/STC_CP,DF_PR/{KEY_PROVINCE}"
HEADER = {"Accept": "application/vnd.sdmx.data+json;version=1.0.0-wd"}
CL_CHARACTERISTIC=350