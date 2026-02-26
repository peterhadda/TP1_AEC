import json

import requests
from config import *

def download_json(url,header):
    r=requests.get(url,headers=header)
    return r.json()


def extract_codes_from_json(codelist_json):
   structure=codelist_json['data'][('structure')]
   codes=[]
   sections=[]

   sections +=structure['dimensions']['series']
   sections += structure['dimensions']['observation']
   sections += structure['attributes']['series']
   sections += structure['attributes']['observation']

   for section in sections:
       for v in section.get("values",[]):
           codes.append({
               "id":v.get('id'),
                "name_en" :v.get("names",{}).get("en")
           })
   return codes

def find_charateristic_code(codelist_json,keyword,lang):
   codes=extract_codes_from_json(codelist_json)

   for code in codes:
       if label == codes["name_en"]:





data=download_json(URL_PROVINCE,HEADER)
print(extract_codes_from_json(data))