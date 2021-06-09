import numpy as np
import matplotlib.pyplot as plt
from simulation_lib import *


# plotting
def plot_b0_b1(mal, F1, F2, x0, x):
    plt.style.use('seaborn')
    plt.figure()
    plt.plot(mal, F1, marker='o', markersize=6, linewidth=4, label='D')
    plt.plot(mal, F2, marker='s', markersize=6, linewidth=4, linestyle='--', label='D\'')
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.xlabel('resources allocated to attacker', fontsize=22)
    plt.ylabel('frequency', fontsize=22)
    plt.legend(loc='best', fontsize=22)
    plt.grid(True)
    plt.savefig('uni.pdf', bbox_inches="tight")
    plt.show()


# Parameter default setup
p = 0
c = 0
lamda = 0

noise_type = 'uniform'
RD = 100000000
k = 10
m = 10  # best strategy

x0 = -10
X = [10, 15]
result = []
utility = []
OFFSET = [0]
for offset in OFFSET:
    for x in X:
        x0 = x0
        x = x
        F = []
        F_prime = []
        a = []
        b = []
        uti = []
        print(x0, x)
        for rd in range(RD):
            f, f_prime = add_noise(x0=x0, k=k, m=m, noise_type=noise_type, x=x, p=p, c=c, lamda=lamda, miu=0, s=s)
            F.append(f)
            F_prime.append(f_prime)
            ra_f, ra_f_p, u = allocation(f=f, f_prime=f_prime, m=m, k=k)
            a.append(ra_f)
            b.append(ra_f_p)
            uti.append(u)

        utility.append(np.mean(uti))
        Before_RA_F, Before_RA_F_p = counter_process(F=F, F_prime=F_prime)
        After_RA_F, After_RA_F_p = counter_process(F=a, F_prime=b)
        print('x_l, x_r', x0, x)
        plot_b0_b1(range(11), After_RA_F, After_RA_F_p, x0=x0, x=x)
        print(str(noise_type) + " - Simulation (k = " + str(k) + "), before RA:",
              max(non_inf(np.log(find_max(Before_RA_F, Before_RA_F_p)))))
        r = max(non_inf(np.log(find_max(After_RA_F, After_RA_F_p))))
        print('max (y) at:', non_inf(np.log(find_max(After_RA_F, After_RA_F_p))).index(r))
        print(str(noise_type) + " - Simulation (k = " + str(k) + "), after RA:", r)
        result.append(r)
        print("utility:", np.mean(uti))
