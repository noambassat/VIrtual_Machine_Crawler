from bs4 import Tag
import json
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

#!/usr/bin/env python3 # -*- coding: utf-8 -*-

class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        if type(obj) == Tag:
            return json.JSONEncoder.default(self, obj.text)
        return json.JSONEncoder.default(self, obj)


def writeToJsonFile(filePath, fileName, data):
    ### drive ####





    filePathName = filePath + str(fileName) + '.json'
    with open(filePathName, 'w', encoding='utf8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, cls=SetEncoder)
    print(fileName)
    return fileName


