import json

class Config:
    def __init__(self):
        f = open ('config.json', "r") 
        data = json.loads(f.read())
        f.close()

        for key, value in data.items():
            setattr(self, key, value)

conf = Config()