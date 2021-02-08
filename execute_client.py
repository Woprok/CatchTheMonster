#!/usr/bin/env python3
import grpc
from libs.configuration_provider import ConfigurationProvider as CfgP
from libs.client_manager import ClientManager

#--------------------
# Main
#--------------------
print('Loading configuration:')
cfg_provider = CfgP()
cfg = cfg_provider.get_configuration()

print('Initializing server certificates:')
certificate_crt = open (cfg[CfgP.CERTIFICATE_CRT_KEY], 'rb').read()

print('Initializing server connection:')
client = ClientManager(cfg[CfgP.SERVER_ADDRESS_KEY], certificate_crt, int(cfg[CfgP.AUDIO_CAPTURE_TIME_KEY]))
client.InitializeProviders()
client.Execute()