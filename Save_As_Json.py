import json

def writeToJsonFile(fileName, data):
    filePathName =  'C:/Users/Noam/PycharmProjects/pythonProject5/Json_Files/' + fileName + '.json'
    with open(filePathName, 'w') as fp:
        json.dump(data, fp)


