#!/bin/env python3
'''Programa para el análisis del tamaño máximo de clusters utilizando grafos.'''

import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.cm as cm
import numpy as np
mpl.rcParams["errorbar.capsize"] = 5
mpl.rcParams["text.usetex"] = True

norm = mpl.colors.Normalize(vmin=0, vmax=1)
cmap = cm.Greens
v2c = cm.ScalarMappable(norm=norm, cmap=cmap)

p_350, mcs_350, sdmcs_350 = np.loadtxt('disks-350.out', delimiter=',', unpack=True)
p_525, mcs_525, sdmcs_525 = np.loadtxt('disks-525.out', delimiter=',', unpack=True)
p_700, mcs_700, sdmcs_700 = np.loadtxt('disks-700.out', delimiter=',', unpack=True)
tp_350, tmcs_350, tsdmcs_350 = np.loadtxt('3-350.out', delimiter=',', unpack=True)
tp_525, tmcs_525, tsdmcs_525 = np.loadtxt('3-525.out', delimiter=',', unpack=True)
tp_700, tmcs_700, tsdmcs_700 = np.loadtxt('3-700.out', delimiter=',', unpack=True)
sp_350, smcs_350, ssdmcs_350 = np.loadtxt('4-350.out', delimiter=',', unpack=True)
sp_525, smcs_525, ssdmcs_525 = np.loadtxt('4-525.out', delimiter=',', unpack=True)
sp_700, smcs_700, ssdmcs_700 = np.loadtxt('4-700.out', delimiter=',', unpack=True)
pp_350, pmcs_350, psdmcs_350 = np.loadtxt('5-350.out', delimiter=',', unpack=True)
pp_525, pmcs_525, psdmcs_525 = np.loadtxt('5-525.out', delimiter=',', unpack=True)
pp_700, pmcs_700, psdmcs_700 = np.loadtxt('5-700.out', delimiter=',', unpack=True)

fig, ax = plt.subplots(2,2, figsize=(10, 8), sharey=True)
alp = 0.5
ax[0, 0].errorbar(p_350, mcs_350, yerr=sdmcs_350, fmt='o-', color=v2c.to_rgba(0.6), label=r"$\phi = 0.214$", alpha=alp)
ax[0, 0].errorbar(p_525, mcs_525, yerr=sdmcs_525, fmt='o-', color=v2c.to_rgba(0.8), label=r"$\phi = 0.321$", alpha=alp)
ax[0, 0].errorbar(p_700, mcs_700, yerr=sdmcs_700, fmt='o-', color=v2c.to_rgba(1.0), label=r"$\phi = 0.428$", alpha=alp)
ax[0,0].legend(title='Discos', loc=2)
ax[0, 0].grid()
# ax[0, 0].set_ylim([0, 1.1])
ax[0, 0].set_ylabel(r"$\max(C_s)/N_T$")
ax[0, 1].errorbar(tp_350, tmcs_350, yerr=tsdmcs_350, fmt='^-', color=v2c.to_rgba(0.6), label=r"$\phi = 0.214$", alpha=alp)
ax[0, 1].errorbar(tp_525, tmcs_525, yerr=tsdmcs_525, fmt='^-', color=v2c.to_rgba(0.8), label=r"$\phi = 0.321$", alpha=alp)
ax[0, 1].errorbar(tp_700, tmcs_700, yerr=tsdmcs_700, fmt='^-', color=v2c.to_rgba(1.0), label=r"$\phi = 0.428$", alpha=alp)
ax[0, 1].legend(title='Triángulos', loc=2)
ax[0, 1].grid()
# ax[0, 1].set_ylim([0, 1.1])
ax[1, 0].errorbar(sp_350, smcs_350, yerr=ssdmcs_350, fmt='s-', color=v2c.to_rgba(0.6), label=r"$\phi = 0.214$", alpha=alp)
ax[1, 0].errorbar(sp_525, smcs_525, yerr=ssdmcs_525, fmt='s-', color=v2c.to_rgba(0.8), label=r"$\phi = 0.321$", alpha=alp)
ax[1, 0].errorbar(sp_700, smcs_700, yerr=ssdmcs_700, fmt='s-', color=v2c.to_rgba(1.0), label=r"$\phi = 0.428$", alpha=alp)
ax[1, 0].legend(title='Cuadrados', loc=2)
ax[1, 0].grid()
ax[1, 0].set_ylabel(r"$\max(C_s)/N_T$")
ax[1, 0].set_xlabel(r"$n_1 / n_2$")
ax[1, 1].errorbar(pp_350, pmcs_350, yerr=psdmcs_350, fmt='p-', color=v2c.to_rgba(0.6), label=r"$\phi = 0.214$", alpha=alp)
ax[1, 1].errorbar(pp_525, pmcs_525, yerr=psdmcs_525, fmt='p-', color=v2c.to_rgba(0.8), label=r"$\phi = 0.321$", alpha=alp)
ax[1, 1].errorbar(pp_700, pmcs_700, yerr=psdmcs_700, fmt='p-', color=v2c.to_rgba(1.0), label=r"$\phi = 0.428$", alpha=alp)
ax[1, 1].legend(title='Pentágonos', loc=2)
ax[1, 1].grid()
ax[1, 1].set_xlabel(r"$n_1 / n_2$")
plt.savefig("fig-01.pdf", bbox_inches="tight")

