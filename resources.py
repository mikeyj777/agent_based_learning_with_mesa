import mesa

# resource classes
class Sugar(mesa.Agent):
    # increase sugar by one unit per round
    # contains an amount of sugar
    def __init__(self, unique_id, model, pos, max_sugar=0):
        super().__init__(unique_id, model)
        self.pos
        self.amount = max_sugar
        self.max_sugar = max_sugar
    
    def step(self):

        '''
        Sugar grows by one unit per round
        Sugar is consumed if it reaches max
        '''
        self.amount = min(self.amount + 1, self.max_sugar)
        

class Spice(mesa.Agent):
    # increase spice by one unit per round
    # contains an amount of spice
    def __init__(self, unique_id, model, pos, max_spice=0):
        super().__init__(unique_id, model)
        self.pos = pos
        self.amount = max_spice
        self.max_spice = max_spice
    
    def step(self):

        '''
         grows by one unit per round
         is consumed if it reaches max
        '''
        self.amount = min(self.amount + 1, self.max_spice)