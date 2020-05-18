import tkinter as tk
from tkinter import filedialog as fd
from PIL import ImageTk,Image
import calc
import io
import pickle

images = list() 
# images = list((image, tex, button, (bool)graph))
# selected = (button, index)



def save():
    file = fd.asksaveasfile(mode='wb', initialfile='document1.np2', filetypes=[('NSpire2 files', '.np2')])
    if file is not None:
        # text
        # file.write(pickle.dumps(text))

        # buttons
        l = list()
        for (key, name, index) in text.dump("1.0", "end", window=True):
            for (image, tex, button, graph) in images:
                if name == str(button):
                    l.append((index, tex, graph))
                    break;

        file.write(pickle.dumps((l, text.get("1.0", "end"))))
    file.close()

def open():
    file = fd.askopenfile(mode='rb', filetypes=[('NSpire2 files', '.np2')])
    if file is not None:
        content = file.read()
        l = pickle.loads(content)
        
        # insert text
        text.delete("1.0", "end")
        text.insert("end", str(l[1]))
        print(l)

        # insert buttons
        for (index, tex, graph) in l[0]:
            add_image(tex, graph=graph, text_index=index)
        
    file.close()

def on_click_img(button, list_index):
    global selected
    selected = (button, list_index)
    
    tex = images[list_index][1]
    output.delete(0, tk.END)
    output.insert(tk.END, tex)

    print('selected ' + tex)

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

def add_image(tex, command=None, graph=False, text_index=tk.INSERT):
    # image
    tex = wrap_try(tex, calc.fix_tex)
    if command != None:
        tex = command(tex)
    if tex == "":
        return
    
    # set output
    output.delete(0, tk.END)
    output.insert(tk.END, tex)
    
    # set the image
    buffer = io.BytesIO()
    if graph:
        calc.print_plot(tex, buffer, (0.0, 0.0, 0.0))
    else:
        calc.print_tex(tex, buffer, (0.0, 0.0, 0.0))
    buffer.seek(0)
    img = ImageTk.PhotoImage(Image.open(buffer))
    index = len(images)

    # append image
    button = tk.Button(text, command=lambda: on_click_img(button, index), image=img)
    wnd = text.window_create(text_index, window=button)
    images.append((img, tex, button, graph))



root = tk.Tk()
root.title('Project <Nspire on steroids>')
root.resizable(False, False)

# save/open
top_frame = tk.Frame()
menubutton = tk.Menubutton(top_frame, text = 'File')
menubutton.pack()
menubutton.menu = tk.Menu(menubutton, tearoff = 0)
menubutton['menu']=menubutton.menu
menubutton.menu.add_command(label = 'Save', command=save)
menubutton.menu.add_command(label = 'Open', command=open)
menubutton.grid()
top_frame.grid()

# textbox
text = tk.Text(root, font=('arial', 16))
text.grid(padx = 5, pady = 5)

bottom_frame = tk.Frame()

# latex entry
label_entry = tk.Label(bottom_frame, text='LaTeX input')
label_entry.grid(row=0, column=0)
entry = tk.Entry(bottom_frame, width=40)
entry.grid(row=0, column=1, padx=5, pady=5)
# latex entry solve
label_solve_entry = tk.Label(bottom_frame, text='LaTeX solve for')
label_solve_entry.grid(row=0, column=7)
solve_entry = tk.Entry(bottom_frame, width=10)
solve_entry.insert(0, 'x')
solve_entry.grid(row=0, column=8, padx=5, pady=5)
# latex output
label_output = tk.Label(bottom_frame, text='LaTeX output')
label_output.grid(row=1, column=0)
output = tk.Entry(bottom_frame, width=40)
output.grid(row=1, column=1, padx=5, pady=5)

# button
button_insert = tk.Button(bottom_frame, text='Insert', command=lambda: add_image(entry.get()))
button_insert.grid(row=0, column=2)
button_simplify = tk.Button(bottom_frame, text='Simplify', command=lambda: add_image(entry.get(), lambda t: calc.simplify(t)))
button_simplify.grid(row=0, column=3)
button_approx = tk.Button(bottom_frame, text='Approx', command=lambda: add_image(entry.get(), lambda t: calc.approx(t)))
button_approx.grid(row=0, column=4)
button_graph = tk.Button(bottom_frame, text='Graph', command=lambda: add_image(entry.get(), graph=True))
button_graph.grid(row=0, column=5)
button_update = tk.Button(bottom_frame, text='Update', command=on_update)
button_update.grid(row=1, column=2)
button_solve = tk.Button(bottom_frame, text='Solve', command=lambda: add_image(entry.get(), lambda t: calc.solve_for(t, solve_entry.get())))
button_solve.grid(row=0, column=9)

bottom_frame.grid()
root.mainloop()