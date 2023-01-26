
import json
import glob
import os
import pandas as pd
import re
import Save_As_Json
from Save_As_Json import writeToJsonFile

json_path = '/home/ubuntu/PycharmProjects/VIrtual_Machine_Crawler/Json_Files/'
new_json_path = '/home/ubuntu/PycharmProjects/VIrtual_Machine_Crawler/UNI_Json_Files/'
delemata_courts_names = set()
requests_Types = set()
init_cases_names = set()

# Extract files from a folder
def Get_Json_Files(path):
    all_files = []
    for root, dirs, files in os.walk(path):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files:
            all_files.append(os.path.abspath(f))
    return all_files

Json_Files = Get_Json_Files(json_path)
print(json_path)
uni_cases = []
for i, json_file in enumerate(Json_Files):
    last_len = len(delemata_courts_names)
    with open(json_file, encoding = 'utf8') as f:
        data = json.load(f)
        try:
            uni_case = data['מסמכים']["פסק דין או החלטה אחרונה"][0]["מסמך מאוחד"]
        except KeyError: continue
        if(uni_case):
            print(json_file[:-20])
            uni_cases.append(json_file[:-20])
            writeToJsonFile(new_json_path,data['פרטי תיק']['שם הקובץ'],data)
df = pd.DataFrame({"שם":list(uni_cases)})

df.to_csv("uni_cases_list.csv")