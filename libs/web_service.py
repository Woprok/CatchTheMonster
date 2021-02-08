from flask import Flask, Response, render_template, url_for
from flask_classful import FlaskView, route
from datetime import datetime
import logging

class Data():
    service = None
    @classmethod
    def get_service(self):
        return self.service    
    @classmethod
    def set_service(self, serv):
        self.service = serv        

class WebService():
    def __init__(self, game_state_manager):
        print("Initializing flask web service")
        self.app = Flask(__name__)
        log = logging.getLogger('werkzeug')
        log.disabled = True
        Data.set_service(game_state_manager)
        GameState.register(self.app, route_base = '/')

    def start_presenting(self):
        self.app.run() #debug=True, threaded=True

class GameState(FlaskView):
    web_service_game_state_provider = None
    """
    Used to present state of the game as console behaviour is extremly volatile when switching to different terminal.
    """
    def generate_state_string(self):
        if Data.get_service() == None:
            yield 'No game in progress right now.'
        state = Data.get_service().get_game_state_data()
        result = state[0]
        result += f'{state[1]}\n'
        for pc in state[2]:
            result += f'{pc}\n'
        result += f'Next turn informations:\n{state[3]}\n'
        yield result

    @route('/State_Update')
    def State_Update(self):
        return Response(self.generate_state_string(), mimetype='text') 

    def index(self):
        """
        Default is at http://localhost:5000/
        """
        return render_template('index.html')