fig, ax = plt.subplots(1,3, sharey=True, figsize=(10, 4))

ax[0].errorbar(p_350, mcs_350, yerr=sdmcs_350, fmt='o-', label=r"Discos", alpha=alp)
ax[0].errorbar(tp_350, tmcs_350, yerr=tsdmcs_350, fmt='^-', label=r"Triángulos", alpha=alp)
ax[0].errorbar(sp_350, smcs_350, yerr=ssdmcs_350, fmt='s-', label=r"Cuadrados", alpha=alp)
ax[0].errorbar(pp_350, pmcs_350, yerr=psdmcs_350, fmt='p-', label=r"Pentágonos", alpha=alp)
ax[0].legend(title=r"$\phi = 0.214$", loc=2, fontsize=9)
ax[0].set_ylabel(r"$\max(C_s)/N_T$")
ax[0].set_xlabel(r"$n_1 / n_2$")
ax[0].grid()
ax[1].errorbar(p_525, mcs_525, yerr=sdmcs_525, fmt='o-', label=r"Discos", alpha=alp)
ax[1].errorbar(tp_525, tmcs_525, yerr=tsdmcs_525, fmt='^-', label=r"Triángulos", alpha=alp)
ax[1].errorbar(sp_525, smcs_525, yerr=ssdmcs_525, fmt='s-', label=r"Cuadrados", alpha=alp)
ax[1].errorbar(pp_525, pmcs_525, yerr=psdmcs_525, fmt='p-', label=r"Pentágonos", alpha=alp)
ax[1].legend(title=r"$\phi = 0.321$", loc=2, fontsize=9)
ax[1].set_xlabel(r"$n_1 / n_2$")
ax[1].grid()
ax[2].errorbar(p_700, mcs_700, yerr=sdmcs_700, fmt='o-', label=r"Discos", alpha=alp)
ax[2].errorbar(tp_700, tmcs_700, yerr=tsdmcs_700, fmt='^-', label=r"Triángulos", alpha=alp)
ax[2].errorbar(sp_700, smcs_700, yerr=ssdmcs_700, fmt='s-', label=r"Cuadrados", alpha=alp)
ax[2].errorbar(pp_700, pmcs_700, yerr=psdmcs_700, fmt='p-', label=r"Pentágonos", alpha=alp)
ax[2].legend(title=r"$\phi = 0.428$", loc=2, fontsize=9)
ax[2].grid()
ax[2].set_xlabel(r"$n_1 / n_2$")
plt.savefig("fig-02.pdf", bbox_inches="tight")
