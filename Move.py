class Move:

    def __init__(self, name, move_type, pp, power):
        self.name = name
        self.move_type = move_type
        self.PP = int(pp)
        self.power = int(power)
