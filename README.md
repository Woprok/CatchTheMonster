# Chase the Monster
## Presentation of final product
https://www.youtube.com/watch?v=OiRv9CB3fuo

## Description
Chase the Monster is simple client - server game for "any" amount of players.  
Player aim for achieving high score by chasing monsters around the labyrinth using voice commands.  
There is no win or lose, once server run your only objective is to get as many point's as possible on leaderboard.  

## Requirements 
This application requires for use & development: Protocol Buffers, gRPC, Google Cloud Api, PyAudio
### Protocol Buffers
Follow instructions at https://github.com/protocolbuffers/protobuf
Troubleshoot using google, actually a lot of google might be required...
Compiling proto files to python source code requires C++ version of the library as well.
### gRPC
Follow instructions at https://github.com/grpc/grpc
Troubleshoot using google, actually a lot of google might be required...
Compiling proto files to python source code requires C++ version of the library as well.
### Google Cloud Api
Application uses Google Cloud Api https://cloud.google.com/
Register and create project that enables speech api and translation api. 
Download credentials, they are required by server. 
> Open & create account (it has free limits) https://cloud.google.com/   
> A. New project   
> B. Api & Services -> Enable Apis and Services  
>> 1. search, select, enable Cloud Speech-to-Text API  
>> 2. search, select, enable Cloud Translation API  
>> 3. search, select, enable Compute Engine API  
> C. Credentials  
>> 1. Create credentials -> Create API key  
>> 2. Create credentials -> Create service account (Role: owner)  
>> 3. Manage service account -> Actions -> Create key -> Choose JSON  
> D. Home -> Select project -> See Project Info from dashboard page of project for Project ID  
Get current version from github and compile it as following:
```
git clone http://github.com/googleapis/googleapis.git
cd googleapis
make OUTPUT=.. LANGUAGE=python GRPCPLUGIN=$(pkg-config --variable=prefix grpc++)/bin/grpc_python_plugin
cd ..
```
### PyAudio
For more informations: https://people.csail.mit.edu/hubert/pyaudio/
Required for voice capture commands...
```
sudo apt-get install libasound-dev portaudio19-dev libportaudio2 libportaudiocpp0
sudo apt-get install ffmpeg libav-tools
pip install wheel
sudo apt install python3-dev
pip install pyaudio
```
or
```
sudo apt-get install python3-pyaudio
```
or for windows this might work
```
pip install pipwin
pipwin install pyaudio
```
That should be all related to installing necessary libraries...
## Instructions (compilation and running)
Both server and client use secure communication, due to this they require credentials.
It is enough to use openssl to generate new credentials.
```
openssl req -newkey rsa:4096 -nodes -keyout server.key -x509 -days 365 -out server.crt
```
They can be viewed for example with...
```
openssl x509 -in server.crt -text
openssl rsa -in server.key -text
```
Then you are required to compile all proto files used by this application...
```
protoc --plugin=protoc-gen-grpc=$(pkg-config --variable=prefix grpc++)/bin/grpc_python_plugin --python_out="." --grpc_out="." protos/*.proto
```
Afterwards you can use venv to get all other required packages...
```
python -m venv .venv 
. .venv/bin/activate
pip install -r requirements.txt
```
These two might be helpful if you are using windows:
```
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
```
### Running server
```
./execute_server.py
```
### Running player client
```
./execute_client.py
```
### Running web presentation client
```
Open url in browser composed from web_adress:web_port, which are defined in the configuration file.
```
### Running tests
```
./execute_tests.py
```
### Cfg example and description
Share by both client and server. Most values are used only by server.  
```
    "server_address": "localhost:8888", # grpc server ip and port configuration.   
    "web_address" : "localhost" # defines ip address used by WebService.   
    "web_port" : "5001" # defines port used by WebService.   
    "cloud_account": "account.json", # see Google Cloud Api, this is private and can't be shared.   
    "cloud_project": "text-text-numbers", # see Google Cloud Api, this is private and can't be shared.   
    "cloud_location": "global", # keep this value as other might not work with all cloud api.  
    "target_language": "sk_SK", # change to whatever language you want to play in.  
    "source_language": "en_US", # do not change this value, or voice commands will no longer work.  
    "capture_time": "4", # in seconds, used by client to create voice capture window.  
    "turn_time": "10", # in seconds, defines length of single turn, lower value to reduce waiting time between turns.  
    "certificate_key": "server.key", # see Instructions for creating basic self signed certificate   
    "certificate_crt": "server.crt", # see Instructions for creating basic self signed certificate.  
    "map_data_key": "map.data" # create your own map, for description of file format see map documentation.  
```
### Dev Documentation
Client - Server game for "any" amount of players using Cloud to process voice input and than transforming transcribed text to game command.  

#### Diagram 
See CatchTheMonster_Diagram.png (simplified mix between component & connector and decomposition viewpoints) for overview of components. That should be enough to understand it un big picture.  

#### Tests
Three tests are provided (catch_game, audio_capture, configuration_provider) each can be used to run small part of application and verify that it works as expected.  
Unit/integration/... tests were not written and should be considered, if you plan to do extensive modifications...  

