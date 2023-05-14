import re
from typing import Any

class Type:
    def __init__(self, name: str, fields: dict[str, Any]):
        self.name = name
        self.fields = fields

class Object:
    def __init__(self, obj_type: Type, values: list):
        self.obj_type = obj_type
        self.values = values

def create_type_configs(lines: list[str]) -> dict[str, Type]:
    type_configs = {}
    for i, line in enumerate(lines):
        match = re.match(r'\|(\w+)\|', line)
        if match:
            name = match.group(1)
            fields_line = lines[i+1]
            field_types_line = lines[i+2]
            fields = dict(zip(re.findall(r'\"(.*?)\"', fields_line), 
                              re.findall(r'(\w+)', field_types_line)[1:]))
            type_configs[name] = Type(name, fields)
    return type_configs

def convert_value(value_str: str, value_type: str) -> Any:
    print(value_str)
    if value_type == "int":
        return int(value_str)
    elif value_type == "string":
        return value_str.strip('"')
    elif value_type == "bool":
        return value_str.lower() == 'true'
    else:
        raise ValueError(f"Unknown value type: {value_type}")

def create_object(obj_str: str, type_configs: dict[str, Type]) -> Object:
    # Extract object type and values
    obj_type_name, obj_values_str = obj_str.split(':', 1)
    obj_type = type_configs[obj_type_name]
    obj_values = []
    field_value_pairs = re.findall(r'(\w+)\s*:\s*(?:({.*?})|([^,}]+))\s*(?=,|\})', obj_values_str)
    for field_name, nested_obj_str, value_str in field_value_pairs:
        if nested_obj_str:  # nested object
            nested_obj = create_object(field_name + ':' + nested_obj_str, type_configs)
            value = nested_obj
        else:
            value = convert_value(value_str.strip(), obj_type.fields[field_name])
        obj_values.append(value)
    # Create and return object
    return Object(obj_type, obj_values)

def create_objects(lines: list[str], type_configs: dict[str, Type]) -> list[Object]:
    objects = []
    for line in lines:
        obj = create_object(line, type_configs)
        if obj:
            objects.append(obj)
    return objects

def deserialize_data(serialized_data: str) -> list[Object]:
    lines = serialized_data.strip().split('\n')
    index = lines.index(';;;')
    type_lines = lines[:index]
    object_lines = lines[index+1:]
    type_configs = create_type_configs(type_lines)
    objects = create_objects(object_lines, type_configs)
    return objects

# Example usage
serialized_data = '''\
|date|
[fields:        {"day","month","year"}
[field_types:   {int,int,int}
|person|
[fields:        {"name","age"}
[field_types:   {string, date}
;;;
person: {"Peter",date:{16,4,1978}}
'''
objects = deserialize_data(serialized_data)
for obj in objects:
    print(obj.obj_type.name, obj.values)