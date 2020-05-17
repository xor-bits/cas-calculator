import tkinter as tk
from PIL import ImageTk,Image
import calc
import io

images = list() 
# images = list((image, tex))
# selected = (button, index)



def on_click_img(button, list_index):
    global selected
    selected = (button, list_index)
    
    tex = images[list_index][1]
    output.delete(0, tk.END)
    output.insert(tk.END, tex)

    print("selected " + tex)

def on_update():
    global selected

    tex = output.get() 
    
    # set the image
    buffer = io.BytesIO()
    calc.print_tex(tex, buffer, (0.0, 0.0, 0.0))
    buffer.seek(0)
    img = ImageTk.PhotoImage(Image.open(buffer))
    images[selected[1]] = (img, tex)
    selected[0].configure(image=images[selected[1]][0])

def wrap_try(tex, command):
    try:
        return command(tex)
    except:
        return ""

def add_image(command=None, printter=calc.print_tex):
    # image
    tex = wrap_try(entry.get(), calc.fix_tex)
    if command != None:
        tex = command(tex)
    if tex == "":
        return
    
    # set output
    output.delete(0, tk.END)
    output.insert(tk.END, tex)
    
    # set the image
    buffer = io.BytesIO()
    printter(tex, buffer, (0.0, 0.0, 0.0))
    buffer.seek(0)
    img = ImageTk.PhotoImage(Image.open(buffer))
    images.append((img, tex))
    index = len(images)-1 # cuz images[-1] wont work here

    # append image
    button = tk.Button(text, command=lambda: on_click_img(button, index), image=images[index][0])
    text.window_create(tk.INSERT, window=button)



root = tk.Tk()
root.title("Project <Nspire on steroids>")

# textbox
text = tk.Text(root, font=('arial', 16))
text.pack(padx = 20, pady = 20)

bottom_frame = tk.Frame()

# latex entry
label_entry = tk.Label(bottom_frame, text="LaTeX input")
label_entry.grid(row=0, column=0)
entry = tk.Entry(bottom_frame, width=40)
entry.grid(row=0, column=1, padx=5, pady=5)
# latex entry solve
label_solve_entry = tk.Label(bottom_frame, text="LaTeX solve for")
label_solve_entry.grid(row=0, column=7)
solve_entry = tk.Entry(bottom_frame, width=10)
solve_entry.insert(0, "x")
solve_entry.grid(row=0, column=8, padx=5, pady=5)
# latex output
label_output = tk.Label(bottom_frame, text="LaTeX output")
label_output.grid(row=1, column=0)
output = tk.Entry(bottom_frame, width=40)
output.grid(row=1, column=1, padx=5, pady=5)

# button
button_insert = tk.Button(bottom_frame, text='Insert', command=lambda: add_image())
button_insert.grid(row=0, column=2)
button_simplify = tk.Button(bottom_frame, text='Simplify', command=lambda: add_image(lambda t: calc.simplify(t)))
button_simplify.grid(row=0, column=3)
button_approx = tk.Button(bottom_frame, text='Approx', command=lambda: add_image(lambda t: calc.approx(t)))
button_approx.grid(row=0, column=4)
button_graph = tk.Button(bottom_frame, text='Graph', command=lambda: add_image(printter=calc.print_plot))
button_graph.grid(row=0, column=5)
button_update = tk.Button(bottom_frame, text='Update', command=on_update)
button_update.grid(row=1, column=2)
button_solve = tk.Button(bottom_frame, text='Solve', command=lambda: add_image(lambda t: calc.solve_for(t, solve_entry.get())))
button_solve.grid(row=0, column=9)

bottom_frame.pack()
root.mainloop()