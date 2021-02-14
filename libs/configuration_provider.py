import json
import os.path

class ConfigurationProvider():
    """
    Cfg dump here.
    """
    # Keys
    SERVER_ADDRESS_KEY = 'server_address'
    WEBSERVER_ADDRESS_KEY = 'web_address'
    WEBSERVER_PORT_KEY = 'web_port'
    GOOGLE_ACCOUNT_KEY = 'cloud_account'
    GOOGLE_PROJECT_ID_KEY = 'cloud_project'
    GOOGLE_LOCATION_KEY = 'cloud_location'
    GOOGLE_SOURCE_LANGUAGE_KEY = 'source_language'
    GOOGLE_TARGET_LANGUAGE_KEY = 'target_language'
    AUDIO_CAPTURE_TIME_KEY = 'capture_time'
    TURN_CAPTURE_TIME_KEY = 'turn_time'
    CERTIFICATE_KEY_KEY = 'certificate_key'
    CERTIFICATE_CRT_KEY = 'certificate_crt'
    MAP_PLAN_FILENAME_KEY = 'map_data_key'
    # Default Values
    SERVER_ADDRESS_VALUE = 'localhost:8888'
    WEBSERVER_ADDRESS_VALUE = 'localhost'
    WEBSERVER_PORT_VALUE = '5001'
    GOOGLE_ACCOUNT_VALUE = 'account.json'
    GOOGLE_PROJECT_ID_VALUE = 'UNDEFINED'
    GOOGLE_LOCATION_VALUE = 'global'
    GOOGLE_SOURCE_LANGUAGE_VALUE = 'sk_SK'
    GOOGLE_TARGET_LANGUAGE_VALUE = 'en_US'
    AUDIO_CAPTURE_TIME_VALUE = '4'
    TURN_CAPTURE_TIME_VALUE = '10'
    CERTIFICATE_KEY_VALUE = 'server.key'
    CERTIFICATE_CRT_VALUE = 'server.crt'
    MAP_PLAN_FILENAME_VALUE = 'map.data'
    CONFIG_FILENAME = 'ctm_config.json'
    def __init__(self):
        self.data = None

    def get_current_configuration(self):
        """
        Wrapper...
        """
        with open(ConfigurationProvider.CONFIG_FILENAME, 'r') as json_file:
            self.data = json.load(json_file)
        return self.data

    def ask_for_project_id(self):
        """
        We require project id to run, so the configuration will ask for it at runtime if it's being generated from default.
        """
        print('Execution requires project id from google cloud. Please type it now:')
        project_id = input()
        print('Setting ->{}<- as project id:'.format(project_id))
        return project_id

    def get_default_configuration(self):
        """
        Full configuration, so it can be created at runtime...
        """
        self.data = {
            ConfigurationProvider.SERVER_ADDRESS_KEY: ConfigurationProvider.SERVER_ADDRESS_VALUE,
            ConfigurationProvider.WEBSERVER_ADDRESS_KEY: ConfigurationProvider.WEBSERVER_ADDRESS_VALUE,
            ConfigurationProvider.WEBSERVER_PORT_KEY: ConfigurationProvider.WEBSERVER_PORT_VALUE,
            ConfigurationProvider.GOOGLE_ACCOUNT_KEY : ConfigurationProvider.GOOGLE_ACCOUNT_VALUE,
            ConfigurationProvider.GOOGLE_PROJECT_ID_KEY : ConfigurationProvider.GOOGLE_PROJECT_ID_VALUE,
            ConfigurationProvider.GOOGLE_LOCATION_KEY : ConfigurationProvider.GOOGLE_LOCATION_VALUE,
            ConfigurationProvider.GOOGLE_SOURCE_LANGUAGE_KEY : ConfigurationProvider.GOOGLE_SOURCE_LANGUAGE_VALUE,
            ConfigurationProvider.GOOGLE_TARGET_LANGUAGE_KEY : ConfigurationProvider.GOOGLE_TARGET_LANGUAGE_VALUE,
            ConfigurationProvider.AUDIO_CAPTURE_TIME_KEY : ConfigurationProvider.AUDIO_CAPTURE_TIME_VALUE,
            ConfigurationProvider.TURN_CAPTURE_TIME_KEY : ConfigurationProvider.TURN_CAPTURE_TIME_VALUE,
            ConfigurationProvider.CERTIFICATE_KEY_KEY : ConfigurationProvider.CERTIFICATE_KEY_VALUE,
            ConfigurationProvider.CERTIFICATE_CRT_KEY : ConfigurationProvider.CERTIFICATE_CRT_VALUE,
            ConfigurationProvider.MAP_PLAN_FILENAME_KEY : ConfigurationProvider.MAP_PLAN_FILENAME_VALUE,
        }
        self.data[ConfigurationProvider.GOOGLE_PROJECT_ID_KEY] = self.ask_for_project_id()
        return self.data

    def set_default_configuration(self):
        """
        Providing method to correctly create cfg file for user...
        """
        default = self.get_default_configuration()
        with open(ConfigurationProvider.CONFIG_FILENAME, 'w') as json_file:
            json.dump(default, json_file, indent=4)
        return default

    def get_configuration(self):
        """
        Load's program configuration. So we don't have to care about input parameters...
        """
        if os.path.isfile(ConfigurationProvider.CONFIG_FILENAME):
            print('Loading from file...')
            return self.get_current_configuration()
        else:
            print('Creating default and saving for future modifications by user...')
            return self.set_default_configuration()