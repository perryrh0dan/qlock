import json


def getConfig():
    with open('config.json', encoding='utf-8') as f:
        return json.load(f)


def getWords():
    with open('words.json', encoding='utf-8') as f:
        return json.load(f)


def setConfig(config):
    string = json.dumps(config)
    with open('config.json', 'w') as f:
        f.write(string)
