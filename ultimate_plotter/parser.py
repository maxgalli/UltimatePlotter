import json

def universal_parser(config_file):
    frmt = config_file.rsplit('.', maxsplit=1)[-1]

    if frmt == "json":
        with open(config_file) as f:
            config = json.load(f)

    return config
