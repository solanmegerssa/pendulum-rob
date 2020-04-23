import gym
import numpy as np
import serial
import time

import balance_bot
import balance_lqr


def main(sim_hil=True):
    # create the environment
    env = gym.make("balancebot-v0")
    if sim_hil:
        hil_sim(env)
    else:
        controller_sim(env)

    env.close()

def controller_sim(env):
    """ performs closed loop sim with LQR controller """

    controller = balance_lqr.BalanceLQR()
    observation = env.reset()
    for t in range(10000):
        env.render(mode="human")

        # control loop
        gains = controller.compute_gains()
        control_force = np.dot(gains, observation)[0]*0.5
        print("Control force: {}".format(control_force))
        observation, _, done, _ = env.step(control_force)
        if done:
            print("Episode finished after {} timesteps".format(t+1))
            break

# TODO: move these to a different module
def hil_sim(env, arduino_port="/dev/ttyACM0", baud=115200):
    arduino_connection = serial.Serial(arduino_port, baud, timeout=0.1)
    observation = env.reset()
    while True:
        env.render(mode="human")
        msg_str = write_serial_message(observation)
        print(msg_str)
        arduino_connection.write(msg_str.encode())
        observation, _, _, _ = env.step(0.1)
        time.sleep(.01) # Delay for one tenth of a second

def write_serial_message(observation):
    msg_str = "<"
    for data in observation:
        msg_str += '%.3f'%(data)
        msg_str += ", "
    msg_str += ">"

    return msg_str


if __name__ == '__main__':
    # TODO: add argparse here
    main(sim_hil=True)