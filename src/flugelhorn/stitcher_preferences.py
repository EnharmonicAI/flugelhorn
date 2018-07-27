"""Stitcher preferences module."""

from setting_definitions import SETTING_DEFINITIONS


class PropertyDescriptor:
    """Simple property descriptor w/ validation against allowed values."""
    def __init__(self, name, allowed_values=None, default=None): #, instance):
        self.name = name
        self.allowed_values = allowed_values
        self.default = default


    def __get__(self, instance, objtype):
        if instance is None:
            return self
        return instance.__dict__[self.name]


    def __set__(self, instance, value):
        if self._validate(value):
            # If validation passes, set the new value
            instance.__dict__[self.name] = value
        else:
            try:
                current_value = instance.__dict__[self.name]
                print("Keeping {0} value as {1!r}.".format(self.name, current_value))
            except KeyError:
                # If not set the value to the default
                print("Setting {0} to default {1!r}.".format(self.name, self.default))
                instance.__dict__[self.name] = self.default 


    def _validate(self, value): 
        # TODO(ryan): Potentially add type validation
        try:
            self._validate_value(value)
            return True
        except ValueError as e:
            # TODO(ryan): log value errors
            print(e)
            return False 


    def _validate_value(self, value):
        """Value validation."""
        if (self.allowed_values) and (value not in self.allowed_values):
            raise ValueError(
                '{0} value must be in {1!r}, requested value was {2}'.format(
                    self.name, self.allowed_values, value))


# TODO(ryan): DEPRECATED with new setting factory
# TODO(ryan): Add appropriate inheritance
class BlendSettings:
    """Blend Setting."""
    tag = 'blend'
    
    # _properties = []
    prop_def = SETTING_DEFINITIONS[tag]['useOpticalFlow']
    useOpticalFlow = PropertyDescriptor(prop_def.allowed, prop_def.default)
    # useOpticalFlow = PropertyDescriptor('useOpticalFlow')
    # useNewOpticalFlow = PropertyDescriptor('useNewOpticalFlow')
    # mode = PropertyDescriptor('mode')
    # samplingLevel = PropertyDescriptor('samplingLevel')
    # useTopFixer= PropertyDescriptor('useTopFixer')

    # TODO(ryan): automatically build this...w/ defaults
    _properties = ['useOpticalFlow', 'useNewOpticalFlow', 'mode',
                   'samplingLevel', 'useTopFixer']

    def __init__(self,
                 useOpticalFlow=True,
                 useNewOpticalFlow=True,
                 mode='pano',
                 samplingLevel='fast',
                 useTopFixer=False):
        self.useOpticalFlow = useOpticalFlow
        self.useNewOpticalFlow = useNewOpticalFlow
        self.mode = mode
        self.samplingLevel = samplingLevel
        self.useTopFixer = useTopFixer


    def __repr__(self):
        property_list = ['{0}={1!r}'.format(key, getattr(self, key, None))
                         for key in self._properties]
        nested_settings = ['{0}={1!r}'.format(key, getattr(self, key, None))
                           for key in self._nested]
        repr_str = '{0}({1}{2})\n'.format(self.tag, ', '.join(property_list),
                                     ', '.join(nested_settings)) 
        return repr_str
        # return '{0}({1})'.format(self.tag, ', '.join(property_list)) 



class Setting:
    """Base class for settings."""
    # def __repr__(self):
    #     property_list = ['{0}={1!r}'.format(key, getattr(self, key, None))
    #                      for key in self._properties]
    #     return '{0}({1})'.format(self.tag, ', '.join(property_list)) 

    def __repr__(self):
        property_list = ['{0}={1!r}'.format(key, getattr(self, key, None))
                         for key in self._properties]
        if len(self._nested) > 0:
            nested_settings = ['\t{0}={1!r}'.format(key, getattr(self, key, None))
                           for key in self._nested]
            repr_str = '{0}({1}\n{2})'.format(self.tag, ', '.join(property_list),
                                              ',\n'.join(nested_settings)) 
        else:
            repr_str = '{0}({1})'.format(self.tag, ', '.join(property_list)) 
        return repr_str

   
    def to_dict(self):
        """Convenience method for getting a dictionary for xml building."""
        return self.__dict__