#### Client
Client starting point is defined in execute_client.py  
> Loads configuration and creates instance of ClientManager that continues execution. 
ClientManager is defined in libs/client_manager.py
> Initializes all grpc client services and provides functionality for capturing inputs for the game by using AudioCapturer.    
> Most terminals are uncapable of correctly displaying emoji, and due to that WebClient is required. Otherwise turn_game_processor function could be used to display map...
AudioCapturer is defined in libs/audio_capturer.py
> Wrapper around pyAudio and primarily provides function to capture single voice command (microphone input). 
#### WebClient & WebService (part of server)
WebClient is defined in libs/templates/index.html  
> Current functionality is just displaying received string from server. String received from server represent's whole game state.  
WebService is defined in libs/web_service.py  
> Defines interface used by WebClient and internally depands on current GameStateManager to get current map state.  
> It's wrapper around Flask.  
#### Server
Server starting point is defined in execute_server.py  
> Loads configuration and creates instance of CloudManager and then creates instance of ServerManager, which continues execution.  
CloudManager is defined in libs/cloud_manager.py
> Provides functionality for translating text and transcribing voice, using Google Cloud Api.   
ServerManager is defined in libs/server_manager.py
> Initializes all grpc server services and links all necessary dependencies between internal objects such as GameStateManager.   
GameStateManager is defined in libs/game_state_manager.py
> Provides functionality for creating CatchGame, registring new player, controlling game loop flow of CatchGame and processing player input for CatchGame by transcribing voice and translating it using Google Cloud Api.    
#### Grpc Services  
Defined in:  
> grpc_game_services.py  
> grpc_time_services.py  
> grpc_login_services.py   
Each provides client stub and server service implementation.   
Other functionality creating correct proto objects and converting proto objects to displayable string.   
#### Configuration
ConfigurationProvider is defined in configuration_provider.py  
>  All configuration used by client, server and cloud is defined in single file. ConfigurationProvider handles creating default cfg file and loading it.
#### CatchGame
CatchGame is defined in catch_game.py
> Labyrinth class is responsible for all game logic calls.   
>> Such as: Loading (load_from_file) and creating map (load_map, create_map_tile).  
>> Spawning and despawning creatures. (spawn_player/missing, unspawn)
>> Managing movement of creatures on map. (process_human/monsters_turn)  
>> update_game method is used to simulate one turn.
> Class Tile and derivated classes are representing objects on the map. 
>> Creature Tile is interface for creatures. 
>> BorderTile, LandTile, WaterTile, MountainTile, FlyingTile represent's a background/map.

### User Documentation  
For running you might have to run your own server:
 - Run Server (requires certificate and google cloud account, see instructions for more informations),   
Once you have server you can connect to:
 - Run Webclient (open webpage with server flask ip & port),   
> Displays current state of game.
 - Run Client (specify server ip & port, certificate used by server in configuration file)
> Required for playing the game.

Once client is running it will ask for username and avatar.
Username  
> insert anything  
Avatar  
> leave empty or type/paste emoji (terminal support required) (https://unicode.org/emoji/charts/full-emoji-list.html)    

Gameplay:  
Webclient displays time until start of the next turn.  
Player can by using client at any time send a command to a server.  
Last command is used in case multiple command would be send before start of next turn. (This should not happen in default configuration, only with shorter voice capture times.)

Command description:
Client in periodic intervals enables voice capture for a command. This is displayed by message written to console by client.  
> Starting recording... (from this point captures voice input)  
> Finishing recording... (end of capturing, start of processing)  
> Turn accepted... (displays what was captured and will be used as next command...)  

Following command words are recognized by server and can be used to move your avatar around the map:  
There are two categories, move type and move direction. Both of them are required to create a move.    
Move types: walk, swim, climb, fly. (Last value in transcribed text is used.) 
> Moving through different tiles requires specific move type: (walk - free land), (swim - water), (climb - land obstacle), (fly - fly obstacle)
Move direction: up, down, left, right (All values entered are used. up + down would result in no movement as they block each other. up + left will move player to upper left position from his current)  

Correct pronunciation is required and it might require multiple attempts to figure out how to say it correctly in different languages.
See Dictionary.txt for Slovak translation. Commands in slovak would be for example: "plávať hore", which will be processed as "swim up" and will cause player avatar to move up, if tile above his current position is water.  

Now you can go catch monsters by going one cell within them.  

### Map Documentation
Initialize map of labyrinth from the file specified in configuration by default "map.data"
File structure for map file is:   
>x - width of the map (single number on the line)     
>y - height of the map (single number on the line)  
>Land_Mobs_Spawn_Count - amount of land mobs that can be spawned on the map (single number on the line)  
>Water_Mobs_Spawn_Count - amount of water mobs that can be spawned on the map  (single number on the line)  
>Fly_Mobs_Spawn_Count - amount of fly mobs that can be spawned on the map  (single number on the line)  
>Map_Plan - "y" lines with "x" symbols per line. Each symbol represent's one on the map. Following symbols are allowed:     
>>X (Border around the map)  
>>O (Obstacle for land and water mobs, player has to climb)  
>>S (Obstacle for fly mob, player has to fly)  
>>W (Water, player has to swim)  
>>. (or any other symbol that is not registred is free land, player has to walk)  
