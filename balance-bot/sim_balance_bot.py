import gym
import numpy as np
import serial
import time

import balance_bot
import balance_lqr


def main(sim_with_hil=False):
    # create the environment
    env = gym.make("balancebot-v0") # <-- this we need to create

    if not sim_with_hil:
        controller = balance_lqr.BalanceLQR()
        observation = env.reset()
        for t in range(10000):
            env.render(mode="human")
            # print(observation)

            # control loop
            gains = controller.compute_gains()
            control_force = np.dot(gains, observation)[0]*0.5
            print("Control force: {}".format(control_force))
            observation, reward, done, info = env.step(control_force)
            if done:
                print("Episode finished after {} timesteps".format(t+1))
                break
        print("Episode success".format(t+1))  
    else:
        hil_sim(env)

    env.close()

def hil_sim(env, arduino_port="/dev/ttyACM0", baud=115200):
    arduino_connection = serial.Serial(arduino_port, baud, timeout=0.1)
    counter = 32 # Below 32 everything in ASCII is gibberish
    while True:
        counter +=1
        arduino_connection.write(str(chr(counter)).encode()) # Convert the decimal number to ASCII then send it to the Arduino
        data = arduino_connection.readline()
        # data = str(data)
        data.rstrip(b'\n')
        print(data.decode()) # Read the newest output from the Arduino
        time.sleep(.1) # Delay for one tenth of a second
        if counter == 255:
            counter = 32


if __name__ == '__main__':
    main(sim_with_hil=True)