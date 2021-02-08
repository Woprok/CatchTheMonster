from concurrent import futures
from time import sleep
from libs.web_service import WebService
from libs.grpc_time_services import *
from libs.grpc_login_services import *
from libs.grpc_game_services import *
from libs.game_state_manager import *
from libs.web_service import *

class ServerManager():
    SERVER_THREAD_COUNT = 4
    """
    Wrapper around server services
    """
    def __init__(self, server_address, certificate_key, certificate_crt, cloud):
        """
        Create the server object.
        The server object represents the server runtime.
        It needs to be told what service to provide and what port to listen on.
        """
        self.credentials = grpc.ssl_server_credentials ([( certificate_key, certificate_crt )])
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers = ServerManager.SERVER_THREAD_COUNT))
        self.server.add_secure_port(server_address, self.credentials)
        self.cloud_manager = cloud

    def InitializeProviders(self, map_file, turn_timer):
        """
        Actual objects that do something...
        """
        self.game_state_manager = GameStateManager(self.cloud_manager, map_file, turn_timer)
        self.web_service = WebService(self.game_state_manager)
        print("Initializing grpc services")
        add_TimeRequestProviderServicer_to_server(TimeRequestProviderServerServicer(), self.server)
        add_LoginRequestProviderServicer_to_server(LoginRequestProviderServerServicer(self.game_state_manager), self.server)
        add_GameProviderServicer_to_server(GameProviderServerServicer(self.game_state_manager), self.server)
        pass
    
    def Execute(self):
        """
        Just keep running until killed from console.
        """
        self.game_state_manager.initialize_game()
        self.server.start()
        self.web_service.start_presenting()
        self.server.wait_for_termination()