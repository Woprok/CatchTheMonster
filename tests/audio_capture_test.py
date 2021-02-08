from libs.audio_capturer import *
from libs.cloud_manager import CloudManager
from libs.configuration_provider import ConfigurationProvider as CfgP
import time

def all():
    cfg_provider = CfgP()
    cfg = cfg_provider.get_configuration()
    start = time.time()
    ac = AudioCapturer(int(cfg[CfgP.AUDIO_CAPTURE_TIME_KEY]))
    byte_stream = ac.record_instance()
    #ac.save_to_file(byte_stream)

    ct = CloudManager("account.json",cfg[CfgP.GOOGLE_PROJECT_ID_KEY],"global", "sk_SK", "en_US")
    ct.create_channels()

    s = ct.transcribe(byte_stream)
    print("Transcribed text:", s)
    print("Translated text:", ct.translate(s))
    end = time.time()
    print(end - start)