import tkinter as tk
from PIL import ImageTk,Image
import calc
import io

images = list()



def wrap_try(tex, command):
    try:
        return command(tex)
    except:
        return ""

def add_image(tex, command=None, printter=calc.print_tex):
    # image
    tex = wrap_try(tex, calc.fix_tex)
    if command != None:
        tex = command(tex)
    if tex == "":
        return
    buffer = io.BytesIO()
    printter(tex, buffer, (0.0, 0.0, 0.0))
    buffer.seek(0)
    img = ImageTk.PhotoImage(Image.open(buffer))
    images.append(img)

    text.image_create(tk.END, image = images[-1]) # Example 1
    # text.window_create(tk.END, window = tk.Label(text, image = img)) # Example 2



root = tk.Tk()
root.title("Project <Nspire on steroids>")

# textbox
text = tk.Text(root)
text.pack(padx = 20, pady = 20)

bottom_frame = tk.Frame()

# latex entry
entry = tk.Entry(bottom_frame, width=40)
entry.grid(row=0, column=0, padx=5, pady=5)

# button
button_insert = tk.Button(bottom_frame, text='Insert', command=lambda: add_image(entry.get()))
button_insert.grid(row=0, column=1)
button_simplify = tk.Button(bottom_frame, text='Simplify', command=lambda: add_image(entry.get(), calc.simplify))
button_simplify.grid(row=0, column=2)
button_approx = tk.Button(bottom_frame, text='Approx', command=lambda: add_image(entry.get(), calc.approx))
button_approx.grid(row=0, column=3)
button_solve = tk.Button(bottom_frame, text='Solve', command=lambda: add_image(entry.get(), calc.solve))
button_solve.grid(row=0, column=4)
button_graph = tk.Button(bottom_frame, text='Graph', command=lambda: add_image(entry.get(), printter=calc.print_plot))
button_graph.grid(row=0, column=5)

bottom_frame.pack()
root.mainloop()