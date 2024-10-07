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

read_parameters('parameters.txt')