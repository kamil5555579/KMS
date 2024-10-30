# argon state
import in_out as io
import numpy as np

def mod_rij(ri, rj):
    return np.sqrt(np.sum((ri - rj)**2))

def mod_ri(ri):
    return np.sqrt(np.sum(ri**2))
class state:
    def __init__(self, parameters, seed=0):
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
        self.F = np.zeros(shape=(self.N, 3))
        self.V = 0.0
        self.P = 0.0
        self.H = 0.0
        self.T = 0.0
        np.random.seed(seed)

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

    def Vp_ij(self, ri, rj):
        rij = mod_rij(ri, rj)
        return self.e * ((self.R / rij)**12 - 2 * (self.R / rij)**6)
    
    def Vs_i(self, ri):
        ri = mod_ri(ri)
        return 0.5 * self.f * (ri - self.L)**2 if ri >= self.L else 0
    
    def Fp_ij(self, ri, rj):
        rij = mod_rij(ri, rj)
        return 12 * self.e * ((self.R / rij)**12 - (self.R / rij)**6) * (ri - rj) / rij**2
    
    def Fs_i(self, ri):
        ri_mod = mod_ri(ri)
        return self.f * (self.L - ri_mod) * (ri / ri_mod) if ri_mod >= self.L else 0

    def calc_V_F_P(self):
        V = 0.0
        F = np.zeros(shape=(self.N, 3))
        Fs_sum = 0.0
        for i in range(self.N):
            V += self.Vs_i(self.r[i])
            F[i] += self.Fs_i(self.r[i])
            Fs_sum += np.sqrt(np.sum(self.Fs_i(self.r[i])**2))
            for j in range(i+1, self.N):
                V += self.Vp_ij(self.r[i], self.r[j])
                F[i] += self.Fp_ij(self.r[i], self.r[j])
                F[j] -= self.Fp_ij(self.r[i], self.r[j])

        P = 1 / (4 * np.pi * self.L**2) * Fs_sum
        self.V = V
        self.F = F
        self.P = P
    
    def calc_H_T(self):
        H = 0.0
        T = 0.0
        for i in range(self.N):
            H += 0.5 * np.sum(self.p[i]**2) / self.m
            T += 0.5 * np.sum(self.p[i]**2) / self.m
        H = H + self.V
        T = 2 * T / (3 * self.N * self.k)
        self.H = H
        self.T = T
    
    def update_r(self):
        self.r += self.p * self.tau / self.m

    def update_p(self):
        self.p += 0.5 * self.F * self.tau

    def step(self):
        self.update_p()
        self.update_r()
        self.calc_V_F_P()
        self.update_p()
        self.calc_H_T()
    
    def run(self):
        io.write_header('in_out/argon.xyz', self.r)
        io.create_output('in_out/output.txt')
        t = 0.0
        T_acc, P_acc, H_acc = 0.0, 0.0, 0.0
        for i in range(self.S_0 + self.S_d):
            self.step()
            if i % self.S_xyz == 0:
                print(f'Writing to xyz file... {i} out of {self.S_0 + self.S_d}')
                io.write_xyz('in_out/argon.xyz', self.r)
            if i % self.S_out == 0:
                io.write_output('in_out/output.txt', t, self.H, self.V, self.T, self.P)
            if i >= self.S_0:
                T_acc += self.T
                P_acc += self.P
                H_acc += self.H
            t += self.tau
        T_avg = T_acc / self.S_d
        P_avg = P_acc / self.S_d
        H_avg = H_acc / self.S_d

        return T_avg, P_avg, H_avg

