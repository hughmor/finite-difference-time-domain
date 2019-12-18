import sys
from fdtd import FDTDSimulation
from render import SimulationRender

help_text = "\n\n" \
            "2D FDTD Simulation Platform\n" \
            "Written by Hugh Morison\n" \
            "\n" \
            "Allowed arguments:\n" \
            "\t--help: Prints this help string\n" \
            "\t--x_length: Supply the length of the horizontal simulation direction [in micrometres]\n" \
            "\t--y_length: Supply the length of the vertical simulation direction [in micrometres]\n" \
            "\t--x_stepsize: Supply the grid spacing of the horizontal simulation direction [in micrometres]\n" \
            "\t--y_stepsize: Supply the grid spacing of the vertical simulation direction [in micrometres]\n" \
            "\t--t_length: Supply the duration of the simulation [in microseconds]\n" \
            "\t--t_stepsize: Supply the time step of the simulation [in microseconds]\n" \
            "\t--render: Whether to generate a rendering of the simulation [T/F]\n" \
            "\t--render_quantity: Which field quantity is rendered [E/H/Ei/Hi for i=(x,y,z)]\n" \
            "\n" \
            "Custom grid and time space parameters will be checked to make sure they function. A warning will be" \
            "displayed if the parameters reduce accuracy or break the simulation.\n"

simulation_args = {
    "x_length": 1.0,
    "y_length": 1.0,
    "x_stepsize": 0.1,
    "y_stepsize": 0.1
}

allowed_switches = {
    "help": 0
}

for k in simulation_args:
    allowed_switches[k] = 1  # 1 value to change


def parse_args():
    kwargs = simulation_args
    if len(sys.argv) > 1:  # arguments supplied
        _ = sys.argv.pop(0)  # filename
        while len(sys.argv) > 0:
            switch = sys.argv.pop(0).split('--')[1]
            if switch not in allowed_switches:
                raise ValueError('Invalid command line argument supplied: {} is not a valid switch'.format(switch))
            n_args = allowed_switches[switch]
            args = []
            for i in range(n_args):
                args.append(sys.argv.pop(0))
            if switch == 'help':
                print(help_text)
                return  # return None to prevent sim
    return kwargs


def main():
    kwargs = parse_args()
    if kwargs is not None:
        env = FDTDSimulation(**kwargs)
        rend = SimulationRender(env)
        rend.generate_animation()


if __name__ == '__main__':
    main()
