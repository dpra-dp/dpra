import math
import numpy as np
import matplotlib.pyplot as plt



def geo2(k, n, eps, miu):
    Pr_y = []
    c = (1 - math.exp(-eps)) / (1 + math.exp(-eps))

    for y in range(k + 1):
        s = float(0)
        for a in range(max(k - y, 0), n + 1):
            s = s + c * float((math.factorial(a) * math.factorial(a) * math.exp(-eps * abs(a - miu)) * math.factorial(
                k) * math.factorial(k))) / float((math.factorial(a - k + y) * math.factorial(k + a) * math.factorial(
                y) * math.factorial(k - y) * math.factorial(k - y)))
        if y == k:
            Pr_y.append(s)
        else:
            Pr_y.append((s + c * math.exp(-eps * abs((y - k - miu)))))
    return Pr_y


def geo1(k, n, p, xl):
    Pr_y = []
    for y in range(k + 1):
        s = float(0)
        b = p * (math.factorial(k) * math.factorial(k)) / (
                math.factorial(y) * math.factorial(k - y) * math.factorial(k - y))
        for a in range(max(k - y, xl), n + 1):
            s += b * ((1 - p) ** (a - xl)) * math.factorial(a) * math.factorial(a) / (
                    math.factorial(a - k + y) * math.factorial(k + a))
        Pr_y.append(s)
    return Pr_y


def uni(k, n, xl, xr):
    Pr_y = []
    p = 1 / (xr - xl + 1)
    for y in range(k + 1):
        s = float(0)
        b = (math.factorial(k) * math.factorial(k)) / (
                    math.factorial(y) * math.factorial(k - y) * math.factorial(k - y))
        for a in range(max(k - y, xl), xr + 1):
            w = math.factorial(a) * math.factorial(a) / (math.factorial(a - k + y) * math.factorial(k + a))
            s += p * b * w
        if y < k and xl <= (y - k):
            s += p
            if y == 0 and xl < (-k):
                s += p * (-k - xl)
        Pr_y.append(s)
    return Pr_y


def cst(k, c):
    Pr_y = []
    for y in range(k + 1):
        s = (math.factorial(k) * math.factorial(k) * math.factorial(c) * math.factorial(c)) / (
                    math.factorial(y) * math.factorial(k - y) * math.factorial(k - y) * math.factorial(
                c - k + y) * math.factorial(k + c))
        Pr_y.append(s)
    return Pr_y


def akr(k, n, eps, delta):
    miu = round(1 - np.log(2 * delta) / eps)
    Pr_y = []
    c = (1 - math.exp(-eps)) / (1 + math.exp(-eps))

    Pr_0 = 0
    for a in range(-200, 1):
        Pr_0 += c * math.exp(-eps * abs(a - miu))
    for y in range(k + 1):
        s = float(0)
        b = (math.factorial(k) * math.factorial(k)) / (
                    math.factorial(y) * math.factorial(k - y) * math.factorial(k - y))
        for a in range(max(k - y, 1), n + 1):
            s += c * float((math.factorial(a) * math.factorial(a) * math.factorial(k) * math.factorial(k) * math.exp(
                -eps * abs(a - miu)))) / float((math.factorial(a - k + y) * math.factorial(k + a) * math.factorial(
                y) * math.factorial(k - y) * math.factorial(k - y)))
        if y == k:
            s += Pr_0
        Pr_y.append(s)
    return Pr_y


Py_geo2 = geo2(k=10, n=91, eps=1, miu=0)
Py_geo1 = geo1(k=10, n=91, p=0.7, xl=0)
Py_uni = uni(k=10, n=91, xl=1, xr=10)
Py_cst = cst(k=10, c=10)
Py_akr = akr(k=10, n=91, eps=1, delta=10**(-6))


k=10
plt.style.use("seaborn")
plt.figure()
plt.plot(range(k+1),Py_cst,marker='^', markersize=6, linewidth=3,label="CST")
plt.plot(range(k+1),Py_uni,marker='s', markersize=6, linewidth=3,label="UNI")
plt.plot(range(k+1),Py_geo1,marker='p',markersize=6, linewidth=3, label="GEO")
plt.plot(range(k+1),Py_geo2,marker='o',markersize=6, linewidth=3, label="GEO2")
plt.plot(range(k+1),Py_akr,marker='v', markersize=6, linewidth=3,label="AKR")

plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.ylabel(r'$Pr[y=j]$', fontsize=22)
plt.xlabel(r'$j$', fontsize=22)
plt.legend(loc='best',fontsize = 20)
plt.show()
