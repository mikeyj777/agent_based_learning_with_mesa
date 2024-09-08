import mesa

class Trader(mesa.Agent):
    # trader has a metabolism (processes sugar and spice per turn)
    # harvest sugar and spice
    def __init__(self, unique_id, model, pos, moore=False, sugar=0, spice=0, metabolism_sugar=0, metabolism_spice=0, vision=0):
        super().__init__(unique_id, model)
        
        self.pos = pos
        self.moore = moore
        self.sugar = sugar
        self.spice = spice
        self.metabolism_sugar = metabolism_sugar
        self.metabolism_spice = metabolism_spice
        self.vision = vision
    
    def move(self):
        # print(f'I am agent {self.unique_id}, currently at {self.pos}.  I am about to move.')
        if self.model.grid.is_cell_empty(self.pos):
            self.model.grid.place_agent(self, self.pos)
        else:
            self.model.grid.move_agent(self, self.pos)
