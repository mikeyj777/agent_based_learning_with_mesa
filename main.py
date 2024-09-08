import mesa
from engine import SugarscapeG1mt

if __name__ == '__main__':

    model = SugarscapeG1mt()
    for i in range(5):
        model.step()
    apple = 1