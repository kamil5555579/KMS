def read_parameters(filename):
    """Reads the parameters from a file."""
    with open(filename, 'r') as f:
        lines = f.readlines()
        n = int(lines[0].split()[0])
        m = float(lines[1].split()[0])
        e = float(lines[2].split()[0])
        R = float(lines[3].split()[0])
        f = float(lines[4].split()[0])
        L = float(lines[5].split()[0])
        a = float(lines[6].split()[0])
        T0 = float(lines[7].split()[0])
        tau = float(lines[8].split()[0])
        S_0 = int(lines[9].split()[0])
        S_d = int(lines[10].split()[0])
        S_out = int(lines[11].split()[0])
        S_xyz = int(lines[12].split()[0])
        parameters = (n, m, e, R, f, L, a, T0, tau, S_0, S_d, S_out, S_xyz)
        
    return parameters

def write_header(filename, r):
    """Writes the number of particles to a file."""
    with open(filename, 'w') as f:
        f.write(str(len(r)) + '\n')

def write_xyz(filename, r):
    """Writes the positions of the particles to a file."""
    with open(filename, 'a') as f:
        for i in range(len(r)):
            f.write('Ar ')
            f.write(' '.join(map(str, r[i])) + '\n')
        
def create_output(filename):
    """Creates a new output file."""
    with open(filename, 'w') as f:
        pass

def write_output(filename, t, H, V, T, P):
    """Writes the output to a file."""
    with open(filename, 'a') as f:
        f.write(str(t) + ' ' + str(H) + ' ' + str(V) + ' ' + str(T) + ' ' + str(P) + '\n')

# read_parameters('parameters.txt')