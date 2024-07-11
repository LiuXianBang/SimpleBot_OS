import json
import threading
from collections import defaultdict
import time
import os


def convert_dict(d):
    if isinstance(d, defaultdict):
        d = {k: convert_dict(v) for k, v in d.items()}
    return d


def dict_to_defaultdict(d):
    if not isinstance(d, dict):
        return d
    return defaultdict(
        lambda: defaultdict(dict), {k: dict_to_defaultdict(v) for k, v in d.items()}
    )


class ConfigServer:
    def __init__(self, config_path):
        self.config_path = config_path
        self.variables = defaultdict(list)

        if not os.path.isfile(self.config_path):
            self.save(self.config_path)

        self.variables = dict_to_defaultdict(self.load(self.config_path))

        self.is_stop = False
        self.save_period = 0.2
        self.Thread = threading.Thread(target=self.auto_save, daemon=True)
        self.Thread.start()

    def auto_save(self):
        while not self.is_stop:
            time.sleep(self.save_period)
            load_variable = self.load(self.config_path)
            if load_variable != convert_dict(self.variables):
                self.save(self.config_path)

    def load_config(self):
        self.variables = dict_to_defaultdict(self.load(self.config_path))
        return self.variables

    def save(self, filename):
        with open(filename, "w") as f:
            json.dump(convert_dict(self.variables), f)

    def load(self, filename):
        with open(filename, "r") as f:
            try:
                return json.load(f)
            except json.decoder.JSONDecodeError:
                return {}
