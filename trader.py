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
        '''
        this_cell = self.model.grid.get_cell_list_contents(pos)
        for agent in this_cell:
            if type(agent) is Sugar:
                # print(f'Sugar {agent.amount} at {agent.pos}')
                return agent
        return None

    def get_spice(self, pos):
        '''
        helper for part 2 of move.
        '''
        this_cell = self.model.grid.get_cell_list_contents(pos)
        for agent in this_cell:
            if type(agent) is Spice:
                # print(f'Spice {agent.amount} at {agent.pos}')
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
        # print(f'I am agent {self.unique_id}, currently at {self.pos}.  I am about to move.')
        '''
        find optimal move in 4 parts
        1.  identify all possible moves
        2.  determine which move maximizes welfare
        3.  find closest best option
        4.  move.
        '''
        # optimal in 4 parts
        # 1. get all neighbors
        print('\n--------------------\n')
        
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

        final_candidates = [i for i, x in enumerate(distances) if math.isclose(x, min_dist, rel_tol=1e-02)]  

        print(f'min_dist: {min_dist}.  final_candidates: {final_candidates}.  ')
        
        self.random.shuffle(final_candidates)

        # 4. move
        # self.model.grid.move_agent(self, final_candidates[0])

        apple = 1