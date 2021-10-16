import json


def getConfig():
    with open('config.json', encoding='utf-8') as f:
        return json.load(f)


def getWords(module = "clock"):
    if (module == "clock"):
        with open('words.json', encoding='utf-8') as f:
            return json.load(f)
    else:
        config = getConfig()
        file_path = config[module]["words_config_path"]
        with open(file_path, encoding='utf-8') as f:
            return json.load(f)

def setConfig(config):
    string = json.dumps(config)
    with open('config.json', 'w') as f:
        f.write(string)
