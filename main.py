import numpy as np
import matplotlib.pyplot as plt

a = 0.38
n = 5
N = n**3
T0 = 100.0
k = 8.31e-3
m = 39.948
r = np.zeros(shape=(N, 3))
p = np.zeros(shape=(N, 3))
print(p)

def initialize_r(r):
    b0 = np.array([a, 0.0, 0.0])
    b1 = np.array([a/2, a * np.sqrt(3) / 2, 0.0])
    b2 = np.array([a/2, a * np.sqrt(3) / 6, a * np.sqrt(2/3)])
    count = 0
    for i in range(n):
        for j in range(n):
            for k in range(n):
                r[count] = (i-(n-1)/2)*b0 + (j-(n-1)/2)*b1 + (k-(n-1)/2)*b2
                count += 1

def initialize_p(p):
    E_kin = np.zeros(shape=(N, 3))
    for i in range(n*n*n):
        E_kin[i] = -(1/2) * k * T0 * np.log(np.random.rand(3))

    # E_kin_avg = np.sum(E_kin, axis=0) / n
    for i in range(n*n*n):
        signs = np.random.rand(3)
        for j in range(3):
            signs[j] = -1 if signs[j] < 0.5 else 1
        p[i] = np.sqrt(2 * m * E_kin[i]) * signs

    P = np.sum(p, axis=0)
    p -= P / N

initialize_r(r)
initialize_p(p)
print(p)

# Plot the lattice
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(r[:,0], r[:,1], r[:,2])
plt.show()
