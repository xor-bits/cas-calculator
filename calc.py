from __future__ import division
from sympy import latex, Symbol, symbols, solve
from sympy.parsing.latex import parse_latex
import matplotlib
matplotlib.use("Agg")
from matplotlib import pyplot as plt
from sympy import simplify as simply
import pandas as pd



symbols('x y z t')

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

    return latex(processed_tex)


# sympy
def fix_tex(tex):
    return latex(tex.replace("\\left(", "(").replace("\\right)", ")"))

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

def simplify(tex):
    tex = fix_tex(tex)

    expr = parse_latex(tex)
    return latex(simply(expr))

def approx(tex):
    tex = fix_tex(tex)

    # constants
    processed_tex = eval_constants(tex)

    return latex(parse_latex(processed_tex).doit().evalf(15))

def f_solve(tex):
    tex = fix_tex(tex)
    
    return latex(solve(parse_latex(tex)))

def f_subs(tex, from_tex, to_tex):
    from_tex = fix_tex(from_tex)
    to_tex = fix_tex(to_tex)
    tex = fix_tex(tex)
    
    return latex(parse_latex(tex).subs(parse_latex(from_tex), parse_latex(to_tex)))