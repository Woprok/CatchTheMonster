import io
import sys
import grpc
        
# Examples might are most useful for learning: https://github.com/googleapis/python-speech/tree/master/samples/microphone
# Following import's are related to 
from google import auth as google_auth
from google.oauth2 import service_account as google_oauth2_service_account
from google.auth.transport import grpc as google_auth_transport_grpc
from google.auth.transport import requests as google_auth_transport_requests

# Following import's are related to speech and translation services
from google.cloud.speech.v1.cloud_speech_pb2 import *
from google.cloud.speech.v1.cloud_speech_pb2_grpc import *
from google.cloud.translate.v3.translation_service_pb2 import *
from google.cloud.translate.v3.translation_service_pb2_grpc import *


class CloudManager():
    SPEECH_SERVICE_ADDRESS = 'speech.googleapis.com:443'
    TRANSLATION_SERVICE_ADDRESS = 'translate.googleapis.com:443'
    SERVICE_SCOPES = ['https://www.googleapis.com/auth/cloud-platform']
    CLOUD_OUTPUT_LANGUAGE = 'en_US' # code operates in english for simplicity
    """
    Manages usage of google cloud api.
    """
    def __init__(self, cloud_account, cloud_project, cloud_location, cloud_source_language, cloud_target_language):
        """
        Initialize instance with credentials specified in file. 
        Credentials are required to call the service.
        """
        print(f'From: {cloud_source_language}, To: {cloud_target_language}')
        self.credentials = google_oauth2_service_account.Credentials.from_service_account_file(cloud_account)
        self.scoped_credentials = self.credentials.with_scopes(CloudManager.SERVICE_SCOPES)
        self.cloud_project_id = cloud_project
        self.cloud_location = cloud_location
        self.speech_config = RecognitionConfig()
        # Encoding and sample rate are only needed for RAW files.
        # When using WAV or FLAC files it is detected automatically. But we are using recorde audio.
        self.speech_config.encoding = RecognitionConfig.LINEAR16
        self.speech_config.sample_rate_hertz = 16000
        self.speech_config.language_code = cloud_source_language
        self.source_language = cloud_source_language
        self.target_language = cloud_target_language
    
    def create_channels(self):
        """
        The request object represents an HTTP transport layer used to renew tokens.
        Create a channels...
        """
        # Request tokens
        self.speech_request = google_auth_transport_requests.Request()
        self.translation_request = google_auth_transport_requests.Request()
        # Channels
        self.speech_channel = google_auth_transport_grpc.secure_authorized_channel(
            self.scoped_credentials, self.speech_request, self.SPEECH_SERVICE_ADDRESS) 
        self.translation_channel = google_auth_transport_grpc.secure_authorized_channel(
            self.scoped_credentials, self.translation_request, self.TRANSLATION_SERVICE_ADDRESS)
        # Create a stub object that provides the service interface.
        self.speech_stub = SpeechStub(self.speech_channel)
        self.translation_stub = TranslationServiceStub(self.translation_channel)

    def kill_channels(self):
        """
        Dispose channels before quitting application...
        """
        pass

    def transcribe(self, data_to_transcribe):
        """
        Transcribe speech with help of cloud.
        """
        # Define Audio
        audio = RecognitionAudio()
        audio.content = data_to_transcribe
        # audio.content = open (sys.argv [1], 'rb').read()
        # Recognize Audio Request
        request = RecognizeRequest(config = self.speech_config, audio = audio)

        try:
            # Call the service through the stub object.
            response = self.speech_stub.Recognize(request)
            # Response contains field results[], each of them contains field alternatives[]
            # each alternative contains transcript, confidence and words
            recognized_text = response.results[0].alternatives[0].transcript
            print('Recognized text:', recognized_text)
        except:
            recognized_text = None
        return recognized_text

    def requires_translation(self):
        return self.source_language != self.target_language 

    def translate(self, text_to_translate):
        """
        Translate text with help of cloud.
        """
        # Translate Text Request
        request = TranslateTextRequest()
        request.contents.append(text_to_translate)
        request.parent = f"projects/{self.cloud_project_id}/locations/{self.cloud_location}"
        request.source_language_code = self.source_language
        request.target_language_code = self.target_language

        try:
            # Call the service through the stub object.
            response = self.translation_stub.TranslateText(request)
            translated_text = response.translations[0].translated_text
            print('Translated text:', translated_text)
        except:
            translated_text = None
        return translated_text