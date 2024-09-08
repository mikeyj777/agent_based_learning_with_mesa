import mesa

# resource classes
class Sugar(mesa.Agent):
    # increase sugar by one unit per round
    # contains an amount of sugar
    def __init__(self, unique_id, model, pos, max_sugar):
        super().__init__(unique_id, model)
        self.pos
        self.amount = max_sugar
        self.max_sugar = max_sugar
        

class Spice(mesa.Agent):
    # increase spice by one unit per round
    # contains an amount of spice
    def __init__(self, unique_id, model, pos, max_spice):
        super().__init__(unique_id, model)
        self.pos = pos
        self.amount = max_spice
        self.max_spice = max_spice
