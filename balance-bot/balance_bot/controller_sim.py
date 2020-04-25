import balance_lqr
import numpy as np

def lqr_sim(env):
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
