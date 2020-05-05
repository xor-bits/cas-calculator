from __future__ import division
import sympy as sp
from sympy.parsing.latex import parse_latex
from sympy.utilities.lambdify import lambdify, implemented_function

import matplotlib
matplotlib.use("Agg")
from matplotlib import pyplot as plt

import pandas as pd
import numpy as np



sp.symbols('x y z t')

# constants
constants = pd.read_excel('constants.xlsx')
constants = constants.dropna()



with open('dc_token.txt', 'r') as file:
    TOKEN = file.read().replace('\n', '')


def list_constants():
    return constants

def eval_constants(tex):
    processed_tex = tex
    while True:
        keep = False
        for index, row in constants.iterrows():
            # print("replace {} with {}".format(row['LaTeX'], row['Evaluates to']))
            processed_tex = processed_tex.replace(row['LaTeX'], row['Evaluates to'])
            keep = True
        if (keep):
            break

    return sp.latex(processed_tex)


# sympy
def fix_tex(tex):
    return sp.latex(tex.replace("\\left(", "(").replace("\\right)", ")"))

def print_tex(tex, file, color=(1.0, 1.0, 1.0)):
    plt.clf()
    plt.cla()
    plt.close()

    #add text
    plt.text(0, 0.6, r"$%s$" % tex, fontsize = 1000, color=color)
    plt.axis('off')

    #hide axes
    fig = plt.gca()
    fig.axes.get_xaxis().set_visible(False)
    fig.axes.get_yaxis().set_visible(False)
    plt.savefig(file, dpi=2, transparent=True, bbox_inches='tight', pad_inches=0)

def print_plot(tex, file, color=(1.0, 0.0, 0.0)):
    plt.clf()
    plt.cla()
    plt.close()

    #add graph
    time = np.arange(0, 10, 0.1);
    f = lambdify('x', parse_latex(tex), 'numpy')
    amplitude = f(time)
    plt.plot(time, amplitude)
    plt.grid(True, which='both')
    plt.axhline(y=0, color='k')
    plt.savefig(file, dpi=50)

def simplify(tex):
    tex = fix_tex(tex)

    expr = parse_latex(tex)
    return sp.latex(sp.simplify(expr))

def approx(tex):
    tex = fix_tex(tex)

    # constants
    processed_tex = eval_constants(tex)

    return sp.latex(parse_latex(processed_tex).doit().evalf(15))

def solve(tex):
    tex = fix_tex(tex)
    
    return sp.latex(sp.solve(parse_latex(tex)))

def subs(tex, from_tex, to_tex):
    from_tex = fix_tex(from_tex)
    to_tex = fix_tex(to_tex)
    tex = fix_tex(tex)
    
    return sp.latex(parse_latex(tex).subs(parse_latex(from_tex), parse_latex(to_tex)))