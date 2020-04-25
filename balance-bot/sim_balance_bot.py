import gym
from balance_bot import hil_sim, controller_sim


def main(sim_hil=True):
    # create the environment
    env = gym.make("balancebot-v0")
    if sim_hil:
        hil_sim.hil_sim(env)
    else:
        controller_sim.lqr_sim(env)

    env.close()

if __name__ == '__main__':
    # TODO: add argparse here
    main(sim_hil=True)