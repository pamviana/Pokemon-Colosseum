class Pokemon:
    pokemon_types = ["Normal", "Fire", "Water", "Electric", "Grass"]

    def __init__(self, name, pokemon_type, hp, attack, defense, moves):
        self.name = name
        self.pokemonType = pokemon_type
        self.HP = int(hp)
        self.attack = int(attack)
        self.defense = int(defense)
        self.Moves = create_moves_list(moves)


def create_moves_list(moves):
    split_moves = moves.replace('[', "").replace(']', "").strip().split(',')
    moves_to_ignore = ["Baby'Doll Eyes", "Double'Edge", "Mud'Slap", "Self'Destruct"]
    moves_list = []

    for move in split_moves:
        move = move.strip(" \" ").strip(" \' ").strip()
        if not moves_to_ignore.__contains__(move):
            moves_list.append(move)

    # Remove some characters that weren't added to moves.csv
    return [move.strip(" \' ").strip(" \" ").strip() for move in split_moves]
     

