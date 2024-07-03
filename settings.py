import yaml
import os

def parent(path):
    return os.path.abspath(os.path.join(path, os.pardir))

BASE_DIR = parent(__file__)

CONFIG_PATH = BASE_DIR + '\\config.yaml'

with open(CONFIG_PATH) as f:
    config = yaml.safe_load(f)
