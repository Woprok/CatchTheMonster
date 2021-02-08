import grpc
from libs.grpc_time_services import *
from libs.grpc_login_services import *
from libs.grpc_game_services import *
from libs.audio_capturer import *
from threading import Thread, Lock
import time

class ClientManager():
    """
    Wrapper around client services
    """
    def __init__(self, server_address, certificate_crt, record_time):
        """
        Create the server object.
        The server object represents the server runtime.
        It needs to be told what service to provide and what port to listen on.
        """
        self.credentials = grpc.ssl_channel_credentials(root_certificates = certificate_crt)
        self.server_address = server_address
        self.audio_manager = AudioCapturer(record_time)

    def InitializeProviders(self):
        """
        Actual objects that do something...
        """    
        # Create the channel used to connect to the server.
        self.channel = grpc.secure_channel(self.server_address, self.credentials)
        # Create a stub object that provides the service interface for each service.
        self.time_stub = TimeRequestProviderStub(self.channel)
        self.login_stub = LoginRequestProviderStub(self.channel)
        self.game_stub = GameProviderStub(self.channel)
    
    def Execute(self):
        """
        Executing loop
        """
        # Let's verify connection with good old time message.
        time_send_request(self.time_stub)
        # Afterward we can join the game with login request.
        self.login_data = login_send_request(self.login_stub)
        if self.login_data.IsSuccess:
            print(f'Joined server with id: {self.login_data.PlayerId} as: {self.login_data.Username} {self.login_data.Avatar}')
        # Finally we can play the game with provided id.
        self.game_loop_execution()

    def display_game_info(self):
        while self.is_executing_loop == True:
            # this client no longer displays full state, to make it easier to use
            game_state_request(self.game_stub, create_game_state_request(self.login_data.PlayerId, True))
            time.sleep(self.state_time)

    def record_input(self):
        result = self.audio_manager.record_instance()
        return result

    def turn_game_processor(self):
        while True:
            voice_command = self.record_input()
            game_turn_request(self.game_stub, create_game_turn_request(self.login_data.PlayerId,
                'DEBUG_MODE', #originally used to supply commands 
                voice_command))
            time.sleep(self.action_time)

    def game_loop_execution(self):
        """
        Manages whole game on client side. Client does very little compared to server.
        """
        # wait before graphic update is approximately half second.
        self.state_time = 2
        self.is_executing_loop = True
        self.state_thread = Thread(target = self.display_game_info)
        self.state_thread.daemon = True
        self.state_thread.start()

        # wait before turn captures
        self.action_time = 3 #cca 3 secs is process time
        self.turn_game_processor()

