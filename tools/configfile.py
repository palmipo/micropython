import json

class ConfigFile:
    def __init__(self, fichier):
        with open(fichier, "r") as fic:
            stream = fic.read()
            self.configFile = json.loads(stream)
            fic.close()

    def config(self):
        return self.configFile
