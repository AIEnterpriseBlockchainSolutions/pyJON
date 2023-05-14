import os
from errors import JONSyntaxError, JONTypeAlreadyExists
from deserialize import Object, deserialize_data

def load_file(path: str) -> list[Object]:
    if not os.path.exists(path):
        raise FileNotFoundError()
    with open(path, "r") as f:
        return deserialize_data(f.read())