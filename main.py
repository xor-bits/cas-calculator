from __future__ import division
from sympy import *
from sympy.parsing.latex import parse_latex
from matplotlib import pyplot as plt
import discord
import os



symbols('x y z t')

# constants
Symbol('c_{\mathit{c}}')
Symbol('c_{\mathit{m}}')
Symbol('c_{\mathit{s}}')

with open('dc_token.txt', 'r') as file:
    TOKEN = file.read().replace('\n', '')
client = discord.Client()



# sympy
def f_fix_tex(tex):
    return latex(tex.replace("\\left(", "(").replace("\\right)", ")"))

def f_print(tex, file):
    tex = f_fix_tex(tex)

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

def f_simplify(tex):
    tex = f_fix_tex(tex)

    expr = parse_latex(tex)
    return latex(simplify(expr))

def f_approx(tex):
    tex = f_fix_tex(tex)

    # constants
    processed_tex = tex
    processed_tex = processed_tex.replace(r'c_{\mathit{c}}', r'(299792458\cdot\frac{c_{\mathit{m}}}{c_{\mathit{s}}})')

    return latex(parse_latex(processed_tex).doit().evalf(15))

def f_solve(tex):
    tex = f_fix_tex(tex)
    
    return latex(solve(parse_latex(tex)))

def f_subs(tex, from_tex, to_tex):
    from_tex = f_fix_tex(from_tex)
    to_tex = f_fix_tex(to_tex)
    tex = f_fix_tex(tex)
    
    return latex(parse_latex(tex).subs(parse_latex(from_tex), parse_latex(to_tex)))



# discord bot
async def f_send_tex(channel, tex, desc):
        f_print(tex, "tempfile.png")
        file = discord.File(filename="tempfile.png", fp="tempfile.png")
        await channel.send(file=file, content="```{}: {}```".format(desc, tex))

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    try:
        split = message.content.split("=",1)
        if split[0] == "simplify": # simplify=2+2
            command_input = split[1]
            fixed_input = f_fix_tex(command_input)
            await f_send_tex(message.channel, fixed_input, "Input")

            simplified_input = f_simplify(fixed_input)
            await f_send_tex(message.channel, simplified_input, "Simplified")
        elif split[0] == "solve": # solve=5x^2-2x=5
            command_input = split[1]
            fixed_input = f_fix_tex(command_input)
            await f_send_tex(message.channel, fixed_input, "Input")

            simplified_input = f_solve(fixed_input)
            await f_send_tex(message.channel, simplified_input, "Solved")
        elif split[0] == "approx": # approx=54/23
            command_input = split[1]
            fixed_input = f_fix_tex(command_input)
            await f_send_tex(message.channel, fixed_input, "Input")

            simplified_input = f_approx(fixed_input)
            await f_send_tex(message.channel, simplified_input, "Approximated")
        elif split[0] == "set": # set=5x^2-2x=x=43y
            split_new = message.content.split("=",3) # (set) , (5x^2-2x) , (x) , (43y)

            await message.channel.send("```Input: from ({}) set ({}) to ({})```".format(split_new[1], split_new[2], split_new[3]))

            output = f_subs(split_new[1], split_new[2], split_new[3])
            await f_send_tex(message.channel, output, "Output")
    except Exception as e:
        await message.channel.send("```Malformed LaTeX {}```".format(split[1]))
        print('exception: {}'.format(e))

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)