from tkinter import *
from tkinter.scrolledtext import ScrolledText
from PIL import ImageTk,Image
import calc

# root
root = Tk()
root.title('discord-bot-calc')

input_text = r'\frac{5}{5}'
tempfile_name = 'tempfile.png'

input_image = Label(root)
input_image.grid(row=0, column=2, pady=10)

outputs = list()


def wrap_try(tex, command):
    try:
        return command(tex)
    except:
        return ""

# update outputs
def update_outputs():
    global input_text, tempfile_name
    for output in outputs:
        # processed tex
        tex = output[1](input_text)
        tex = wrap_try(tex, calc.fix_tex)
        if input_text == "":
            continue
        
        # insert to textbox
        output[2].delete(0, END)
        output[2].insert(0, tex)

        # image
        calc.print_tex(tex, tempfile_name, (0.0, 0.0, 0.0))
        image_data = ImageTk.PhotoImage(Image.open(tempfile_name))
        output[0].configure(image=image_data)
        output[0].image = image_data

# show iput and update
def on_modify_input(text):
    global input_text, tempfile_name, input_image
    input_text = text
    input_text = wrap_try(input_text, calc.fix_tex)
    if input_text == "":
        return

    calc.print_tex(text, tempfile_name, (0.0, 0.0, 0.0))
    image_data = ImageTk.PhotoImage(Image.open(tempfile_name))
    input_image.configure(image=image_data)
    input_image.image = image_data

    update_outputs()


# entry
def input_field():
    # description
    tex_input = Label(root, text="Input:")
    tex_input.grid(row=0, column=0)

    # input box
    sv = StringVar()
    sv.set(input_text)
    sv.trace("w", lambda name, index, mode, sv=sv: on_modify_input(sv.get()))
    input_entry = Entry(root, width=50, textvariable=sv)
    input_entry.grid(row=0, column=1)

def output_field(name, row, action):
    global outputs

    # description
    label = Label(root, text=name)
    label.grid(row=row, column=0)

    # image
    image = Label(root)
    image.grid(row=row, column=2, pady=10)

    # textbox
    sv = StringVar()
    sv.set(input_text)
    entry = Entry(root, width=50, textvariable=sv)
    entry.grid(row=row, column=1)

    outputs.append((image, action, entry))


# fields
input_field()
output_field("Simplified", 3, lambda tex: wrap_try(tex, calc.simplify))
output_field("Approximated", 5, lambda tex: wrap_try(tex, calc.approx))

# initial update
on_modify_input(input_text)

# mainloop
root.mainloop()