# def setting_factory_backup(setting_name, properties):
#     try:
#         properties = properties.replace(',', ' ').split()
#     except AttributeError:  # no .replace or .split
#         pass  # Assume properties is already a sequence
#     props = tuple(properties)
# 
#     def __init__(self, *args, **kwargs):
#         # Start with default values in a dict and update with args/kwargs
#         attrs = {}
#         for prop in self._properties:
#             prop_descr = getattr(self.__class__, prop)
#             attrs[prop] = prop_descr.default
#         
#         # print(attrs)
#          # print(args)
#         # print(kwargs)
#         arg_attrs = dict(zip(self._properties, args))
#         # print(arg_attrs)
#         arg_attrs.update(kwargs)
#         # print(arg_attrs)
#         attrs.update(arg_attrs)
#         # print(attrs)
# 
#         # Set the attributes through the PropertyDescriptor
#         for name, value in attrs.items():
#             # print(name, value)
#             setattr(self, name, value)
#             # Set defaults if not supplied
#             
# 
#     prop_descriptors = {}
#     for prop in properties:
#         print(prop)
#         prop_def = SETTING_DEFINITIONS[setting_name][prop]
#         prop_descriptors[prop] = PropertyDescriptor(prop,
#                                     prop_def.allowed, prop_def.default)
# 
#     cls_attrs = dict(__init__ = __init__,
#                      tag = setting_name,
#                      _properties = props)
#     cls_attrs.update(prop_descriptors)
# 
#     return type(setting_name, (Setting,), cls_attrs)
# 


def setting_factory(setting_name, properties):
    """Automatically create a new setting object.

    Args:
        setting_name: name for the new Settings object
        properties: dict of PropertyDefs
    """
    print('Building setting: {0}'.format(setting_name))
    # try:
    #     properties = properties.replace(',', ' ').split()
    # except AttributeError:  # no .replace or .split
    #     pass  # Assume properties is already a sequence
    # props = tuple(properties.keys())

    def __init__(self, *args, **kwargs):
        # Start with default values in a dict and update with args/kwargs
        attrs = {}
        for prop in self._properties:
            prop_descr = getattr(self.__class__, prop)
            if isinstance(prop_descr, PropertyDescriptor):
                attrs[prop] = prop_descr.default
        
        # print(attrs)
         # print(args)
        # print(kwargs)
        arg_attrs = dict(zip(self._properties, args))
        # print(arg_attrs)
        arg_attrs.update(kwargs)
        # print(arg_attrs)
        attrs.update(arg_attrs)
        # print(attrs)

        # Set the attributes through the PropertyDescriptor
        for name, value in attrs.items():
            # print(name, value)
            setattr(self, name, value)
            # Set defaults if not supplied
            

    prop_descriptors = {}
    nested = {}
    for prop, prop_def in properties.items():
        # TODO(ryan): This currently handles a single level of nesting
        print(prop, type(prop_def))
        if isinstance(prop_def, dict):
            print("NESTED!!")
            print(properties[prop])
            # Nested properties have another Settings object as their value
            # They are not PropertyDescriptors
            # Create our setting class and instantiate an instance 
            nested[prop] = setting_factory(prop, properties[prop])
        
            # new_setting = setting_factory(prop, properties[prop])
            # prop_descriptors[prop] = new_setting() 

        # prop_def = SETTING_DEFINITIONS[setting_name][prop]
        else:
            prop_descriptors[prop] = PropertyDescriptor(prop,
                                                        prop_def.allowed,
                                                        prop_def.default)

    # props = tuple(prop_descriptors.keys())
    # nested = tuple(nested.keys())
    cls_attrs = dict(__init__ = __init__,
                     tag = setting_name,
                     _properties = tuple(prop_descriptors.keys()),
                     _nested = tuple(nested.keys()))
    cls_attrs.update(prop_descriptors)
    cls_attrs.update(nested)

    return type(setting_name, (Setting,), cls_attrs)


def build_config_template():
    """Return a configuration template for stitching settings."""
    # Naively create a dict object with values as record objects
    config_template = {}
    for setting in SETTING_DEFINITIONS.keys():
        print(setting)
        props = [p for p in SETTING_DEFINITIONS[setting]]
        print(props)    
        config_template[setting] = setting_factory(setting, props)

    return config_template


def build_config_template_new():
    """Return a configuration template for stitching settings."""
    # Naively create a dict object with values as record objects
    # We need to build from bottom up...
    config_template = {}
    config_template = setting_factory('settings', SETTING_DEFINITIONS)
    # for key, value in SETTING_DEFINITIONS.items():
    #     print(key)
    #     config_template[key] = setting_factory(key, value)
    # print(config_template)

    return config_template
        
        # Search props to see if we have nesting
        # for key, value in SETTING_DEFINITIONS[setting].items():
        #     if isinstance(value, dict):
        #         print("NESTED")
        #         print(key)
        #         # props = [p for p in SETTING_DEFINITIONS[setting][key]]
        #         new_setting = setting_factory(key, value)
        #         print(new_setting)
        #         # for k, v in SETTING_DEFINITIONS[setting][prop].items():
        #         #     print(k, v)            
                    
 
        # props = [p for p in SETTING_DEFINITIONS[setting]]
        # print(props)    
        # config_template[setting] = setting_factory(setting, props)
 
    # config = {}
    # for s in config_template:
    #     config[s] = config_template[s]()

    # return config


