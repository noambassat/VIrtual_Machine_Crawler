
import json
import glob
import os
import pandas as pd
import re

json_path = '/home/ubuntu/PycharmProjects/VIrtual_Machine_Crawler/Json_Files/'

init_cases_names = []
case_len = []

# Extract files from a folder
def Get_Json_Files(path):
    all_files = []
    for root, dirs, files in os.walk(path):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files:
            all_files.append(os.path.abspath(f))
    return all_files

Json_Files = Get_Json_Files(json_path)


years = []
madors = []
statuses = []
judges = []
df = pd.DataFrame(columns=["שנה","מדור","סטטוס תיק","תחילית"])
for i, json_file in enumerate(Json_Files):
    with open(json_file, encoding = 'utf8') as f:
        data = json.load(f)

        year = mador = status = judge = 'unknown'
        new_row = {"שנה":'',"מדור":'',"סטטוס תיק":'',"תחילית ממספר התיק":''}
        for field in ['מדור','סטטוס תיק']:
            try: # מדור
                value = data["פרטי תיק"]["פרטים כלליים"][field]
                new_row[field] = value

            except KeyError:
                pass

        try:
            year = data["פרטי תיק"]["שנת תיק"]
            if(int(year)>2022): year ='19'+str(year)[:-2]
            new_row["שנה"] = year
        except KeyError:
            pass
        try:
            init = data["פרטי תיק"]["ראשי תיבות תיק"]
            new_row["תחילית ממספר התיק"] = init
        except KeyError:
            pass
        print(new_row)
        df.append(new_row,ignore_index=True)


print(df)
df.to_csv('statistics.csv')
