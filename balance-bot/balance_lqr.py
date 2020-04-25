import numpy as np
from scipy import linalg, signal

class BalanceLQR:
    def __init__(self):

        I = .001 # kgm**2
        m = 0.8 # kg
        l = 0.4 # m
        b = 1 # coefficient of friction
        g = 9.8 # m/s**2
        # state vector is [x, x_dot, pitch, pitch_dot]

        mass_moment = I*m + m**2*l**2 # TODO might have to get rid of second term
        self.A = np.array(
            [
                [0, 1, 0, 0],
                [0, -(I+m*l**2)*b/mass_moment, m**2*g*l**2/mass_moment, 0],
                [0, 0, 0, 1],
                [0, -m*l*b/mass_moment, m**2*g*l/mass_moment, 0]
            ]
        )

        self.B = np.array(
            [
                [0],
                [(I+m*l**2)/mass_moment],
                [0],
                [m*l/mass_moment]
            ]
        )

        self.C = np.array(
            [
                [1, 0, 0, 0],
                [0, 0, 1, 0]
            ]
        )

        self.D = np.array(
            [
                [0],
                [0]
            ]
        )
    def compute_gains(self, position_weight=1.0, pitch_weight=1.0, control_weight=1.0, dt=0.01):

        Q = np.diag([position_weight, 0, pitch_weight, 0.0])
        R = np.diag([control_weight])

        A_de, B_de, C_de, D_de, dt = signal.cont2discrete((self.A, self.B, self.C, self.D), dt)
          # solve Discrete Ricatti Equation
        P = linalg.solve_discrete_are(A_de, B_de, Q, R)

        # compute optimum controller gains
        Bp = np.linalg.multi_dot([B_de.T, P, B_de])
        Bp = np.linalg.inv((R+Bp))
        gains = np.linalg.multi_dot([Bp, B_de.T, P, A_de])

        return gains


if __name__ == "__main__":
    lqr = BalanceLQR()
    gains = lqr.compute_gains()
    print(gains)