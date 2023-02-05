from Pokemon import Pokemon
from Move import Move
import math
import random
import numpy as np
import csv

# Global Variables
type_matchup_table = {
    "Normal": {"Normal": 1, "Fire": 1, "Water": 1, "Electric": 1, "Grass": 1},
    "Fire": {"Normal": 1, "Fire": 0.5, "Water": 0.5, "Electric": 1, "Grass": 2},
    "Water": {"Normal": 1, "Fire": 2, "Water": 0.5, "Electric": 1, "Grass": 0.5},
    "Electric": {"Normal": 1, "Fire": 1, "Water": 2, "Electric": 0.5, "Grass": 0.5},
    "Grass": {"Normal": 1, "Fire": 0.5, "Water": 2, "Electric": 1, "Grass": 0.5}
}

rocket_team = []
player_team = []
pokemon_lookup = {}
move_lookup = {}


def create_pokemon_lookup():
    try:
        f = open('pokemon-data.csv', 'r')
    except IOError:
        print('Cannot open pokemon-data.csv')
    data_lines = csv.reader(f)

    # skip header
    next(data_lines)

    for line in data_lines:
        pokemon = Pokemon(line[0], line[1], line[2], line[3], line[4], line[7])
        pokemon_lookup[pokemon.name] = pokemon

    f.close()
    return pokemon_lookup


def create_moves_lookup():
    moves_lookup = {}

    try:
        f = open('moves-data.csv', 'r')
    except IOError:
        print('Cannot open pokemon-data.csv')
    data_lines = csv.reader(f)

    # skip header
    next(data_lines)

    for line in data_lines:
        move = Move(line[0], line[1], line[4], line[5])
        moves_lookup[move.name] = move

    f.close()
    return moves_lookup


def get_stab(pokemon_a, move):
    if pokemon_a.pokemonType == move.move_type:
        return 1.5
    else:
        return 1


def get_type_efficiency(move, pokeb_type):
    if not type_matchup_table.__contains__(move_lookup[move].move_type):
        return 1
    else:
        return type_matchup_table[move_lookup[move].move_type][pokeb_type]


def calculate_damage(move, pokemon_a, pokemon_b):
    pb = pokemon_lookup[pokemon_b]
    pa = pokemon_lookup[pokemon_a]
    move_a = move_lookup[move]

    random_value = random.choice([0.5, 0.6, 0.7, 0.8, 0.9, 1.0])

    return math.ceil(move_a.power * (pa.attack / pb.defense) * get_stab(pa, move_a) *
                     get_type_efficiency(move, pb.pokemonType) * random_value)


def create_teams(player_name):
    # creates a list of 6 Pokemon. "replace= False" ensures that it only retrieves unique items
    random_pokemons = np.random.choice(list(pokemon_lookup.keys()), 6, replace=False).tolist()

    global rocket_team
    global player_team

    # Split the array in 2 teams. First 3 are Rocket Team's Pokémon, and last 3 are Player Team's Pokémon
    for r in range(3):
        rocket_team.append(random_pokemons.pop())
    for p in range(3):
        player_team.append(random_pokemons.pop())

    print("\nRocket's team :")
    print(rocket_team)
    print("\n" + player_name + "'s team :")
    print(player_team)


def get_rocket_move(moves):
    move = random.choice(moves)
    return move


def get_player_move(available_moves, pokemon, player_name, moves):
    i = 1
    acceptable_inputs = []
    is_input_wrong = 1

    # If player runs out of moves, it makes all the moves available again
    if len(available_moves) == 0:
        available_moves = moves

    print("\nChoose the move for " + pokemon + ":")

    # This for loop displays the moves and creates an array with the numbers that are acceptable as an input.
    # For example, if there are 5 moves, only the inputs 1 to 5 will be accepted.
    # Therefore, acceptable_inputs = [1,2,3,4,5]
    for move in available_moves:
        print(str(i) + ". " + move.strip())
        acceptable_inputs.append(str(i))
        i += 1

    while is_input_wrong:
        player_input = input("Team " + player_name + "'s choice: ")

        if not acceptable_inputs.__contains__(player_input):
            print("Input " + player_input + " is not valid")
        else:
            is_input_wrong = 0

    return available_moves[int(player_input) - 1]


def player_turn(teams_lookup, teams, player_name, pokemon_lookup_copy):
    print("============================================")
    print("Turn: Team " + teams[0] + " with " + str(teams_lookup[teams[0]]))

    pokemon_defending = teams_lookup[teams[1]][0]
    pokemon_attacker = teams_lookup[teams[0]][0]

    available_moves = pokemon_lookup[teams_lookup[teams[0]][0]].Moves
    if teams[0] == "Rocket":
        move = get_rocket_move(available_moves)
    else:
        move = get_player_move(available_moves, teams_lookup[player_name][0], player_name,
                               pokemon_lookup_copy[teams_lookup[player_name][0]].Moves)
    pokemon_lookup[teams_lookup[teams[0]][0]].Moves.remove(move)

    poke_def_obj = pokemon_lookup[pokemon_defending]
    poke_atck_obj = pokemon_lookup[pokemon_attacker]

    damage = calculate_damage(move, pokemon_attacker, pokemon_defending)

    print("\nAttacker: " + pokemon_attacker + " [" + str(poke_atck_obj.HP) + " HP]")
    print("Defender: " + pokemon_defending + " [" + str(poke_def_obj.HP) + " HP]")
    print("Move: " + move)

    print("Damage= " + str(damage))

    poke_def_obj.HP = poke_def_obj.HP - damage
    print(pokemon_defending + "'s new HP: " + str(poke_def_obj.HP))

    # Pop pokemon from queue if its HP is less or equal than 0.
    if poke_def_obj.HP <= 0:
        print("\n" + poke_def_obj.name + " faints back to pokeball =(")
        teams_lookup[teams[1]].pop(0)
    print("============================================\n")


def main():
    print("-----------------------------\nWelcome to Pokemon Colosseum!\n-----------------------------\n")

    # Load data
    global pokemon_lookup
    global move_lookup
    is_name_acceptable = 1

    move_lookup = create_moves_lookup()
    pokemon_lookup = create_pokemon_lookup()
    pokemon_lookup_copy = pokemon_lookup.copy()

    while is_name_acceptable:
        player_name = input("Enter Player Name: ")
        if player_name.upper() == "ROCKET":
            print("\nEnter another player name. " + player_name + " is not acceptable.\n")
        else:
            is_name_acceptable = 0

    create_teams(player_name)
    teams_lookup = {player_name: player_team,
                    "Rocket": rocket_team}
    teams = list(teams_lookup.keys())
    random.shuffle(teams)  # the first item in the list will be the starter

    print("\n--------------- Let the battle begin!!!! ---------------")
    print("\nTeam " + teams[0] + " starts the battle!")
    print("\n--------------------------------------------------------\n")

    while len(teams_lookup[teams[1]]) != 0 and len(teams_lookup[teams[0]]) != 0:
        player_turn(teams_lookup, teams, player_name, pokemon_lookup_copy)

        # This ensures that it changes the turn of who attacks next
        teams = teams[-1:] + teams[:-1]

    # There will be a winner if one team doesn't have any pokemons
    if len(teams_lookup[teams[1]]) != 0:
        winner = teams[1]
    elif len(teams_lookup[teams[0]]) != 0:
        winner = teams[0]

    print("The winner is: " + winner)


if __name__ == "__main__":
    main()
