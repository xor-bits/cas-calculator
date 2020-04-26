import discord
import calc



with open('dc_token.txt', 'r') as file:
    TOKEN = file.read().replace('\n', '')
client = discord.Client()


help_string = """
**simplify=<input>**
> ex. simplify=2+2

**solve=<input>=<what>**
> ex. solve=5x^{2}-2x=5

**approx=<input>**
> ex. approx=54/23

**set=<from>=<what>=<to>**
> ex. set=5x^{2}-2x=x=43y

**help=**

**const=**

**helpconst=<const>**
> ex. helpconst=\\\\mathit{c}
"""



# discord bot
async def send_tex(channel, tex, desc):
    calc.print(tex, "tempfile.png")
    file = discord.File(filename="tempfile.png", fp="tempfile.png")
    await channel.send(file=file, content="```{}: {}```".format(desc, tex))

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    try:
        split = message.content.split("=",1)
        if split[0] == "simplify":
            command_input = split[1]
            fixed_input = calc.fix_tex(command_input)
            await send_tex(message.channel, fixed_input, "Input")

            simplified_input = calc.simplify(fixed_input)
            await send_tex(message.channel, simplified_input, "Simplified")
        elif split[0] == "solve":
            command_input = split[1]
            fixed_input = calc.fix_tex(command_input)
            await send_tex(message.channel, fixed_input, "Input")

            simplified_input = calc.solve(fixed_input)
            await send_tex(message.channel, simplified_input, "Solved")
        elif split[0] == "approx":
            command_input = split[1]
            fixed_input = calc.fix_tex(command_input)
            await send_tex(message.channel, fixed_input, "Input")

            simplified_input = calc.approx(fixed_input)
            await send_tex(message.channel, simplified_input, "Approximated")
        elif split[0] == "set":
            split_new = message.content.split("=",3) # (set) , (5x^2-2x) , (x) , (43y)

            await message.channel.send("```Input: from ({}) set ({}) to ({})```".format(split_new[1], split_new[2], split_new[3]))

            output = calc.subs(split_new[1], split_new[2], split_new[3])
            await send_tex(message.channel, output, "Output")
        elif split[0] == "help":
            await message.channel.send(help_string)
        elif split[0] == "const":
            await message.channel.send("lol")
        elif split[0] == "helpconst":
            await message.channel.send("lul")
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