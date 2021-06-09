import math
import numpy as np
import csv


def get_utility(Pr_y, k):
    u = 0
    for i in range(k + 1):
        u += Pr_y[i] * i / k
    return u


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
    utility_geo2 = get_utility(Pr_y, k)

    eps_geo2 = [0] * (k + 1)
    for y in range(k + 1):
        num = 0
        den = math.exp(-eps * abs(y - k - 1 - miu)) * (k - y + 1) / (k + 1)
        b = (math.factorial(k) * math.factorial(k)) / (
                    math.factorial(y) * math.factorial(k - y) * math.factorial(k - y))
        for i in range(max(k - y, 0), n + 1):
            num += b * math.factorial(i) * math.factorial(i) * math.exp(-eps * abs(i - miu)) / (
                        math.factorial(i - k + y) * math.factorial(k + i))
        for i in range(max(k - y - 1, 0), n + 1):
            den += b * math.factorial(i + 1) * math.factorial(i + 1) * math.exp(-eps * abs(i - miu)) / (
                        math.factorial(i + 1 - k + y) * math.factorial(k + i + 1))
        if y != k:
            num += math.exp(-eps * abs(y - k - miu))
            den += math.exp(-eps * abs(y - k - miu)) * (y + 1) / (k + 1)
        if num == 0 or den == 0:
            eps_geo2[y] = float('inf')
        else:
            eps_geo2[y] = np.log(max(num / den, den / num))

    if sum(Pr_y) > 0.99:
        return max(eps_geo2), utility_geo2
    else:
        return 0, 0


def geo1(k, n, p, xl):
    Pr_y1 = []
    for y in range(k + 1):
        s = float(0)
        b = p * (math.factorial(k) * math.factorial(k)) / (
                math.factorial(y) * math.factorial(k - y) * math.factorial(k - y))
        for a in range(max(k - y, xl), n + 1):
            s += b * ((1 - p) ** (a - xl)) * math.factorial(a) * math.factorial(a) / (
                    math.factorial(a - k + y) * math.factorial(k + a))
        Pr_y1.append(s)

    if sum(Pr_y1) > 0.99:
        utility_geo1 = get_utility(Pr_y1, k)
        eps_geo = [0] * (k + 1)
        for y in range(0, k + 1):
            Pr_geo = p * math.factorial(k) * math.factorial(k) / (
                    math.factorial(y) * math.factorial(k - y) * math.factorial(k - y))
            s_num = 0
            s_den = 0
            for i in range(max(k - y, xl, 0), n + 1):
                s_num += (1 - p) ** (i - xl) * math.factorial(i) * math.factorial(i) / (
                        math.factorial(i - k + y) * math.factorial(k + i))
            for i in range(max(k - y - 1, xl, 0), n + 1):
                s_den += (1 - p) ** (i - xl) * math.factorial(i + 1) * math.factorial(i + 1) / (
                        math.factorial(i + 1 - k + y) * math.factorial(k + i + 1))
            Xp = 0
            X = 0
            if y < k and y >= (k + xl):
                X += (1 - p) ** (y - k - xl)
                Xp += (p * (1 + y) * (1 - p) ** (y - k - xl)) / (k + 1)
            elif y <= k and y >= (k + xl + 1):
                Xp += (p * (k - y + 1) * (1 - p) ** (y - k - xl - 1)) / (k + 1)
            elif y == 0:
                if xl < -k:
                    X += 1 - (1 - p) ** (-k - xl)
                if xl < -k - 1:
                    Xp += 1 - (1 - p) ** (-k - xl - 1)
            num = s_num * Pr_geo + X
            den = s_den * Pr_geo + Xp
            if num == 0 or den == 0:
                eps_geo[y] = float('inf')
            else:
                eps_geo[y] = np.log(max(num / den, den / num))
        return max(eps_geo), utility_geo1
    else:
        return 0, 0


