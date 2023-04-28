#!/bin/env python3
'''Programa para el análisis del tamaño máximo de clusters utilizando grafos.'''

import glob
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import sys
import argparse

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
    description='Calcula el tamaño medio de clusters en función del cociente mu1/m2.')
parser.add_argument('-o', '--output', default='max_cluster_sizes-mu1.dat',
            help='Archivo de guardado de resultados.')
parser.add_argument('-p', '--prefix', required = True,
            help='Prefijo del nombre de archivos xvc.')
parser.add_argument('-n', '--nTotal', required = True, type=int,
            help='Número total de granos en el sistema.')
args = parser.parse_args()

n_total = args.nTotal
f_out = args.output

file_list = []
for f in glob.glob(args.prefix + '*.xvc'):
    file_list.append(f)
n_files = len(file_list)
file_list.sort()
print(f"Cantidad de archivos a procesar: {len(file_list)}")

res = {}
mu1 = []
mcf = []
mcf_std = []

for f in file_list:
    fl = (f.split('.')[0]).split('_')
    res[int(fl[2])] = []

for f in file_list:
    fl = (f.split('.')[0]).split('_')
    lc = mean_cluster_size(f)
    res[int(fl[2])].append(lc[0] / n_total)
    # res[int(fl[1])].append(lc[0] / sum(lc))

for mu in sorted(res.keys()):
    arr = np.array(res[mu])
    print(mu, arr.sum(), arr.mean(), arr.std())
    mu1.append(mu / 1000)
    mcf.append(arr.mean())
    mcf_std.append(arr.std())

fout = open(f_out, 'w')
fout.write("# p_fraction, max_clus_size.mean, max_clus_size.std\n")
for p, m, s in zip(mu1, mcf, mcf_std):
   sout = f"{p}, {m}, {s}\n"
   fout.write(sout)

fout.close()

