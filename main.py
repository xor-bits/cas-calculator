
import discord
import os
import calc



with open('dc_token.txt', 'r') as file:
    TOKEN = file.read().replace('\n', '')
client = discord.Client()



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
        if split[0] == "simplify": # simplify=2+2
            command_input = split[1]
            fixed_input = calc.fix_tex(command_input)
            await send_tex(message.channel, fixed_input, "Input")

            simplified_input = calc.simplify(fixed_input)
            await send_tex(message.channel, simplified_input, "Simplified")
        elif split[0] == "solve": # solve=5x^2-2x=5
            command_input = split[1]
            fixed_input = calc.fix_tex(command_input)
            await send_tex(message.channel, fixed_input, "Input")

            simplified_input = calc.solve(fixed_input)
            await send_tex(message.channel, simplified_input, "Solved")
        elif split[0] == "approx": # approx=54/23
            command_input = split[1]
            fixed_input = calc.fix_tex(command_input)
            await send_tex(message.channel, fixed_input, "Input")

            simplified_input = calc.approx(fixed_input)
            await send_tex(message.channel, simplified_input, "Approximated")
        elif split[0] == "set": # set=5x^2-2x=x=43y
            split_new = message.content.split("=",3) # (set) , (5x^2-2x) , (x) , (43y)

            await message.channel.send("```Input: from ({}) set ({}) to ({})```".format(split_new[1], split_new[2], split_new[3]))

            output = calc.subs(split_new[1], split_new[2], split_new[3])
            await send_tex(message.channel, output, "Output")
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