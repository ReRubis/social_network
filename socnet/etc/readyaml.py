import yaml


def read_config_yaml():
    """
    Parses config file to get
    the contents
    """
    with open('config.yaml', 'r') as stream:
        try:
            parsed_yaml = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    return parsed_yaml
