import random
import itertools
import enum

class Tile():
    """
    Abstract interface class
    """
    def __init__(self, x, y):
        """
        Creates tile with X, Y coordinates
        """
        self.x = x
        self.y = y
    def __str__(self):
        return ' '

    def is_empty(self):
        """
        Is this tile currently occupied by something ?
        Some types like border are always unreachable, while other like land are mostly free.
        """
        return False
class BorderTile(Tile):
    """
    Represent's border of the map. Border is never empty.
    """
    def __init__(self, x, y):
        super().__init__(x, y)
    def __str__(self):
        return '⬛' #X
class LandTile(Tile):
    """
    Represent's free land of the map.
    """
    def __init__(self, x, y):
        super().__init__(x, y)
        self.empty = None
    def __str__(self):
        return '🟩' #.
    def is_empty(self):
        return self.empty == None 
    def fill(self, occupier):
        self.empty = occupier
    def free(self):
        self.empty = None

class WaterTile(Tile):
    """
    Represent's water obstacle on the map.
    """
    def __init__(self, x, y):
        super().__init__(x, y)
        self.empty = None
    def __str__(self):
        return '🟦' #W
    def is_empty(self):
        return self.empty == None 
    def fill(self, occupier):
        self.empty = occupier
    def free(self):
        self.empty = None
class MountainTile(Tile):
    """
    Represent's mountain obstacle on the map.
    """
    def __init__(self, x, y):
        super().__init__(x, y)
        self.empty = None
    def __str__(self):
        return '🟫' #O
    def is_empty(self):
        return self.empty == None 
    def fill(self, occupier):
        self.empty = occupier
    def free(self):
        self.empty = None
class FlyingTile(Tile):
    """
    Represent's flying obstacle on the map.
    """
    def __init__(self, x, y):
        super().__init__(x, y)
        self.empty = None
    def __str__(self):
        return '⬜' #S
    def is_empty(self):
        return self.empty == None 
    def fill(self, occupier):
        self.empty = occupier
    def free(self):
        self.empty = None

class CreatureTile(Tile):
    """
    Represent's border of the map.
    """
    def __init__(self, x, y):
        super().__init__(x, y)
        self.age = 0
    def __str__(self):
        return 'C'
    def is_empty(self):
        return False
    def get_age(self):
        return self.age
    def on_survival(self):
        self.age += 1
    def can_move_to(self, x, y, lab):
        """
        Checks if creature can move to selected tile.
        """
        return False
    def desired_move(self, lab):
        """
        Creature desired next move location. 
        Return coordinates.
        Is responsible for executing on_survival()
        """
        self.on_survival()
        return (self.x, self.y)
    def choose_spawn(lab):
        """
        Creature desired spawn location. Return tile/coordinates or None.
        """
        return None
class SkyBeast(CreatureTile):
    """
    Represent's sky monster the map.
    """
    def __init__(self, x, y):
        super().__init__(x, y)
    def __str__(self):
        return '🦅'
    def can_move_to(self, x, y, lab):
        if lab.is_enterable(x, y):
            tile = lab.get_tile(x, y)
            if isinstance(tile, LandTile) or \
               isinstance(tile, WaterTile) or \
               isinstance(tile, MountainTile):
                return True
        return False
    def desired_move(self, lab):
        self.on_survival()
        possible_moves = [
            (self.x + 1, self.y - 1), (self.x + 1, self.y + 0), (self.x + 1, self.y + 1),
            (self.x + 0, self.y - 1), (self.x + 0, self.y + 0), (self.x + 0, self.y + 1),
            (self.x - 1, self.y - 1), (self.x - 1, self.y + 0), (self.x - 1, self.y + 1)]
        random.shuffle(possible_moves)
        for pos in possible_moves:
            if self.can_move_to(pos[0], pos[1], lab):
                return pos
        return (self.x, self.y)
    def choose_spawn(lab):
        return lab.get_spawn(lab.mountains)
