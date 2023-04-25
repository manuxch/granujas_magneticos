#!/bin/env python3
'''Programa para el análisis de RMSD utilizando grafos.'''

import glob
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import sys

# Levanto todos los archivos con datos del grafo (*xvc)
file_list = []
for f in glob.glob('*.xvc'):
    file_list.append(f)
n_files = len(file_list)
file_list.sort()
# Detecto la cantidad de granos (nodos) en el sistema
fin = open(file_list[0], 'r')
data = fin.readlines()
fin.close()
n_granos = len(data) - 1 # resto 1 porque la primera línea es encabezado
print(f'Número total de granos: {n_granos}')

tstep = 0.01

# Proceso la segunda mitad de los archivos para evitar el transitorio
n_tot_files_anal = len(file_list[int(n_files / 2) :])
for i in range(len(file_list) - 1):
    file_0 = file_list[i]
    file_1 = file_list[i + 1]
    step = int(file_0.split('_')[1][:-4])

    gid_0, x_0, y_0, a_0, vx_0, vy_0, w_0, t_0 = np.loadtxt(file_0,
            usecols=(0, 1, 2, 3, 4, 5, 6, 7), unpack=True)
    gid_1, x_1, y_1, a_1, vx_1, vy_1, w_1, t_1 = np.loadtxt(file_1,
            usecols=(0, 1, 2, 3, 4, 5, 6, 7), unpack=True)

    r_0 = np.sqrt(x_0**2 + y_0**2)
    r_1 = np.sqrt(x_1**2 + y_1**2)
    diff = np.diff(r_1 - r_0)
    diff2 = diff**2
    MSD = np.mean(diff2)
    mask_0 = (t_0 == 1)
    mask_1 = (t_1 == 1)
    r_0_1 = r_0[mask_0]
    r_1_1 = r_1[mask_1]
    diff_1 = np.diff(r_1_1 - r_0_1)
    diff_11 = diff_1**2
    MSD_11 = np.mean(diff_11)
    print(i, step * tstep,  MSD, MSD_11)


