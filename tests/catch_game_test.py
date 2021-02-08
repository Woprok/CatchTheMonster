from libs.catch_game import Labyrinth, PlayerMove

import random

def test_print(lab):
    map = lab.get_current_map()
    print(map)
    board = lab.get_scores()
    print(board)
    pc = lab.get_scores()
    for pc in lab.get_scores():
        print(pc)

def test_loading():
    """
    load default map.data
    """
    print('Test loading')
    lab = Labyrinth()
    lab.load_from_file('map.data')
    test_print(lab)
    print('Test completed')
    return lab

def test_spawn(lab):
    """
    test spawn of all missing
    """
    print('Test spawn')
    lab.spawn_missing()
    test_print(lab)
    print('Test completed')

def test_turn_ai_and_players(lab):
    """
    test turn of all creatures
    """
    print('Test turn')
    lab.update_game()
    test_print(lab)
    print("Turn: {}".format(lab.turn_count))
    print('Test completed')

def test_spawn_player(lab):
    """
    test player spawn
    """
    print('Test spawn player')
    pc = lab.spawn_player('🦸', 'Bob the Tester', 0)
    test_print(lab)
    print('Test completed')
    return pc

def all():
    """
    Verify that all parts work as expected
    """
    lab = test_loading()

    for _ in range(1):
        print('🦅🐀🐙')

    test_spawn(lab)

    pc = test_spawn_player(lab)

    while True:
        pc.store_move(PlayerMove(random.choice(['walk left', 'walk up', 'walk down', 'walk right'])))
        test_turn_ai_and_players(lab)
        if input() == '0':
            break