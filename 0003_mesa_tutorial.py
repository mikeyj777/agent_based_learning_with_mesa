import mesa
import random
import numpy as np
import matplotlib.pyplot as plt
from resources import *
from trader import Trader
        
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
                resource_instance = resource_class(self.get_agent_id(), self, (x, y), max_amount)
                self.grid.place_agent(resource_instance, (x, y))
                self.schedule.add(resource_instance)
    
    def generate_traders(self):
        for i in range(self.initial_population):

            sugar = int(random.uniform(self.endowment_min, self.endowment_max+1))
            spice = int(random.uniform(self.endowment_min, self.endowment_max+1))
            metab_sugar = int(random.uniform(self.metabolism_min, self.metabolism_max+1))
            metab_spice = int(random.uniform(self.metabolism_min, self.metabolism_max+1))
            vision = int(random.uniform(self.vision_min, self.vision_max+1))
            posn = (np.random.randint(0, self.width), 
                    np.random.randint(0, self.height))
            trader = Trader(self.get_agent_id(), 
                            self,
                            posn,
                            sugar = sugar,
                            spice = spice,
                            metabolism_sugar = metab_sugar,
                            metabolism_spice = metab_spice,
                            vision = vision)
            self.grid.place_agent(trader, posn) 
            self.schedule.add(trader)
            print(trader.unique_id, trader.sugar, trader.metabolism_spice)

    def get_agent_id(self):
        id = self.agent_id
        self.agent_id += 1
        return id
    


model = SugarscapeG1mt()

apple = 1