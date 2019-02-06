from __future__ import absolute_import, print_function, division
from rotary_pendulum_pybullet import RotaryPendulumPyBulletEnv
from rotary_pendulum import RotaryPendulumEnv

from gym_brt.control import NoControl, \
                            RandomControl, \
                            QubeFlipUpControl, \
                            QubeHoldControl#, \
                            # QubeDampenControl
import numpy as np
import argparse
import gym
import time

def main():
    # Get arguments to quickly test the environments
    parser = argparse.ArgumentParser(description='Renders a Gym environment for quick inspection.')
    parser.add_argument('--pybullet', '-pb', action='store_true', help='Whether to use Mujoco (default) or PyBullet.')
    parser.add_argument('--begin_down', '-bd', action='store_true', help='Whether to start the pendulum at the top (default) or at the bottom')
    parser.add_argument('--controller', '-c', type=str, default='flip', choices=['none', 'rand', 'flip', 'hold'], help='The controller to use.')
    parser.add_argument( '--frequency', '-f', default='1000', type=float, help='The frequency of the simulation.')
    args = parser.parse_args()

    # A list of available classical controllers
    controllers_dict = {
        'none': NoControl,
        'rand': RandomControl,
        'flip': QubeFlipUpControl,
        'hold': QubeHoldControl,
    }
    Controller = controllers_dict[args.controller]

    # Select Mujoco or PyBullet to run the simulation
    if args.pybullet:
        env = RotaryPendulumPyBulletEnv() # PyBullet Env
    else:
        env = RotaryPendulumEnv() # Mujoco env

    env.render(mode="human") # Needed for pybullet for some reason...
    ctrl_sys = Controller(env, frequency=args.frequency) # Set the controller
    obs = env.reset() # Get the initial observation

    # Run the loop reseting every 3 seconds
    step = 0
    while True:
        action = ctrl_sys.action(obs)
        # action = env.action_space.sample()
        obs, reward, _, _ = env.step(action)
        env.render('human')
        if step % (3 * args.frequency) == 0:
            obs = env.reset()
        step += 1


if __name__ == '__main__':
    main()