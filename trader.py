import math
import mesa

import helpers
from resources import *

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
    
    def eat(self):
        sugar_patch = self.get_sugar(self.pos)
        if sugar_patch is not None:
            self.sugar += sugar_patch.amount
            sugar_patch.amout = 0
        self.sugar -= self.metabolism_sugar
        self.sugar = max(0, self.sugar)

        spice_patch = self.get_spice(self.pos)
        if spice_patch is not None:
            self.spice += spice_patch.amount
            spice_patch.amout = 0
        self.spice -= self.metabolism_spice
        self.spice = max(0, self.spice)

    def is_starved(self):
        return (self.sugar <= 0) or (self.spice <= 0)

    def maybe_die(self):
        '''
        fxn to remove traders who have consumed all of their sugar or spice
        '''
        # print(f'checking if trader {self.unique_id} should die.  current sugar: {self.sugar}, spice: {self.spice}')
        if self.is_starved():
            traders_before_pruning = self.model.schedule.get_type_count(Trader)
            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)

            # print(f'Trader {self.unique_id} died.  initial number of traders: {traders_before_pruning}.  current number of traders:  {self.model.schedule.get_type_count(Trader)}')
            apple = 1

    def get_trader(self, pos):
        this_cell = self.model.grid.get_cell_list_contents(pos)
        for a in this_cell:
            # check if it's occupied by another trader
            if isinstance(a, Trader):
                return a

        return None

    def trade_with_neighors(self):
        '''
        1. identify neighbors
        2. trade (2 sessions)
        3. collect data
        
        '''

        # 1. identify neighbors
        neighbor_agents = [self.get_trader(pos) for pos in 
                           self.model.grid.get_neighborhood(self.pos, self.moore, False, self.vision)
                           if self.is_occupied_by_other(pos)
                           ]
        # 2. trade
        for neighbor in neighbor_agents:
            # 3. collect data
            pass

    def is_occupied_by_other(self, pos):
        if pos == self.pos:
            # agent can stay in same spot.  not considered occupied
            return False
        this_cell = self.model.grid.get_cell_list_contents(pos)
        for a in this_cell:
            # check if it's occupied by another trader
            if isinstance(a, Trader):
                return True
        
        return False

    def calculate_welfare(self, sugar, spice):
        '''
        part 2. of self.move()
        cobb-douglas function 
        '''
        # calc cobb-douglas
        total = self.metabolism_sugar + self.metabolism_spice
        return sugar**(self.metabolism_sugar/total) * spice**(self.metabolism_spice/total)
    
    def get_sugar(self, pos):
        '''
        helper for part 2 of move.
        also in self.eat()
        '''
        this_cell = self.model.grid.get_cell_list_contents(pos)
        for agent in this_cell:
            if type(agent) is Sugar:
                return agent
        return None

    def get_spice(self, pos):
        '''
        helper for part 2 of move.
        '''
        this_cell = self.model.grid.get_cell_list_contents(pos)
        for agent in this_cell:
            if type(agent) is Spice:
                return agent
        return None
    
    def get_sugar_amount(self, pos):
        '''
        helper for part 2 of move.
        '''
        sugar_patch = self.get_sugar(pos)
        if sugar_patch:
            return sugar_patch.amount
        return 0

    def get_spice_amount(self, pos):
        '''
        helper for part 2 of move.
        '''
        spice_patch = self.get_spice(pos)
        if spice_patch:
            return spice_patch.amount
        return 0
        

    def move(self):
        '''
        find optimal move in 4 parts
        1.  identify all possible moves
        2.  determine which move maximizes welfare
        3.  find closest best option
        4.  move.
        '''
        # optimal in 4 parts
        # 1. get all neighbors
        
        # all_neighbors = self.model.grid.get_neighborhood(self.pos, self.moore, True, self.vision)
        # available_spots = []
        # for neighor in all_neighbors:
        #     if not self.is_occupied_by_other(neighor):
        #         available_spots.append(neighor)

        neighbors = [i for i in self.model.grid.get_neighborhood(
            self.pos, self.moore, True, self.vision) if not self.is_occupied_by_other(i)
            ]
        
        # 2. det which move maximizes welfare

        welfares = [
            self.calculate_welfare(
                self.sugar + self.get_sugar_amount(pos), 
                self.spice + self.get_spice_amount(pos)) 
            for pos in neighbors
        ]

        # 3. find closest best option

        # link welfare and location
        max_welfare = max(welfares)
        candidate_idxs = [i for i, x in enumerate(welfares) if math.isclose(x, max_welfare, rel_tol=1e-06)]
        

        candidate_positions = [neighbors[i] for i in candidate_idxs]

        distances = [helpers.get_distance(self.pos, pos) for pos in candidate_positions]

        min_dist = min(distances)

        final_candidate_idxs = [i for i, x in enumerate(distances) if math.isclose(x, min_dist, rel_tol=1e-02)]  

        final_candidates = [candidate_positions[i] for i in final_candidate_idxs]
        
        self.random.shuffle(final_candidates)

        # 4. move
        # self.model.grid.move_agent(self, final_candidates[0])

        apple = 1
    
