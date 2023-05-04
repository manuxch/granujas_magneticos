#!/bin/env python3
'''Programa para el análisis del tamaño máximo de clusters utilizando grafos.'''

import glob
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import sys
import argparse
from math import sqrt

def mean_cluster_size(file):
    fin = open(file, 'r')
    data = fin.readlines()
    fin.close()
    G = nx.Graph()
    edges = []
    for linea in data[1:]:
        l = linea.split()
        gid = int(l[0])
        if gid == -100:
            continue
        G.add_node(gid)
        for sid in l[9:]:
            if int(sid) == -100:
                continue
            edges.append((gid, int(sid)))
    G.add_edges_from(edges)
    cc = [len(c) for c in sorted(nx.connected_components(G), key=len,
                                 reverse=True)]
    return cc


parser = argparse.ArgumentParser(
    description='Calcula el tamaño medio de clusters en función de la proporción.')
parser.add_argument('-o', '--output', default='max_cluster_sizes.dat',
            help='Archivo de guardado de max_clusultados.')
parser.add_argument('-p', '--prefix', required = True,
            help='Prefijo del nombre de archivos xvc.')
# parser.add_argument('-n', '--nTotal', required = True, type=int,
            # help='Número total de granos en el sistema.')
args = parser.parse_args()

# n_total = args.nTotal
f_out = args.output

file_list = []
for f in glob.glob(args.prefix + '*.xvc'):
    file_list.append(f)
n_files = len(file_list)
file_list.sort()
print(f"Cantidad de archivos a procesar: {len(file_list)}")

max_clus = {}  # clave: n1 valor: [max_clus_1, max_clus_2, ...]
n1On2 = []
mcf = []
mcf_std = []

for f in file_list:
    fl = (f.split('.')[0]).split('_')
    max_clus[int(fl[1])] = [[], []]
    n12 = np.loadtxt(f, usecols=(7), unpack=True)
    u, c = np.unique(n12, return_counts=True)
    n_total = c[0] + c[1]
    max_clus[c[0]][0].append(c[1])


for f in file_list:
    fl = (f.split('.')[0]).split('_')
    lc = mean_cluster_size(f)
    n_total = max_clus[int(fl[1])][0][0] + int(fl[1])
    max_clus[int(fl[1])][1].append(lc[0] / n_total)
    # max_clus[int(fl[1])].append(lc[0] / sum(lc))

for n_p in sorted(max_clus.keys()):
    arr = np.array(max_clus[n_p][1])
    # print(n_p, arr.sum(), n_p/arr.sum(), arr.mean(), arr.std())
    n1On2.append(n_p / max_clus[n_p][0][0])
    mcf.append(arr.mean())
    mcf_std.append(arr.std() / sqrt(arr.size))

fout = open(f_out, 'w')
fout.write("# p_fraction, max_clus_size.mean, max_clus_size.std\n")
for p, m, s in zip(n1On2, mcf, mcf_std):
   sout = f"{p}, {m}, {s}"
   print(sout)
   fout.write(sout + "\n")

fout.close()

