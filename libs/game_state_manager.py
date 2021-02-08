from libs.cloud_manager import *
from libs.grpc_game_services import *
from libs.grpc_login_services import *
from libs.catch_game import *
from threading import Thread, Lock
import time
from datetime import datetime, timedelta

class Player():
    def __init__(self, id, username, avatar):
        self.id = id
        self.username = username
        self.avatar = avatar
        self.character = None
    def set_character(self, player_character):
        self.character = player_character

class GameStateManager():
    """
    Manages whole game on server side.
    """
    def __init__(self, cloud_manager, map_plan_file, turn_timer):
        self.cloud_manager = cloud_manager
        self.players = []
        self.game_instance = Labyrinth()
        # Lock used to synchronize GRPC async demands with game update.
        self.synchronization_game_lock = Lock()
        self.map_plan_file = map_plan_file
        self.turn_time = turn_timer

    def register_player(self, request):
        player = next((x for x in self.players if x.username == request.Username), None)
        if player != None:
            print(f'Old player rejoined: {player.avatar} -> {request.Avatar}')
            # We are updating player character entity as well, to reflect new avatar
            with self.synchronization_game_lock:
                player.avatar = request.Avatar
                player.character.symbol = request.Avatar
        else:
            print(f'New player joined: {request.Username} {request.Avatar}')
            player = Player(len(self.players), request.Username, request.Avatar)
            # Only this action must be synchronized in this branch
            with self.synchronization_game_lock:
                pc = self.game_instance.spawn_player(player.avatar, player.username, player.id)
            player.set_character(pc)
            self.players.append(player)
        return login_generate_response(request, player.id)
    
    #
    def get_game_state_data(self):        
        """
        Return values are in order Map_Plan, Leaderboard_Header, Player_Scores[], Turn_Counter
        All these values might change and we want them from one time, so this call uses lock.
        """
        with self.synchronization_game_lock:
            plan = self.game_instance.get_current_map()
            lb = self.game_instance.get_leaderboard()
            pcs = self.game_instance.get_scores()
            turnstart = self.turn_time - (datetime.now() - self.loop_iteration_time).total_seconds() 
        return (plan, lb, pcs, f'Next turn starts in cca: {turnstart:.1f} seconds')

    def on_game_state_request(self, request = None):
        sd = self.get_game_state_data()
        return create_game_state_response(sd[0], sd[1], sd[2], sd[3])
    
    def cloud_analysis(self, id, voice_data):
        voice_text = self.cloud_manager.transcribe(voice_data)
        if voice_text == None:
            return None
        print(f'Transcribed text {id}: {voice_text}')
        translated_text = self.cloud_manager.translate(voice_text)
        if translated_text == None:
            return None
        print(f'Translated text {id}: {translated_text}')
        return translated_text

    def on_game_turn_request(self, request):
        cloud_result = self.cloud_analysis(request.PlayerId, request.VoiceData)
        if cloud_result != None: # process as move, even if not possible
            move = PlayerMove(cloud_result)
            player = next((x for x in self.players if x.id == request.PlayerId), None)
            if player != None and player.character != None:
                with self.synchronization_game_lock:
                    player.character.store_move(move)
            else:
                cloud_result = "Invalid input. (No player recognized ?)"
        else: # otherwise notify user of failure.
            cloud_result = "Invalid input. (No voice record ?)"

        return create_game_turn_response(True, cloud_result)

    def initialize_game(self):
        """
        Basic initialization of the game and start of turn loop.
        """
        print(f'Initializing game instance with: {self.map_plan_file}')
        self.game_instance.load_from_file(self.map_plan_file)
        self.game_instance.spawn_missing()
        print('Printing initialized game')
        print(self.game_instance.get_current_map())
        print(self.game_instance.get_leaderboard())
        for pc in self.game_instance.get_scores():
            print(pc)
        self.start_loop()

    def continuous_game_loop(self):
        """
        Loop running in new thread, that periodically executes player moves and updates game state.
        """
        while self.is_executing_loop == True:
            time.sleep(self.loop_sleep_length)
            last_turn = 0
            # update must be done in synchronized access, otherwise we could create race conditions
            with self.synchronization_game_lock:
                self.game_instance.update_game()
                self.loop_iteration_time = datetime.now()
                last_turn = self.game_instance.turn_count
            print(f'New turn started: {last_turn}')

    def start_loop(self):
        """
        Start new thread with a infinity loop. Define all loop related values here.
        """
        self.is_executing_loop = True
        self.loop_iteration_time = datetime.now()
        self.loop_sleep_length = self.turn_time 
        self.loop_thread = Thread(target = self.continuous_game_loop)
        self.loop_thread.daemon = True
        self.loop_thread.start()