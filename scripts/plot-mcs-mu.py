#!/bin/env python3
'''Programa para el análisis del tamaño máximo de clusters utilizando grafos.'''

import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
mpl.rcParams["errorbar.capsize"] = 5
mpl.rcParams["text.usetex"] = True

d_mu, d_mcs, d_sdmcs = np.loadtxt('disks-mu.out', delimiter=',', unpack=True)
t_mu, t_mcs, t_sdmcs = np.loadtxt('3-mu.out', delimiter=',', unpack=True)
s_mu, s_mcs, s_sdmcs = np.loadtxt('4-mu.out', delimiter=',', unpack=True)
p_mu, p_mcs, p_sdmcs = np.loadtxt('5-mu.out', delimiter=',', unpack=True)

# fig, ax = plt.subplots(2,2, figsize=(10, 8), sharey=True)
alp = 0.5
plt.errorbar(d_mu, d_mcs, yerr=d_sdmcs, fmt='o-', alpha=alp, label=r"Discos")
plt.errorbar(t_mu, t_mcs, yerr=t_sdmcs, fmt='^-', alpha=alp, label=r"Triángulos")
plt.errorbar(s_mu, s_mcs, yerr=s_sdmcs, fmt='s-', alpha=alp, label=r"Cuadrados")
plt.errorbar(p_mu, p_mcs, yerr=p_sdmcs, fmt='p-', alpha=alp, label=r"Pentágonos")
plt.xlabel(r"$|\mu_1/\mu_2|$")
plt.ylabel(r"$\max(C_s)/N_T$")
plt.title(r"$\phi = 0.321$")
plt.grid()
plt.legend()
plt.savefig("fig-03.pdf", bbox_inches="tight")
