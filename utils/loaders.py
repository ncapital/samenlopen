import yaml


def load_yaml(yaml_file):
    stream = open(yaml_file, 'r')
    return yaml.safe_load(stream=stream)


def load_keys(yaml_file):
    yaml_data = load_yaml(yaml_file)
    return yaml_data['keys']
