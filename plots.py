import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

def plot_H_V_T_P():
    with open('in_out/output.txt') as f:
        lines = f.readlines()
        data = [line.split() for line in lines]
        data = np.array(data, dtype=float)

    t = data[:,0]
    H = data[:,1]
    V = data[:,2]
    T = data[:,3]
    P = data[:,4]

    fig, ax = plt.subplots(2, 2)
    fig.set_size_inches(12, 10)

    ax[0,0].plot(t, H)
    ax[0,0].set_title('H')
    ax[0,0].set_xlabel('t [ps]')
    ax[0,0].set_ylabel('H [kJ/mol]')

    ax[0,1].plot(t, V)
    ax[0,1].set_title('V')
    ax[0,1].set_xlabel('t [ps]')
    ax[0,1].set_ylabel('V [kJ/mol]')

    ax[1,0].plot(t, T)
    ax[1,0].set_title('T')
    ax[1,0].set_xlabel('t [ps]')
    ax[1,0].set_ylabel('T [K]')

    ax[1,1].plot(t, P)
    ax[1,1].set_title('P')
    ax[1,1].set_xlabel('t [ps]')
    ax[1,1].set_ylabel('P [16.6 atm]')

    # plt.show()
    plt.savefig('in_out/H_V_T_P.png')

def plot_3d_animation():

    with open('in_out/output.txt') as f:
        lines = f.readlines()
        data = [line.split() for line in lines]
        data = np.array(data, dtype=float)

    T = data[:,3]
    T = np.round(T, 1)

    with open('in_out/argon.xyz') as f:
        lines = f.readlines()
        n = int(lines[0])
        data = [line.split() for line in lines[1:]]
        data = [line[1:] for line in data]
        data = np.array(data, dtype=float)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_title('T = ' + str(T[0]) + ' K')
    fig.set_size_inches(6, 6)
    ax.set_xlim3d([-2.5, 2.5])
    ax.set_ylim3d([-2.5, 2.5])
    ax.set_zlim3d([-2.5, 2.5])

    scatter = ax.scatter([], [], [])

    # Create a sphere
    r = 2.3
    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, np.pi, 100)
    x = np.outer(np.cos(u), np.sin(v)) * r
    y = np.outer(np.sin(u), np.sin(v)) * r
    z = np.outer(np.ones(np.size(u)), np.cos(v)) * r
    ax.plot_wireframe(x, y, z, color='r', alpha=0.05)

    def update_graph(num):
        # Update the scatter plot data
        scatter._offsets3d = (data[num*n:(num+1)*n, 0], data[num*n:(num+1)*n, 1], data[num*n:(num+1)*n, 2])
        ax.set_title('T = ' + str(T[num]) + ' K')
        return scatter,

    ani = animation.FuncAnimation(fig, update_graph, frames=len(data)//n, interval=50, blit=True)
    ani.save('in_out/animation.gif', writer='imagemagick')

    # plt.show()

if __name__ == '__main__':
    # plot_H_V_T_P()
    plot_3d_animation()