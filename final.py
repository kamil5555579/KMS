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

def plot_P_T():
    P_arr = np.array([2.8, 13.7, 24.7, 35.2])
    T_arr = np.array([162.2, 596, 1074.5, 1537.4])

    fig, ax = plt.subplots(1, 1)
    ax.plot(T_arr, P_arr, 'o')
    ax.set_title('$P_{avg}(T_{avg})$')
    ax.set_ylabel('$P_{avg}$ [16.6 atm]')
    ax.set_xlabel('$T_{avg}$ [K]')

    # linear fit

    m, b = np.polyfit(T_arr, P_arr, 1)
    T = np.linspace(0, 2000, 100)
    P = m * T + b
    ax.plot(T, P, '--', label = 'dopasowanie liniowe')

    print('m =', m)
    print('b =', b)
    m_teor = 125 * 1.5 * 8.31e-3 * 0.75 / (np.pi * 2.3* 2.3 * 2.3)
    print('m_teor =', m_teor)

    P = m_teor * T + b
    ax.plot(T, P, '--', label = 'krzywa teoretyczna')
    ax.legend()

    plt.savefig('in_out/P_T.png')

if __name__ == '__main__':
    plot_P_T()