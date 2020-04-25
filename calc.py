from __future__ import division
from sympy import latex, Symbol, symbols, solve
from sympy.parsing.latex import parse_latex
from matplotlib import pyplot as plt
from sympy import simplify as simply



symbols('x y z t')

# constants
Symbol('c_{\mathit{c}}')
Symbol('c_{\mathit{m}}')
Symbol('c_{\mathit{s}}')



# sympy
def fix_tex(tex):
    return latex(tex.replace("\\left(", "(").replace("\\right)", ")"))

def print(tex, file):
    tex = fix_tex(tex)

    plt.clf()
    plt.cla()
    plt.close()

    #add text
    plt.text(0, 0.6, r"$%s$" % tex, fontsize = 1000, color=(1.0, 1.0, 1.0))
    plt.axis('off')

    #hide axes
    fig = plt.gca()
    fig.axes.get_xaxis().set_visible(False)
    fig.axes.get_yaxis().set_visible(False)
    plt.savefig(file, dpi=2, transparent=True, bbox_inches='tight', pad_inches=0)
    plt.clf()

def simplify(tex):
    tex = fix_tex(tex)

    expr = parse_latex(tex)
    return latex(simply(expr))

def approx(tex):
    tex = fix_tex(tex)

    # constants
    processed_tex = tex
    processed_tex = processed_tex.replace(r'c_{\mathit{c}}', r'(299792458\cdot\frac{c_{\mathit{m}}}{c_{\mathit{s}}})')

    return latex(parse_latex(processed_tex).doit().evalf(15))

def f_solve(tex):
    tex = fix_tex(tex)
    
    return latex(solve(parse_latex(tex)))

def f_subs(tex, from_tex, to_tex):
    from_tex = fix_tex(from_tex)
    to_tex = fix_tex(to_tex)
    tex = fix_tex(tex)
    
    return latex(parse_latex(tex).subs(parse_latex(from_tex), parse_latex(to_tex)))