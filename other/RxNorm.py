import pandas as pd
import requests
from bs4 import BeautifulSoup
import json
df=pd.read_excel('drug_freq.xlsx')
arr=[]
for index,row in df.iterrows():
    base_url="https://rxnav.nlm.nih.gov/REST/rxclass/class/byDrugName.json?drugName="
    value=requests.get(base_url+row['Drug Name'])
    soup = BeautifulSoup(value.text,'html.parser')
    site_json=json.loads(soup.text)
    json_formatted_str = json.dumps(site_json, indent=4)
    try:
        list1=site_json['rxclassDrugInfoList']["rxclassDrugInfo"]
        for i in range(len(list1)):
            score=0
            if(list1[i]["minConcept"]["name"]==row['Drug Name']):
                arr.append(list1[i]["minConcept"]["rxcui"])
                score=1
                break
            if((i==len(list1)-1)&(score==0)):
                arr.append('No Exact Match')
    except:
        arr.append('No Match')

df['Mapping']=arr
df.to_excel('drug_mapping.xlsx')