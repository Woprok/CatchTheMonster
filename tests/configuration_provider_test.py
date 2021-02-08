from libs.configuration_provider import ConfigurationProvider
import os

def cfg_base_single():
    """
    What's up.
    """
    cp = ConfigurationProvider()
    result = cp.get_configuration()
    with open(cp.CONFIG_FILENAME, 'r') as json_file:
        print(json_file.read())

def cfg_base_twice():
    if os.path.isfile(ConfigurationProvider.CONFIG_FILENAME):
        print('Deleting File')
        os.remove(ConfigurationProvider.CONFIG_FILENAME)
    cfg_base_single()
    cfg_base_single()
    print('Finished')