class LandBeast(CreatureTile):
    """
    Represent's land monster the map.
    """
    def __init__(self, x, y):
        super().__init__(x, y)
    def __str__(self):
        return '🐀'
    def can_move_to(self, x, y, lab):
        if lab.is_enterable(x, y):
            tile = lab.get_tile(x, y)
            if isinstance(tile, LandTile) or \
               isinstance(tile, WaterTile) or \
               isinstance(tile, FlyingTile):
                return True
        return False
    def desired_move(self, lab):
        self.on_survival()
        possible_moves = [
            (self.x + 1, self.y - 1), (self.x + 1, self.y + 1),
            (self.x + 0, self.y + 0), 
            (self.x - 1, self.y - 1), (self.x - 1, self.y + 1)]
        random.shuffle(possible_moves)
        for pos in possible_moves:
            if self.can_move_to(pos[0], pos[1], lab):
                return pos
        return (self.x, self.y)
    def choose_spawn(lab):
        return lab.get_spawn(lab.lands)
class WaterBeast(CreatureTile):
    """
    Represent's water monster on the map.
    """
    def __init__(self, x, y):
        super().__init__(x, y)
    def __str__(self):
        return '🐙'
    def can_move_to(self, x, y, lab):
        if lab.is_enterable(x, y):
            tile = lab.get_tile(x, y)
            if isinstance(tile, WaterTile):
                return True
        return False
    def desired_move(self, lab):
        self.on_survival()
        possible_moves = [
            (self.x + 1, self.y + 0),
            (self.x + 0, self.y - 1), (self.x + 0, self.y + 0), (self.x + 0, self.y + 1),
            (self.x - 1, self.y + 0)]
        random.shuffle(possible_moves)
        for pos in possible_moves:
            if self.can_move_to(pos[0], pos[1], lab):
                return pos
        return (self.x, self.y)
    def choose_spawn(lab):
        return lab.get_spawn(lab.waters)

class MoveType(enum.Enum):
   Walk = 1
   Swim = 2
   Climb = 3
   Fly = 4

class PlayerMove():
    def __init__(self, text_move):
        """
        I am actually nice to player, so they can type whatever they want...
        We will just create some kind of result from it, not necesary what they wanted,
        when they tried to trolls us. 
            Duplicates are ignored.
            Unkown words are ignored.
        Player can:
        Walk, Swim, Climb, Fly
        in any of the following directions:
        up, down, left, right
        any direction can be combined e.g.:
        up down = don't move
        up left = move to upper left
        """
        self.move_type = None
        self.change_of_y = 0
        self.change_of_x = 0
        words = text_move.split()
        self.parse_type(words)
        self.parse_direction(words)
    def parse_type(self, moves):
        if "walk" in moves:
            self.move_type = MoveType.Walk 
        if "swim" in moves:
            self.move_type = MoveType.Swim
        if "climb" in moves:
            self.move_type = MoveType.Climb
        if "fly" in moves:
            self.move_type = MoveType.Fly
    def parse_direction(self, moves):
        if "up" in moves:
            self.change_of_y -= 1
        if "down" in moves:
            self.change_of_y += 1
        if "left" in moves:
            self.change_of_x -= 1
        if "right" in moves:
            self.change_of_x += 1 

class PlayerTile(Tile):
    """
    Represent's Player on the map.
    """
    def __init__(self, x, y, symbol, username, id):
        super().__init__(x, y)
        self.symbol = symbol
        self.username = username
        self.id = id
        self.last_unsolved_move = None
        self.score = 0.0
        self.age = 0
    def __str__(self):
        return self.symbol
    def is_empty(self):
        return False
    def get_age(self):
        return self.age
    def on_survival(self):
        self.age += 1
    def update_score(self, val):
        self.score += val
    def can_move_to(self, move, lab):
        if lab.is_enterable(self.x + move.change_of_x, self.y + move.change_of_y):
            tile = lab.get_tile(self.x + move.change_of_x, self.y + move.change_of_y)
            if (isinstance(tile, LandTile) and move.move_type == MoveType.Walk) or \
               (isinstance(tile, WaterTile) and move.move_type == MoveType.Swim) or \
               (isinstance(tile, MountainTile) and move.move_type == MoveType.Climb) or \
               (isinstance(tile, FlyingTile) and move.move_type == MoveType.Fly):
                return (tile.x, tile.y)
        return None
    def store_move(self, player_move_data):
        """
        Expects PlayerMove entity
        Checks if human can move to selected tile.
        """
        self.last_unsolved_move = player_move_data

    def get_move(self, lab):
        """
        Player desired move to next location. 
        Return coordinates.
        Is responsible for executing on_survival()
        """
        if self.last_unsolved_move == None:
            return (self.x, self.y)
        result = self.can_move_to(self.last_unsolved_move, lab)
        if result == None:
            return (self.x, self.y)
        self.last_unsolved_move = None
        self.on_survival()
        return result
    def choose_spawn(lab):
        """
        Player desired spawn location. Return tile/coordinates or None.
        Player should spawn always, but that would be annoying to check and harder
        to randomize. So we will try to spawn him on each terrain type.
        """
        spawn = lab.get_spawn(lab.lands)
        if spawn == None:
            spawn = lab.get_spawn(lab.skies)
        if spawn == None:
            spawn = lab.get_spawn(lab.waters)
        if spawn == None:
            spawn = lab.get_spawn(lab.mountains)
        return spawn