# def initialize_template(config_template):
#     """Create a new instance from a Settings config template w/ defaults."""
#     # Recursiveley initialize from top->down
#     temp = config_template()    
#     for n in temp._nested:
#         print(n)
#         new_setting = getattr(temp, n)
#         initialized_setting = _initialize_setting(new_setting)
#         setattr(temp, n, initialized_setting)
# 
#     return temp
# 

def initialize_settings(setting_template):
    """Create a new instance from a Settings config template w/ defaults."""
    # Recursively initialize from top->down
    top_setting = setting_template()
    for n in top_setting._nested:
        print(n)
        sub_setting = getattr(top_setting, n)
        initialized_setting = initialize_settings(sub_setting)
        setattr(top_setting, n, initialized_setting)

    return top_setting


def create_stitcher_config(config_template, settings):
    """Create a stitcher configuration dict.
    
    Applies settings as defined in a settings dictionary,
    leaving non-defined settings on their default values.
    """
    # config_template = build_config_template()
    # print(config_template)
    
    # Traverse our template and initialize
    for prop in config_template._properties:
        print(prop)    
        print(type(getattr(config_template, prop)))
 
    # config = {}
    # for s in config_template:
    #     config[s] = config_template[s]()

    # print(config)        
    # # Replace defaults w/ our settings
    # # This also validates our settings
    # for s in settings.keys():
    #     print(s) 
    #     for prop in settings[s]:
    #         setattr(config[s], prop, settings[s][prop])

    # print(config)        
    # return config    

if __name__ == '__main__':
    # props = [p for p in PROPERTY_DEFINITIONS['blend'].keys()]
    # # print(props)
    # blend = setting_factory('blend', props) 

    # Iterate through PROPERTY DEFINITIONS to create our settings
    # We don't want to be playing with a bunch of lose variables,
    # so I need a single data structure to pass around and save
    # A large property object should work...esp if I limit nesting

    # Let's start iterating through..
    # print(PROPERTY_DEFINITIONS)

    # Naively create a dict object with values as record objects
    # config_template = build_config_template()
    # config_template = {}
    # for setting in SETTING_DEFINITIONS.keys():
    #     props = [p for p in PROPERTY_DEFINITIONS[setting]]
    #     config_template[setting] = setting_factory(setting, props)

    template = build_config_template_new()
    temp = initialize_settings(template)

    # TODO(ryan):
        # fileCount should be defined by looking at directories
    all_settings = {
        'input': {
            'type': 'video',
            'lensCount': 6,
            'fileCount': 1
        }, 
        'blend': {
            'useOpticalFlow': True,
            'useNewOpticalFlow': True,
            'mode': '?????',
            'samplingLevel': 'fast',
            'useTopFixer': False,
            'blend_calibration': {
                'lensVersion': 7,
                'lensType': 12,
                'captureTime': '?????',
                'captureTimeIndex': '?????',
                'useDefaultCircle': True,
                'useDefaultOffset': True
            }
        },
        # Check local hardware setting
        'encode': {
            'useHardware': True,
            'threads': 1,
            'preset': 'superfast',
            'profile': 'baseline'
        },
        'decode': {
            'useHardware': True,
            'threads': 1,
            'count': 1
        },
        'blender': {
            'type': 'auto'
        },
        'gyro': {
            'version': 3, # Version from pro.prj file
            'type': 'pro', 
            'enable': True,
            'filter': 'akf'
        },
        # Add timeOffset tag, based on start_ts from pro.pj XML file
        # Add files tag, w/ path to desired gyro.dat file in our image folder
        'gyro_calibration': {
            # These values fcome from pro.pj XML file
            'gravity_x': 0.0008186848958333335,
            'gravity_y': -0.00043326822916666665,
            'gravity_z': 0.9980732421875
        },
        'gyro_angle': {
            'diff_pan': 0,
            'diff_tilt': 0,
            'diff_roll': 0,
            'distance': 603.3333333333334
        },
        'color': {
            'brightness': 0,
            'contrast':0,
            'highlight': 0,
            'shadow': 0,
            'saturation': 0,
            'tempture': 0,
            'tint': 0,
            'sharpness': 0 
        },
        'depthMap': {
            'enable': False,
            'path': '',
            'inverse': True
        },
        'output': {
            'width': 3840,
            'height':1920,
            'dst': '~/stitchertest/test.mp4',
            'type': 'video'
        },
        'video': {
            'fps': 29.97,
            'codec': 'h264',
            # TODO(ryan): This should be calculated?
            'bitrate': 62914560,
            'useInterpolation': False
        },
    'audio': {
        'type': 'pano',
        'device': 'insta360'
    }
}

    # c = create_stitcher_config(template, all_settings)
