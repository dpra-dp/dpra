import math
import random
import matplotlib.pyplot as plt
import numpy as np
import itertools
from collections import Counter


# generating noise
def get_noise(x0, k, x, p, c, lamda, noise_type, miu, s):
    if noise_type == 'uniform':
        return np.random.randint(x0, x + 1)
    elif noise_type == 'geometric':
        a = np.random.geometric(p)
        if a > x:
            return x
        else:
            return a - 1 + x0
    elif noise_type == 'constant':
        return c
    elif noise_type == 'laplace':
        # h =1.328*lamda
        # g=lamda/(10*np.log(2))
        # return max(0, int(np.random.laplace(1*h,1*g)))
        return max(0, np.random.laplace(loc=miu, scale=s))
    elif noise_type == 'akr':
        a = max(0, np.random.laplace(loc=miu, scale=s))
        return a
    elif noise_type == 'laplace2':
        n = np.random.laplace(loc=miu, scale=s)
        return n
    else:
        print("Invalid Noise Type Input!")
        return 0


V = 1

# adding laplace noise to the total number of requests
def add_noise(x0, k, m, noise_type, x, p, c, lamda, miu, s):
    noise1 = round(get_noise(x0=x0, k=k, x=x, p=p, c=c, lamda=lamda, noise_type=noise_type, miu=miu, s=s))
    noise2 = round(get_noise(x0=x0, k=k, x=x, p=p, c=c, lamda=lamda, noise_type=noise_type, miu=miu, s=s))

    while noise2 < 2:
        noise2 = round(get_noise(x0=x0, k=k, x=x, p=p, c=c, lamda=lamda, noise_type=noise_type, miu=miu, s=s))

    while noise1 < 1:
        noise1 = round(get_noise(x0=x0, k=k, x=x, p=p, c=c, lamda=lamda, noise_type=noise_type, miu=miu, s=s))

    f_prime = m + V + noise1

    f = m + noise2

    return f, f_prime


# perform allocation and output the number of resources assigned to the attacker
def allocation(f, f_prime, m, k):
    if f < 0 or f == 0:
        F = 0
        u = 0
    elif f > m:
        U = [0] * m + [2] * (f - m)
        np.random.shuffle(U)
        # why not just get count_zeros?
        F = min(k, len(U)) - np.count_nonzero(U[:min(k, len(U))])
        u = F / min(k, len(U))
        u = F / k
    else:
        # so this is 0<f<=m. what if m>=f>k? is this consition considered?
        # should it be F = min(k, f)?
        F = min(k, f)
        u = F / min(k, f)
        u = F / k

    if f_prime < 0 or f_prime == 0:
        F_p = 0
    elif f_prime > m + 1:
        U_p = [0] * m + [2] * (f_prime - m - 1) + [1] * V
        np.random.shuffle(U_p)
        F_p = min(k, len(U_p)) - np.count_nonzero(U_p[:min(k, len(U_p))])
    else:
        U_p = [0] * m + [1] * V
        np.random.shuffle(U_p)
        F_p = min(k, f_prime) - np.count_nonzero(U_p[:min(k, f_prime)])

    return F, F_p, u


def find_max_PL(F, F_p):
    idx = [i for i, e in enumerate(F_p) if e != 0]
    pl = []
    for i in idx:
        if F[i] == 0:
            pl.append(float('inf'))
        else:
            pl.append(max(F_p[i] / F[i], F[i] / F_p[i]))
    return pl


def non_inf(a):
    b = []
    for i in a:
        if i != float('inf'):
            b.append(i)
    return b


def counter_process(F, F_prime):
    F_counter = Counter(F)
    F_prime_counter = Counter(F_prime)
    L = max(max(F), max(F_prime)) - min(0, min(min(F), min(F_prime))) + 1
    Before_RA_F = [0] * max(11, L)
    Before_RA_F_p = [0] * max(11, L)
    for i in F_counter.keys():
        Before_RA_F[i] = F_counter.get(i)
    for i in F_prime_counter.keys():
        Before_RA_F_p[i] = F_prime_counter.get(i)
    return Before_RA_F, Before_RA_F_p


def find_max(F, F_p):
    idx = [i for i, e in enumerate(F_p) if e != 0]
    pl = []
    for i in idx:
        if F[i] == 0:
            pl.append(float('inf'))
        elif F[i] > 0:
            pl.append(max(F_p[i] / F[i], F[i] / F_p[i]))
        else:
            continue
    return pl