class Labyrinth():
    def __init__(self):
        self.width = 0
        self.height = 0
        self.turn_count = 0
        self.land_spawn_count = 0
        self.water_spawn_count = 0
        self.sky_spawn_count = 0
        self.lands = [] # land tiles
        self.waters = [] # water tiles
        self.mountains = [] # mountain tiles
        self.skies = [] # flying tiles
        self.monsters = [] # living monsters
        self.players = [] # players
        self.plan = [[None for x in range(self.width)] for y in range(self.height)]
    def __str__(self):
        current_map = ''
        for y in range(self.height):
            for x in range(self.width):
                if self.plan[y][x].is_empty() or isinstance(self.plan[y][x], BorderTile):
                    current_map += self.plan[y][x].__str__()
                else:
                    current_map += self.find_occupier(x, y).__str__()
            current_map += '\n'
        return current_map
    def find_occupier(self, x, y):
        """
        Find monster or player on searched coordinates or None if not found. 
        """
        for creature in itertools.chain(self.monsters, self.players):
            if creature.x == x and creature.y == y:
                return creature
        return None
    def is_enterable(self, x , y):
        """
        API FOR CREATURES.
        """
        if self.plan[y][x].is_empty():
            return True
        return False
    def get_tile(self, x, y):
        """
        API FOR CREATURES.
        """
        return self.plan[y][x]
    def get_current_map(self):
        """
        Basically just return string representation of the map.
        """
        return self.__str__()
    def load_from_file(self, file):
        """
        Initialize map of labyrinth from the file
        File structure is:
            Width == x
            Height == y
            Land_Mobs_Spawn_Count
            Water_Mobs_Spawn_Count
            Fly_Mobs_Spawn_Count
            x * y map plan with symbols: 
                X (Border around the map)
                O (Obstacle for land and water mobs)
                S (Obstacle for fly mob)
                W (Water)
                . (or any other symbol that is not registred is free land)
        """
        with open(file, 'r', encoding="utf8") as map_data:
            self.width = int(map_data.readline())
            self.height = int(map_data.readline())
            self.land_spawn_count = int(map_data.readline())
            self.water_spawn_count = int(map_data.readline())
            self.sky_spawn_count = int(map_data.readline())
            self.load_map(map_data)
    def load_map(self, map_file):
        self.plan = [[None for x in range(self.width)] for y in range(self.height)]
        for y in range(self.height):
            row = map_file.readline()
            for x in range(self.width):
                self.save_tile(x, y, row[x])
    def create_map_tile(self, x, y, symbol):
        if symbol == 'X':
            return BorderTile(x, y)
        if symbol == 'W':
            water = WaterTile(x, y)
            self.waters.append(water) 
            return water
        if symbol == 'O':
            mountain = MountainTile(x, y)
            self.mountains.append(mountain)
            return mountain
        if symbol == 'S':
            sky = FlyingTile(x, y)
            self.skies.append(sky)
            return sky
        land = LandTile(x, y)
        self.lands.append(land)
        return land      
    def save_tile(self, x, y, symbol):
        self.plan[y][x] = self.create_map_tile(x, y, symbol)
    def get_spawn(self, array):
        choices = [tile for tile in array if tile.is_empty()] 
        if len(choices) == 0:
            return None
        new_spawn = random.choice(choices)
        return new_spawn    
    def water_condition(creature):
        return isinstance(creature, WaterBeast)
    def land_condition(creature):
        return isinstance(creature, LandBeast)
    def sky_condition(creature):
        return isinstance(creature, SkyBeast)
    def assign_to_tile(self, creature, tile):
        """
        Assigns selected creature to tile.
        """
        tile.fill(creature)
        creature.x = tile.x
        creature.y = tile.y
    def unassign_from_tile(self, creature, tile):
        """
        Unassigns selected creature from a tile.
        """
        tile.free()
        creature.x = -1
        creature.y = -1
    def unspawn_creature(self, creature, tile):
        """
        Removes creature from an existance.
        """
        self.unassign_from_tile(creature, tile)
        self.monsters.remove(creature)
        return creature
    def spawn_water(self):
        """
        Extendable beast sub selection for multiple of same type.
        """
        tile = WaterBeast.choose_spawn(self)
        if tile == None:
            return
        beast = WaterBeast(-1, -1)
        self.monsters.append(beast)
        self.assign_to_tile(beast, tile)
    def spawn_land(self):
        """
        Extendable beast sub selection for multiple of same type.
        """
        tile = LandBeast.choose_spawn(self)
        if tile == None:
            return
        beast = LandBeast(-1, -1)
        self.monsters.append(beast)
        self.assign_to_tile(beast, tile)
    def spawn_sky(self):
        """
        Extendable beast sub selection for multiple of same type.
        """
        tile = SkyBeast.choose_spawn(self)
        if tile == None:
            return
        beast = SkyBeast(-1, -1)
        self.monsters.append(beast)
        self.assign_to_tile(beast, tile)    
    def spawn_missing(self):
        for _ in range(self.water_spawn_count - sum(map(Labyrinth.water_condition, self.monsters))):
            self.spawn_water()
        for _ in range( self.land_spawn_count - sum(map(Labyrinth.land_condition, self.monsters))):
            self.spawn_land()
        for _ in range(self.sky_spawn_count - sum(map(Labyrinth.sky_condition, self.monsters))):
            self.spawn_sky()    
    def spawn_player(self, symbol, username, id):
        tile = PlayerTile.choose_spawn(self)
        if tile == None:
            return
        new_player = PlayerTile(-1, -1, symbol, username, id)
        self.players.append(new_player)
        self.assign_to_tile(new_player, tile)
        return new_player
    
    def process_move_creature(self, creature, oldX, oldY):
        tile_position = creature.desired_move(self)
        self.unassign_from_tile(creature, self.plan[oldY][oldX])
        self.assign_to_tile(creature, self.plan[tile_position[1]][tile_position[0]])    
    def process_monsters_turn(self):
        for creature in self.monsters:
            self.process_move_creature(creature, creature.x, creature.y)    
    def try_catch(self, player, monster):
        removed = self.unspawn_creature(monster, self.plan[monster.y][monster.x])
        player.update_score(((self.turn_count // (removed.age + 1)) % (player.age + 1)) + 5)
    
    def player_catch_at(self, player, x, y):
        if self.is_enterable(x, y) == False:
            monster = self.find_occupier(x, y)
            if isinstance(monster, CreatureTile):
                self.try_catch(player, monster)
    def player_catch(self, player, x, y):
        """
        Catch any monster that is located around the player:
        """
        self.player_catch_at(player, x + 1, y + 1)
        self.player_catch_at(player, x + 1, y + 0)
        self.player_catch_at(player, x + 1, y - 1)
        self.player_catch_at(player, x + 0, y + 1)
        self.player_catch_at(player, x + 0, y - 1)
        self.player_catch_at(player, x - 1, y + 1)
        self.player_catch_at(player, x - 1, y + 0)
        self.player_catch_at(player, x - 1, y - 1)
    def process_move_player(self, player, oldX, oldY):
        tile_position = player.get_move(self)
        if tile_position != None:
            self.unassign_from_tile(player, self.plan[oldY][oldX])
            self.assign_to_tile(player, self.plan[tile_position[1]][tile_position[0]])   
            self.player_catch(player, player.x, player.y)

    def process_human_turn(self):
        for player in self.players:
            self.process_move_player(player, player.x, player.y)
            
    def get_leaderboard(self):    
        result = f'Scoreboard at turn {self.turn_count}:' 
        return result
    def get_scores(self):
        """
        print score of each player and age
        """
        result = []
        for pc in self.players:
            result.append(f'{pc.id}:{pc.username}[ {pc.symbol} ] achieved {pc.score} age {pc.age}')
        return result    

    def update_game(self):
        """
        Turn logic is following:
            - Player move
            - Monster move
            - Monster spawn
        """
        self.turn_count += 1
        self.process_human_turn()
        self.process_monsters_turn()
        self.spawn_missing()