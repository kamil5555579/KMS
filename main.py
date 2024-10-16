from argon import state
import in_out as io
import numpy as np
import matplotlib.pyplot as plt

def main():
    parameters = io.read_parameters('in_out/parameters.txt')
    s = state(parameters)
    s.initialize_r(s.r)
    s.initialize_p(s.p)

    T_avg, P_avg, H_avg = s.run()

    print('T_avg =', T_avg)
    print('P_avg =', P_avg)
    print('H_avg =', H_avg)

    # fig = plt.figure()
    # ax = fig.add_subplot(111, projection='3d')
    # ax.scatter(s.r[:,0], s.r[:,1], s.r[:,2])
    # plt.show()

if __name__ == '__main__':
    main()