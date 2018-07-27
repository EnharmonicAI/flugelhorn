"""YAML settings parsing module."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


from ruamel.yaml import YAML

from stitcher_preferences import build_config_template_new, initialize_settings

def load_yaml_to_dict(path):
    with open(path, 'r') as f:
        yaml = YAML(typ='safe')
        data = yaml.load(f)    

    return data


def parse_yaml_dict(settings_dict):
    """Create a stitcher Settings configuration object.
    
    Applies settings as defined in a settings dictionary,
    leaving non-defined settings on their default values.
    """

    template = build_config_template_new()
    config = initialize_settings(template)

    print(settings_dict)

    # Replace defaults w/ our settings
    # This also validates our settings
    for key, value in settings_dict.items():
        print(key, isinstance(value, dict)) 
        # Recurse
        _config_from_dict(getattr(config, key, None), value)

        # for key in value:
        #     print('\t', prop)
        #     setattr(config, prop, value)

    print(config)        
    return config 

def _config_from_dict(config, settings_dict):
    print("RECURSE")
    print(config)
    for key, value in settings_dict.items():
        print(key, isinstance(value, dict)) 
        if isinstance(value, dict):
            _config_from_dict(getattr(config, key, None), value) 
        else:
        # print(key, isinstance(value, dict))
            setattr(config, key, value)
    print(config) 


if __name__ == '__main__':
    test_path = '/Users/ryan/Projects/VrVideoAutomations/test.yaml' 

    test = load_yaml_to_dict(test_path)
    settings = parse_yaml_dict(test)
    # parse_dict_to_object(test)



