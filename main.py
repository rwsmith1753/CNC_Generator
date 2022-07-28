import tkinter as tk
from tkinter.filedialog import *
import gcodes
import mcodes

class Col0:
  def __init__(self):
    self.orow = 0
    self.newrow = self.orow + 1
    self.svrow = self.newrow + 1
    self.grow = self.svrow + 1
    self.xrow = self.grow + 1
    self.yrow = self.xrow + 1
    self.srow = self.yrow + 1
    self.frow = self.srow + 1
    self.mrow = self.frow + 1
    self.clrow = self.mrow + 1
    self.nlrow = self.clrow + 1

class Col1:
  def __init__(self):
    self.lblrow = 0
    self.comrow = self.lblrow + 1
    self.cbtnrow = self.comrow + 1
    self.grow = self.cbtnrow + 3
    self.xrow = self.grow + 1
    self.yrow = self.xrow + 1
    self.srow = self.yrow + 1
    self.frow = self.srow + 1
    self.mrow = self.frow + 1
    self.clrow = self.mrow + 1
    self.nlrow = self.clrow + 1

col0 = Col0()
col1 = Col1()

def open_file():
  """Open a file for editing."""
  filepath = askopenfilename(
      filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
  )
  if not filepath:
    return
  program.delete("1.0", tk.END)
  with open(filepath, mode="r", encoding="utf-8") as input_file:
    text = input_file.read()
    program.insert(tk.END, text)
  window.title(f"CNC Translator - {filepath}")


#==Create new program, and insert program name
def create_new():
  """Create a new .txt file to store the CNC code"""
  global filepath
  filepath = asksaveasfilename(

    defaultextension=".txt",
    filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
  )
  if not filepath:
    return
  with open(filepath, 'w+'):
    pathsplit = filepath.split('/')
    filename = pathsplit[-1].split('.')
    program.insert(tk.INSERT, f'O{filename[0]}\n')
    prog = program.get(1.0, 'end')
    filepath.write(prog)
    filepath.close()


def save_file():
  with open(filepath, 'w+'):
    prog = program.get(1.0, 'end')
    filepath.write(prog)
    filepath.close()

def ins_com():
  com = comment.get('1.0', 'end-1c')

  program.insert(tk.INSERT, f'(  {com}  )\n')

  comment.delete('1.0', 'end-1c')
    

def add_g():
  selg = lst_g.get(lst_g.curselection())
  if selg == 'None':
    pass
  else:
    g = selg.split(': ')
    cline.insert(tk.INSERT, g[0])

  
  
def add_x():
  x = x_coor.get()
  if isinstance(x,int):
    cline.insert(tk.INSERT, f'X{x}.')  
  else:
    cline.insert(tk.INSERT, f'X{x}')
  x_coor.delete(0, END)

def add_y():
  # y = y_coor.get('1.0', 'end-1c')
  y = y_coor.get()
  
  if isinstance(y,int):
    cline.insert(tk.INSERT, f'Y{y}.')  
  else:
    cline.insert(tk.INSERT, f'Y{y}')
  y_coor.delete(0, END)

def add_s():
  s = speed.get()
  cline.insert(tk.INSERT, f'S{s}')
  speed.delete(0, END)

def add_f():
  f = feed.get()
  cline.insert(tk.INSERT, f'F{f}')
  feed.delete(0, END)
  

def add_m():
  selm = lst_m.get(lst_m.curselection())
  if selm == 'None':
    pass
  else:
    m = selm.split(': ')
    cline.insert(tk.INSERT, m[0])

def new_line():
  code = cline.get()
  program.insert(tk.INSERT, f'{code}\n')
  cline.delete(0, END)




  
#===Window Config  
window = tk.Tk()
window.title('CNC Translator')
window.rowconfigure(0, minsize = 1)
#window.columnconfigure(0, minsize = 200)
window.geometry('800x800')

#===Button Config
frm_buttons = tk.Frame(window, relief=tk.RAISED, bd=1)
frm_buttons.columnconfigure(0, minsize = 300)
frm_buttons.grid(column=0, rowspan = 11, sticky="nsew")

#===Text Box Config
txt_box = tk.Frame(window, bd=1)
txt_box.rowconfigure(0, minsize = 20)
txt_box.grid(column=1, row = 4, rowspan = 8, sticky="nsew")

#=====Program Window
program = tk.Text(window)
program.grid(column=2, row = 0, rowspan = 8, sticky="nsw")
program.insert(tk.INSERT,'%\n')

