import mesa
from engine import SugarscapeG1mt

if __name__ == '__main__':

    model = SugarscapeG1mt()
    model.run_model(step_count=1)
    apple = 1