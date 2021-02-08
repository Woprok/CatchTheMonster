#!/usr/bin/env python3
import grpc
from libs.configuration_provider import ConfigurationProvider as CfgP
from libs.cloud_manager import CloudManager
from libs.server_manager import ServerManager

#--------------------
# Main
#--------------------
print('Loading configuration:')
cfg_provider = CfgP()
cfg = cfg_provider.get_configuration()

print('Initializing server certificates:')
certificate_key = open (cfg[CfgP.CERTIFICATE_KEY_KEY], 'rb').read()
certificate_crt = open (cfg[CfgP.CERTIFICATE_CRT_KEY], 'rb').read()

print('Initializing cloud connection:')
cloud = CloudManager(cfg[CfgP.GOOGLE_ACCOUNT_KEY], 
    cfg[CfgP.GOOGLE_PROJECT_ID_KEY], cfg[CfgP.GOOGLE_LOCATION_KEY],
    cfg[CfgP.GOOGLE_SOURCE_LANGUAGE_KEY], cfg[CfgP.GOOGLE_TARGET_LANGUAGE_KEY])
cloud.create_channels()

print('Initializing server connection:')
server = ServerManager(cfg[CfgP.SERVER_ADDRESS_KEY], certificate_key, certificate_crt, cloud)
server.InitializeProviders(cfg[CfgP.MAP_PLAN_FILENAME_KEY], int(cfg[CfgP.TURN_CAPTURE_TIME_KEY]))
server.Execute()

#--------------------
# Dead, won't be reached as GRPC is bloking all execution until it receives kill (CTL+C).
#--------------------
print('Type x to exit')
while "x" != input():
    continue
cloud.kill_channels()