#=====Comment Window
com_label = tk.Label(text = 'Comment')
com_label.grid(column = 1, row = col1.lblrow, rowspan = 1,sticky = 'sew')
comment = tk.Text(window, height = 3, width = 1)
comment.grid(column=1, row = col1.comrow, rowspan = 1, sticky="nsew")
btn_com = tk.Button(window, text = 'Insert Comment', command = ins_com)
btn_com.grid(column = 1, row = col1.cbtnrow, rowspan = 1, stick = 'new', padx = 5, pady = 5)

#=====Open Program
btn_open = tk.Button(frm_buttons, text = 'Open Program', command = open_file)
btn_open.grid(column = 0, row = col0.orow, sticky = 'nsew', padx = 5, pady = 5)

#=====Create New Program
btn_createnew = tk.Button(frm_buttons, text="Create New Program", command=create_new)
btn_createnew.grid(column=0, row=col0.newrow, sticky="nsew", padx=5, pady=5)

#=====Save Program
btn_save = tk.Button(frm_buttons, text = 'Save Program', command = save_file)
btn_save.grid(column = 0, row = col0.svrow, sticky = 'nsew', padx = 5, pady = 5)

#=====G Code list
#g = StringVar()
#g.set(gcodes2.gcode_list[1])
lst_g = tk.Listbox(frm_buttons)
lst_g.grid(column = 0, row = col0.grow, sticky = 'new')
lst_g.insert(tk.END, 'None')
for i in gcodes.gcode_list:
  lst_g.insert(tk.END, i)
lst_g.select_set(0)
btn_g = tk.Button(window, text = 'Insert G-Code', command = add_g)
btn_g.grid(column = 1, row = col1.grow, rowspan = 1, sticky = 'new', padx = 5, pady = 5)

#=====Code to insert
# cline = tk.Text(txt_box, height = 1, width = 20)
# cline.grid(column = 1, row = 4, sticky = 'nsew', padx = 5, pady = 8)

#=====X Coordinate
x_coor = tk.Entry(window)
x_coor.grid(column = 1, row = col1.grow, sticky = 'sew', padx = 5, pady = 10)
btn_x = tk.Button(frm_buttons, text = 'X-Coordinate', command = add_x)
btn_x.grid(column = 0, row=col0.xrow, sticky = 'nsew', padx = 5, pady = 5)


#=====Y Coordinate
# y_coor = tk.Text(txt_box, height = 1, width = 20)
y_coor = tk.Entry(window)
y_coor.grid(column = 1, row = col1.xrow, sticky = 'new', padx = 5, pady = 10)
btn_y = tk.Button(frm_buttons, text = 'Y-Coordinate', command = add_y)
btn_y.grid(column = 0, row=col0.yrow, sticky = 'nsew', padx = 5, pady = 5)

#=====Speed
speed = tk.Entry(window)
speed.grid(column = 1, row = col1.xrow, sticky = 'sew', padx = 5, pady = 10)
spd_btn = tk.Button(frm_buttons, text = 'Speed (RPM)', command = add_s)
spd_btn.grid(column = 0, row=col0.srow, sticky = 'nsew', padx = 5, pady = 5)

#=====Feed
feed = tk.Entry(window)
feed.grid(column = 1, row = col1.yrow, sticky = 'new', padx = 5, pady = 5)
fd_btn = tk.Button(frm_buttons, text = 'Feed (Inch/Rev)', command = add_f)
fd_btn.grid(column = 0, row=col0.frow, sticky = 'nsew', padx = 5, pady = 5)

#=====M Code
lst_m = tk.Listbox(frm_buttons)
lst_m.grid(column = 0, row = col0.mrow, sticky = 'new')
lst_m.insert(tk.END, 'None')
for i in mcodes.mcode_list:
  lst_m.insert(tk.END, i)
btn_m = tk.Button(window, text = 'Insert M-Code', command = add_m)
btn_m.grid(column = 1, row = col1.yrow, sticky = 'sew')

#=====New line
btn_NL = tk.Button(window, text = 'New Line', command = new_line)
btn_NL.grid(column = 1, row = col1.srow, sticky = 'new', padx = 5, pady = 8)

#=====Code to insert
cline = tk.Entry(window)
cline.grid(column = 1, row = col1.srow, sticky = 'sew', padx = 5, pady = 8)



window.mainloop()