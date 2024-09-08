import mesa
import random
import numpy as np
import matplotlib.pyplot as plt

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

class SugarscapeG1mt(mesa.Model):
    '''
    model class to manage sugarscape with traders (g1mt)
    from Growing Artificial Societies - Axtell and Epstien
    '''
    def __init__(self, width = 50, height = 50, initial_population = 200, endowment_min = 25, endowment_max = 50, metabolism_min = 1, metabolism_max = 50, vision_min=1, vision_max=50):

        super().__init__()
        self.width = width
        self.height = height
        self.initial_population = initial_population
        self.endowment_min = endowment_min
        self.endowment_max = endowment_max
        self.metabolism_min = metabolism_min
        self.metabolism_max = metabolism_max
        self.vision_min = vision_min
        self.vision_max = vision_max

        self.grid = mesa.space.MultiGrid(width, height, torus=False)
        self.schedule = mesa.time.RandomActivationByType(self)
        self.agent_id = 0
        self.populate_resources()
        self.generate_traders()

    def populate_resources(self):
        self.sugar_distribution = np.genfromtxt('data/sugar-map.txt')
        self.spice_distribution = np.flip(self.sugar_distribution, axis=1)

        for _, x, y in self.grid.coord_iter():
            for resource, resource_class in zip([self.sugar_distribution, self.spice_distribution], [Sugar, Spice]):
                max_amount = resource[x, y]
                if max_amount == 0:
                    continue
                resource_instance = resource_class(self.agent_id, self, (x, y), max_amount)
                self.grid.place_agent(resource_instance, (x, y))
                self.schedule.add(resource_instance)
                self.agent_id += 1
    
    def generate_traders(self):
        for i in range(self.initial_population):

            sugar = int(random.uniform(self.endowment_min, self.endowment_max))
            spice = int(random.uniform(self.endowment_min, self.endowment_max))
            metab_sugar = int(random.uniform(self.metabolism_min, self.metabolism_max))
            metab_spice = int(random.uniform(self.metabolism_min, self.metabolism_max))
            vision = int(random.uniform(self.vision_min, self.vision_max))
            posn = (np.random.randint(0, self.width), 
                    np.random.randint(0, self.height))
            trader = Trader(self.agent_id, 
                            self,
                            posn,
                            sugar = sugar,
                            spice = spice,
                            metabolism_sugar = metab_sugar,
                            metabolism_spice = metab_spice,
                            vision = vision)
            self.grid.place_agent(trader, posn) 
            self.schedule.add(trader)
            self.agent_id += 1
            print(trader.unique_id, trader.sugar, trader.metabolism_spice)


model = SugarscapeG1mt()

apple = 1