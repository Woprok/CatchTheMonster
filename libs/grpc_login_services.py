import grpc
import random
from protos.login_pb2 import *
from protos.login_pb2_grpc import *

def ask_for_username():
    print('Enter username:')
    username = input()
    return username

def ask_for_avatar():
    print('Enter avatar (You can leave this empty (prefer) or type emoji (browser column) (! will cause problems if done wrong) https://unicode.org/emoji/charts/full-emoji-list.html):')
    avatar = input()
    if not avatar:
        avatar = random.choice(['🤴','👸','👳','👼','🦸','🦹','🧙','🧚','🧛','🧜','🧝','🧞','🧟','🐒'])
    return avatar

def login_generate_request():
    rv = LoginRequest()
    rv.Username = ask_for_username()
    rv.Avatar = ask_for_avatar()
    return rv

def login_generate_response(rq, id):
    rv = LoginResponse()
    rv.IsSuccess = True
    rv.Username = rq.Username
    rv.Avatar = rq.Avatar
    rv.PlayerId = id
    return rv
    
def login_request_string(lr):
    return f'login: {lr.Username} {lr.Avatar}'
def login_response_string(lr):
    return f'login: {lr.IsSuccess} {lr.Username} {lr.Avatar} {lr.PlayerId}'

# Server Service implementation.
# The implementation inherits from a generated base class.
class LoginRequestProviderServerServicer(LoginRequestProviderServicer):
    def __init__(self, game_state_manager):
        super().__init__()
        self.game_manager = game_state_manager

    def RequestLogin(self, request, context):
        print("Request", login_request_string(request))
        response = self.game_manager.register_player(request) 
        print("Response", login_response_string(response))
        return response

# Client Message Spamer
def login_send_request(stub):
        request = login_generate_request()
        print("Request", login_request_string(request))
        # Call the service through the stub object.
        response = stub.RequestLogin(request)
        print("Response", login_response_string(response))
        return response