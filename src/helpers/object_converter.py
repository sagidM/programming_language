import json
from typing import Dict
from src.abstract_tree import Number


class SimpleEncoder(json.JSONEncoder):
    def default(self, obj):
        if type(obj) is Number:
            typ, value = obj.token
            if typ == 'int_value':
                return int(value)
            if typ == 'float_value':
                return float(value)
            return value
        return obj.__dict__ 


def convert_to_dict(obj) -> Dict:
    return json.loads(SimpleEncoder().encode(obj))

def to_pretty_format(obj) -> str:
    return SimpleEncoder(indent=2).encode(obj)
