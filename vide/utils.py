import os

def load_config(cls):
    filename = "/".join(os.path.abspath(__file__).split("/")[:-1]) + "/default.cfg"
    with open(filename, 'r') as handle:
        for line in handle.read().split('\n'):
            if line:
                key, value = line.split('=')
                setattr(cls, key, value)
