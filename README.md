# Chase the Monster
## Presentation of final product
https://www.youtube.com/watch?v=OiRv9CB3fuo

## Description
Chase the Monster is simple client - server game for questionable amount of players.
Player aim for achieving high score by chasing monsters around the labyrinth.
There is no win or lose, once server run your only objective is to get as many point's as possible on leaderboard.

## Requirements 
This application requires for use & development: Protocol Buffers, gRPC, Google Cloud Api, PyAudio
### Protocol Buffers
Follow instructions at https://github.com/protocolbuffers/protobuf
Troubleshoot using google, actually a lot of google might be required...
Python requires C++ version as well
### gRPC
Follow instructions at https://github.com/grpc/grpc
Troubleshoot using google, actually a lot of google might be required...
Python requires C++ version as well
### Google Cloud Api
Application uses Google Cloud Api https://cloud.google.com/
Register and create project that enables speech api and translation api.
Download credentials, they are required by server.
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
basically just figure it out yourself...
## Instructions
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
Afterwards you can use venv to get requirements...
```
python -m venv .venv 
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
. .venv/bin/activate
pip install -r requirements.txt
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
Open following url in browser: http://localhost:5000/
Note: it's using flask, to run it on other url please see flask documentation and edit code accordingly.
This exists only for purpose of testing it at localhost...
Extending this part should be trivial if you spent few hours learning flask...
```
### Running tests
```
./execute_tests.py
```
### Cfg example and description
```
{
    "server_address": "localhost:8888", # grpc server cfg
    "cloud_account": "account.json",
    "cloud_project": "text-text-numbers",
    "cloud_location": "global",
    "target_language": "sk_SK", # change to whatever language you want to play in
    "source_language": "en_US", # don't change, it's dependant on it, originally planned to be used on client
    "capture_time": "4", # in seconds
    "turn_time": "10", # in seconds
    "certificate_key": "server.key",
    "certificate_crt": "server.crt",
    "map_data_key": "map.data" # create your own map, for description see catch_game.py or map documentation
}
```
### Dev Short Documentation
See CatchTheMonster_Diagram.png (simplified mix between component & connector and decomposition viewpoints) and source code...  
Client - Server application that uses GRPC for communication.  
Webclient - Server uses Flask for communication  
Cloud is part of Google Cloud Services...  

Short test apps are localed it tests and should be used for extended debuging of smaller parts of whole software...  

configuration_provider.py -> handles loading configuration.  
client_manager.py -> holds all components of client and provides simple voice capture and sending to server logic.   
server_manager.py -> holds all components of server.  
cloud_manager.py -> handles google api communication for transcribe and translate.  

grpc_*_services.py -> holds specific code for services.  

catch_game.py -> holds all game logic and entity definitions. All entities are derived from class Tile. Creature Tile is interface for creatures. Labyrinth class is responsible for all game logic calls.  

game_state_manager.py -> holds all responsibility on server for managing the game and preventing race conditions...  

audio_capturer.py -> simple use of pyAudio for recording microphone input.  

web_service.py -> simple service that ask for current game state.  

execute_client, execute_server -> program starting points  

### User Documentation
Run Server (create certificate and google cloud account (get project_id and account credentials in form of account.json)), Webclient (open webpage with server ip), Client  

Client will ask for username, type something...  
Client will ask for emoji, leave empty or type emoji if your terminal can handle it (https://unicode.org/emoji/charts/full-emoji-list.html)  
Then use following commands to move your avatar around the map:  
Move type (one): climb(land obstacle), fly(fly obstacle), walk(free land), swim(water)  
Move direction (one or two): up, down, left, right  
Now go fetch me some monsters by going one cell within them.  

### Map Documentation
Initialize map of labyrinth from the file  
File structure is:  
>Width == x  
>Height == y  
>Land_Mobs_Spawn_Count  
>Water_Mobs_Spawn_Count  
>Fly_Mobs_Spawn_Count  
>x * y map plan with symbols:   
>>X (Border around the map)  
>>O (Obstacle for land and water mobs, player has to climb)  
>>S (Obstacle for fly mob, player has to fly)  
>>W (Water, player has to swim)  
>>. (or any other symbol that is not registred is free land, player has to walk)  
