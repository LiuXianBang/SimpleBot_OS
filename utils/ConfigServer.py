import json
import threading
from collections import defaultdict

def convert_dict(d):
    if isinstance(d, defaultdict):
        d = {k: convert_dict(v) for k, v in d.items()}
    return d

def dict_to_defaultdict(d):
    if not isinstance(d, dict):
        return d
    return defaultdict(lambda: defaultdict(dict), {k: dict_to_defaultdict(v) for k, v in d.items()})

class ConfigServer:
    def __init__(self):
        self.filename = "config.json"
        self.variables = defaultdict(list)
        self.variables = dict_to_defaultdict(self.load(self.filename))
        self.is_stop = False
        self.Thread = threading.Thread(target=self.auto_save,daemon=True)
        self.Thread.start()
        
        
    def auto_save(self):
        while not self.is_stop:
            load_variable = self.load(self.filename)
            if load_variable != convert_dict(self.variables):
                self.save(self.filename)
            
    #save as json
    def save(self, filename):
        with open(filename, 'w') as f:
            json.dump(convert_dict(self.variables), f)
            
    def load(self, filename):
        with open(filename, 'r') as f:
            try:
                return json.load(f)
            except json.decoder.JSONDecodeError:
                return {}
            
if __name__ == "__main__":
    configServer = ConfigServer()
    configServer.load("config.json")
    