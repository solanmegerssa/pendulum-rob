import gym
import balance_bot
import balance_lqr
import numpy as np
 
def callback(lcl, glb):
    # stop training if reward exceeds 199
    is_solved = lcl['t'] > 100 and sum(lcl['episode_rewards'][-101:-1]) / 100 >= 199
    return is_solved


def main():
    # create the environment
    env = gym.make("balancebot-v0") # <-- this we need to create

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
    env.close()
 
if __name__ == '__main__':
    main()