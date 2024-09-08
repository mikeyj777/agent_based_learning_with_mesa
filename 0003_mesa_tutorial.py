import mesa
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
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        
class SugarscapeG1mt(mesa.Model):
    '''
    model class to manage sugarscape with traders (g1mt)
    from Growing Artificial Societies - Axtell and Epstien
    '''
    def __init__(self, width = 50, height = 50):
        super().__init__()
        self.width = width
        self.height = height

        self.grid = mesa.space.MultiGrid(width, height, torus=False)
        self.schedule = mesa.time.RandomActivationByType(self)

        self.sugar_distribution = np.genfromtxt('data/sugar-map.txt')
        self.spice_distribution = np.flip(self.sugar_distribution, axis=1)

        agent_id = 0
        for _, (x, y) in self.grid.coord_iter():
            for resource, resource_class in zip([self.sugar_distribution, self.spice_distribution], [Sugar, Spice]):
                max_amount = resource[x, y]
                if max_amount == 0:
                    continue
                resource_instance = resource_class(agent_id, self, (x, y), max_amount)
                self.grid.place_agent(resource_instance, (x, y))
                print(self.schedule.agents_by_type[resource_class][agent_id])
                agent_id += 1

                # print(_, (x, y))


model = SugarscapeG1mt()
# plt.imshow(model.sugar_distribution, origin='lower')
# plt.show()

apple = 1