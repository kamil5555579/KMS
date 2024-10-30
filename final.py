import matplotlib.pyplot as plt
import numpy as np
from argon import state
import in_out as io

def plot_H():

    parameters = io.read_parameters('in_out/parameters.txt')
    s = state(parameters)
    s.initialize_r(s.r)
    s.initialize_p(s.p)
    T_avg, P_avg, H_avg = s.run()

    with open('in_out/output.txt') as f:
        lines = f.readlines()
        data = [line.split() for line in lines]
        data = np.array(data, dtype=float)

    t = data[:,0]
    H = data[:,1]

    fig, ax = plt.subplots(1, 1)
    ax.plot(t, H)
    ax.set_title('H')
    ax.set_xlabel('t [ps]')
    ax.set_ylabel('H [kJ/mol]')

    # plt.show()
    plt.savefig('in_out/H.png')

def plot_V_a():
    
    parameters = io.read_parameters('in_out/parameters.txt')
    s = state(parameters)

    V = np.array([])
    for a in np.linspace(0.35, 0.41, 30):
        s.a = a
        s.initialize_r(s.r)
        s.initialize_p(s.p)
        s.calc_V_F_P()
        V = np.append(V, s.V)

    a = np.linspace(0.35, 0.41, 30)

    fig, ax = plt.subplots(1, 1)
    ax.plot(a, V)
    ax.set_title('V(a)')
    ax.set_xlabel('a [nm]')
    ax.set_ylabel('V [kJ/mol]')

    # plt.show()
    plt.savefig('in_out/V_a.png')
    V_min = np.min(V)
    a_min = a[np.argmin(V)]
    print('V_min =', V_min)
    print('a_min =', a_min)

if __name__ == '__main__':
    plot_V_a()