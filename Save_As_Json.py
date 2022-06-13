import json
from io import StringIO

def writeToJsonFile(filePath, fileName, data):
    print("#########################")
    filePathName = filePath  + fileName + '.json'
    with open(filePathName, 'w') as fp:
        json.dump(data, fp)



