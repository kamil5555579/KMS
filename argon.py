# argon state
import in_out as io
import numpy as np

class state:
    def __init__(self, parameters):
        self.n = parameters[0]
        self.m = parameters[1]
        self.e = parameters[2]
        self.R = parameters[3]
        self.f = parameters[4]
        self.L = parameters[5]
        self.a = parameters[6]
        self.T0 = parameters[7]
        self.tau = parameters[8]
        self.S_0 = parameters[9]
        self.S_d = parameters[10]
        self.S_out = parameters[11]
        self.S_xyz = parameters[12]
        self.N = self.n**3
        self.k = 8.31e-3
        self.r = np.zeros(shape=(self.N, 3))
        self.p = np.zeros(shape=(self.N, 3))

    def initialize_r(self, r):
        b0 = np.array([self.a, 0.0, 0.0])
        b1 = np.array([self.a/2, self.a * np.sqrt(3) / 2, 0.0])
        b2 = np.array([self.a/2, self.a * np.sqrt(3) / 6, self.a * np.sqrt(2/3)])
        count = 0
        for i in range(self.n):
            for j in range(self.n):
                for k in range(self.n):
                    r[count] = (i-(self.n-1)/2)*b0 + (j-(self.n-1)/2)*b1 + (k-(self.n-1)/2)*b2
                    count += 1

        self.r = r

    def initialize_p(self, p):
        E_kin = np.zeros(shape=(self.N, 3))
        for i in range(self.N):
            E_kin[i] = -(1/2) * self.k * self.T0 * np.log(np.random.rand(3))

        # E_kin_avg = np.sum(E_kin, axis=0) / n
        
        for i in range(self.N):
            signs = np.random.rand(3)
            for j in range(3):
                signs[j] = -1 if signs[j] < 0.5 else 1
            p[i] = np.sqrt(2 * self.m * E_kin[i]) * signs

        P = np.sum(p, axis=0)
        p -= P / self.N

        self.p = p

    def Vp(self, rij):
        return self.e * ((self.R / rij)**12 - 2 * (self.R / rij)**6)