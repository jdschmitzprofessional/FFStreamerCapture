import json


def dump_variables(input_dict):
    data = {}
    compatible_types = [ str, int, float ]
    for k,v in input_dict.items():
        if type(v) not in compatible_types
            data[k] = str(v)
        else:
            data[k] = v
    return json.dumps(data)

