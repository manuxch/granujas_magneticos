#!/usr/bin/env python3

import argparse
from sympy import symbols, sin, pi
from sympy.solvers import solve

parser = argparse.ArgumentParser(
    description='Calcula el radio de un polígono regular de n lados equivalente a un círculo de radio r')
parser.add_argument('-r', type=float, default=0.5, required=False,
                    help='Radio del disco.')
parser.add_argument('-n', type=int, default=3, required=True,
                    help='Número de lados del polígono regular.')

args = parser.parse_args()

r_disk = args.r
n_lados = args.n

r = symbols('r', real=True, positive=True)
n = symbols('n', integer=True, positive=True)

def area_polygon(r, n):
    return n * r**2 * sin(2 * pi / n) / 2

def area_disk(r):
    return pi * r**2

sol = solve(area_polygon(r, n_lados) - area_disk(r_disk), r)
print(f"Radio del disco: {r_disk}")
print(f"Número de lados del polígono de área equivalente: {n_lados}")
print(f"Radio solución: {sol[0]}")
