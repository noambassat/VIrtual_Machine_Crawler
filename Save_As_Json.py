import json
from io import StringIO

def writeToJsonFile(filePath, fileName, data):
    filePathName = filePath  + fileName + '.json'

    with open(filePathName, 'w', encoding='utf8') as json_file:
       json.dump(data, json_file, ensure_ascii=False)