def uni(k, n, xl, xr):
    Pr_y3 = []
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
        Pr_y3.append(s)
    if sum(Pr_y3) > 0.99:
        utility_uni = get_utility(Pr_y3, k)
        eps_uni = [0] * (k + 1)
        test_num = []
        for y in range(0, k + 1):
            num = 0
            den = 0
            for i in range(max(xl, k - y, 0), xr + 1):
                num += math.factorial(k) * math.factorial(k) * math.factorial(i) * math.factorial(i) / (
                            math.factorial(y) * math.factorial(k - y) * math.factorial(k - y) * math.factorial(
                        i - k + y) * math.factorial(k + i))
            for i in range(max(xl, k - y - 1, 0), xr + 1):
                den += math.factorial(k) * math.factorial(k) * math.factorial(i + 1) * math.factorial(i + 1) / (
                            math.factorial(y) * math.factorial(k - y) * math.factorial(k - y) * math.factorial(
                        i + 1 - k + y) * math.factorial(k + i + 1))
            if y < k and y >= xl + k:
                num += 1
                den += (y + 1) / (k + 1)
                if y <= k and y >= xl + k + 1:
                    den += (k - y + 1) / (k + 1)
            if y == 0:
                if xl < -k:
                    num += -k - xl
                if xl < -k - 1:
                    den += -k - xl - 1
            if num == 0 or den == 0:
                eps_uni[y] = float('inf')
            else:
                eps_uni[y] = np.log(max(num / den, den / num))
            test_num.append(den * p)
        return max(eps_uni), utility_uni
    else:
        return 0, 0


def cst(k, d):
    Pr_y4 = []
    for y in range(k + 1):
        s = (math.factorial(k) * math.factorial(k) * math.factorial(d) * math.factorial(d)) / (
                    math.factorial(y) * math.factorial(k - y) * math.factorial(k - y) * math.factorial(
                d - k + y) * math.factorial(k + d))
        Pr_y4.append(s)
    utility_cst = get_utility(Pr_y4, k)
    eps = [0] * (k + 1)
    for y in range(k + 1):
        eps[y] = ((k + d + 1) * (d + y + 1 - k)) / ((k + d + 1 - k) * (d + 1))
    return max(np.log(eps)), utility_cst


def akr(k, n, eps, delta):
    miu = round(1 - np.log(2 * delta) / eps)
    Pr_y5 = []
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
        Pr_y5.append(s)
    utility_akr = get_utility(Pr_y5, k)
    return eps, utility_akr

k=10
n=91

#geo2
S = [0.01,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.2,1.4,1.6,1.8,2,3,4,5,10,15,20]
MIU = range(0,51)
el=[]
ul=[]
el_all=[]
ul_all = []
for miu in MIU:
  el_geo2=[]
  ul_geo2=[]
  for s in S:
    e,u = geo2(k=k,n=n,eps=1/s,miu=miu)
    el_geo2.append(e)
    ul_geo2.append(u)
    if e!= 0 and u!=0:
      el_all.append(e)
      ul_all.append(u)
  el.append(el_geo2)
  ul.append(ul_geo2)

file = open('geo2.csv', 'w', newline ='')
with file:
    write = csv.writer(file)
    write.writerows([el_all, ul_all])
file.close()

#geo1
P=[0.7]
xl = 0
Xl=[3]
el =[]
ul=[]
el_all = []
ul_all = []
for xl in Xl:
  el_geo=[]
  ul_geo=[]
  for p in P:
    e,u = geo1(k=k,n=n,p=p,xl=xl)
    el_geo.append(e)
    ul_geo.append(u)
    if e!=0 and u!=0:
      el_all.append(e)
      ul_all.append(u)
  el.append(el_geo)
  ul.append(ul_geo)
file = open('geo1.csv', 'w', newline ='')
with file:
    write = csv.writer(file)
    write.writerows([el_all, ul_all])
file.close()


#uni
Xl = range(-k,k, 1)
Xr = range(k,2*k+1,1)
el=[]
ul=[]

el_all=[]
ul_all=[]
for xr in Xr:
  el_uni=[]
  ul_uni=[]
  for xl in Xl:
    e,u = uni(k=k,n=n,xl=xl,xr=xr)
    el_uni.append(e)
    ul_uni.append(u)
    if e!=0 and u!=0:
      el_all.append(e)
      ul_all.append(u)
  el.append(el_uni)
  ul.append(ul_uni)

file = open('uni.csv', 'w', newline ='')
with file:
    write = csv.writer(file)
    write.writerows([el_all, ul_all])
file.close()

#cst
el_all=[]
ul_all=[]
for d in range(k,50):
  e,u = cst(k=k,d=d)
  el_all.append(e)
  ul_all.append(u)

file = open('cst.csv', 'w', newline ='')
with file:
    write = csv.writer(file)
    write.writerows([el_all, ul_all])
file.close()

#akr
delta = 10**(-6)
EPS=[0.65,1.7,2.3]
el_all=[]
ul_all=[]
for eps in EPS:
  e,u =akr(k=k,n=n,eps=eps,delta=delta)
  el_all.append(e)
  ul_all.append(u)

file = open('akr.csv', 'w', newline ='')
with file:
    write = csv.writer(file)
    write.writerows([el_all, ul_all])
file.close()