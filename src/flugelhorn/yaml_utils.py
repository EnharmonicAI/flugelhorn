"""YAML configuration load & parsing module."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from ruamel.yaml import YAML

from stitcher_preferences import build_config_template, initialize_settings


def _load_yaml_to_dict(path):
    """Read a YAML file into a py dict."""
    with open(path, 'r') as f:
        yaml = YAML(typ='safe')
        data = yaml.load(f)

    return data


def _parse_yaml_dict(settings_dict):
    """Create a stitcher Settings configuration object.

    Applies settings as defined in a settings dictionary,
    leaving non-defined settings on their default values.
    """

    template = build_config_template()
    config = initialize_settings(template)

    print(settings_dict)

    # Recursively replace defaults w/ our settings
    # This also validates our settings
    _config_from_dict(config, settings_dict)

    return config


def _config_from_dict(config, settings_dict):
    print(config)
    for key, value in settings_dict.items():
        if isinstance(value, dict):
            _config_from_dict(getattr(config, key, None), value)
        else:
        # print(key, isinstance(value, dict))
            setattr(config, key, value)
    print(config)


def load_configuration_from_yaml(yaml_path):
    """Load Stitcher configuration from yaml file.

    Args:
        yaml_path: path to settings.yaml file
    Returns:
        config: a Settings object to be used for Stitcher run
                Note that config will still need to have final
                settings set based on media files and pro.prj file
    """
    yaml_dict = _load_yaml_to_dict(yaml_path)
    config = _parse_yaml_dict(yaml_dict)

    return config
