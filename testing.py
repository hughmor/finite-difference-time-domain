import unittest
from fdtd import FDTDSimulation
from render import SimulationRender
import numpy as np


class TestCases(unittest.TestCase):
    def test_animate_heatmap(self):
        # dummy simulation (only needs history)
        class Sim:
            def __init__(self):
                self.size = (1000, 1000)
                self.history = [tuple(np.random.random(self.size) for _ in range(6)) for _ in range(5)]
        s = Sim()
        rend = SimulationRender(s)
        rend.generate_animation()

    def test_simulation(self):
        params = {
            "time_stepsize":  1.0e-12,
            "x_length": 1.0e-6,
            "x_stepsize": 1.0e-9,
            "y_length": 1.0e-6,
            "y_stepsize": 1.0e-9,
            "boundary": {
                "type": "PML",
                "n_layers": 5
            },
            "source": {
                "position": (),
            },
            "objects": [
                {
                    None
                },
            ]
        }

        sim = FDTDSimulation(**params)
        rend = SimulationRender(sim)
        rend.generate_animation()


if __name__ == '__main__':
    unittest.main()
