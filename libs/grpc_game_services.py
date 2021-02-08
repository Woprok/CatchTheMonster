import grpc
import random
from protos.game_pb2 import *
from protos.game_pb2_grpc import *

def game_state_request_to_string(gsr):
    return f'Waiting for game state as {gsr.PlayerId}'
def game_state_response_to_string(gsr):
    result = gsr.MapPlan
    result += f'{gsr.ScoreBoard}\n'
    for pc in gsr.PlayerScore:
        result += f'{pc}\n'
    result += f'Next turn informations:\n{gsr.Info}\n'
    return result
def game_state_reduced_response_to_string(gsr):
    result = f'Next turn informations:\n{gsr.Info}\n'
    return result
def game_turn_request_to_string(gtr):
    return f'Waiting for turn to be processed as {gtr.PlayerId} {gtr.DebugDump}'
def game_turn_response_string(gtr):
    return f'Turn accepted, await result. Debug:{gtr.DebugDump}'

# Server Service implementation.
# The implementation inherits from a generated base class.
class GameProviderServerServicer(GameProviderServicer):
    def __init__(self, game_state_manager):
        super().__init__()
        self.game_manager = game_state_manager

    def RequestStateUpdate(self, request, context):
        #print("Request", game_state_request_to_string(request))
        response = self.game_manager.on_game_state_request(request) 
        #print("Response\n", game_state_response_to_string(response))
        return response
    def RequestTurn(self, request, context):
        #print("Request", game_turn_request_to_string(request))
        response = self.game_manager.on_game_turn_request(request) 
        print("Response", game_turn_response_string(response))
        return response

# server methods for creating responses

def create_game_state_response(map_plan, scoreBoard, players_scores, info):
    rp = GameStateResponse()
    rp.MapPlan = map_plan
    rp.ScoreBoard = scoreBoard
    rp.PlayerScore.extend(players_scores)
    rp.Info = info
    return rp

def create_game_turn_response(accepted, debug_dump):
    rp = GameTurnResponse()
    rp.Accepted = accepted
    rp.DebugDump = debug_dump
    return rp

# client methods for creating requests

def create_game_state_request(player_id, get_state):
    rq = GameStateRequest()
    rq.PlayerId = player_id
    rq.GetState = get_state
    return rq

def create_game_turn_request(player_id, debug_dump, voice_data):
    rq = GameTurnRequest()
    rq.PlayerId = player_id
    rq.DebugDump = debug_dump
    rq.VoiceData = voice_data
    return rq

# Client Message Spamer
def game_state_request(stub, request):
        # print(game_state_request_to_string(request))
        # Call the service through the stub object.
        response = stub.RequestStateUpdate(request)
        print(game_state_reduced_response_to_string(response))
        return response
def game_turn_request(stub, request):
        print(game_turn_request_to_string(request))
        # Call the service through the stub object.
        response = stub.RequestTurn(request)
        print(game_turn_response_string(response))
        return response