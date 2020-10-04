import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from tkinter import ttk
import glob
from math import ceil
from PIL import ImageTk, Image

from game.lib.lib import Material, Scene


def do_nothing():
    pass


class Example(tk.Frame):
    ICON_PADDING = 4

    def __init__(self, root):
        super().__init__()
        self.root = root
        self.scene_view = None
        self.current_scene = None
        self.has_changes = False
        self.materials = {mat.name: (tk.IntVar(), mat, None) for mat in Material.from_yaml('../game/data/materials.yaml')}
        for var, mat, button in self.materials.values():
            var.set(1)
        self.object_icons = []
        self.object_buttons = []
        self.material_buttons = []
        self.initUI()

    def initUI(self):
        self.master.title("Scene Builder")
        self.pack(fill=tk.BOTH, expand=True)
        self.build_menu()
        # self.build_left_bar()
        # self.build_right_bar()

        self.bottom_frame = tk.Frame(master=self)
        self.bottom_frame.grid(row=4, column=0, columnspan=6, sticky=tk.E + tk.W + tk.S + tk.N)
        # tk.Label(master=self.bottom_frame, text='TEST', bg='red').pack(fill=tk.BOTH, expand=True)

        self.columnconfigure(2, weight=1)
        # self.columnconfigure(3, pad=7)
        # self.columnconfigure(4, pad=7)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(5, pad=7)

        self.scene_view_frame = tk.Frame(master=self)
        self.scene_view_frame.grid(row=0, column=2, columnspan=2, rowspan=4, padx=5, sticky=tk.E + tk.W + tk.S + tk.N)

        self.build_canvas()

    def build_canvas(self, max_x=100, max_y=100):
        if self.scene_view is not None:
            self.scene_view.destroy()
        self.scene_view = tk.Canvas(self.scene_view_frame, bg="white", width=max_x, height=max_y)
        self.xsb = tk.Scrollbar(self.scene_view_frame, orient="horizontal", command=self.scene_view.xview)
        self.ysb = tk.Scrollbar(self.scene_view_frame, orient="vertical", command=self.scene_view.yview)
        self.scene_view.configure(yscrollcommand=self.ysb.set, xscrollcommand=self.xsb.set)
        self.scene_view.configure(scrollregion=(0, 0, max_x, max_y))
        self.scene_view.grid(row=0, column=0, sticky=tk.E + tk.W + tk.S + tk.N)

        self.scene_view.bind("<ButtonPress-1>", self.scroll_start)
        self.scene_view.bind("<B1-Motion>", self.scroll_move)

        self.xsb.grid(row=1, column=0, sticky="ew")
        self.ysb.grid(row=0, column=1, sticky="ns")
        self.scene_view_frame.grid_rowconfigure(0, weight=1)
        self.scene_view_frame.grid_columnconfigure(0, weight=1)

    def scroll_start(self, event):
        self.scene_view.scan_mark(event.x, event.y)

    def scroll_move(self, event):
        self.scene_view.scan_dragto(event.x, event.y, gain=1)

    def build_left_bar(self):
        self.left_notebook = ttk.Notebook(self)
        self.left_mat_tab = tk.Frame(self.left_notebook)
        self.left_obj_tab = tk.Frame(self.left_notebook)
        self.left_notebook.add(self.left_mat_tab, text='Materials')
        self.left_notebook.add(self.left_obj_tab, text='Objects')
        self.left_notebook.grid(row=0, column=1, rowspan=4, sticky=tk.E + tk.W + tk.S + tk.N)

        # self.label1 = ttk.Label(self.mat_tab, text='Materials').grid(row=1, column=1)
        # self.label2 = ttk.Label(self.obj_tab, text='Objects').grid(row=1, column=1)

        for name, (var, mat, button) in self.materials.items():
            if var.get():
                check=tk.Checkbutton(master=self.left_mat_tab, text=name, variable=var)
                check.pack(side=tk.TOP)

    def new(self):
        # filetypes = [('all files', '.*'), ('yamls', '.yaml')]
        # savepath = filedialog.asksaveasfilename(parent=self,
        #                                         initialdir='../game/data/',
        #                                         title="Please select a file to save the scene:")
        if self.current_scene is not None and self.has_changes:
            response = messagebox.askyesno('Discard Chages?',
                                           '''If you create a new scene now, your existing changes will be discarded. 
                                           Do you really want to discard these changes?''')
            if not response:
                return


        name = simpledialog.askstring('Name', 'What is the name of the new scene?', parent=self)
        length = simpledialog.askfloat('Length', 'How long will the scene be, in meters?', parent=self)
        width = simpledialog.askfloat('Width', 'How wide will the scene be, in meters?', parent=self)
        length *= 10
        width *= 10
        self.build_canvas(length*10+5, width*10+5)
        self.current_scene = Scene(name, (ceil(length), ceil(width)))
        img = ImageTk.PhotoImage(image=Image.fromarray(self.current_scene.layout))
        self.scene_view.create_image((0, 0), anchor='nw', image=img)
        self.scene_view.create_rectangle(0,0,length*10, width*10)
        self.build_right_bar()
        self.build_left_bar()


    def build_right_materials(self):
        for i, (name, (activated, material, button)), in enumerate(self.materials.items()):
            if button is None:
                button = tk.Button(master=self.right_mat_tab, text=name, fg=material.color)
            if activated:
                button.grid(column=i%3, row=i//3, pady=self.ICON_PADDING, padx=self.ICON_PADDING)
            else:
                button.grid_forget()


    def build_right_bar(self):
        self.right_notebook = ttk.Notebook(self)
        self.right_mat_tab = tk.Frame(self.right_notebook)
        self.right_obj_tab = tk.Frame(self.right_notebook)
        self.right_notebook.add(self.right_mat_tab, text='Materials')
        self.right_notebook.add(self.right_obj_tab, text='Objects')
        self.right_notebook.grid(row=0, column=4, rowspan=4, sticky=tk.E + tk.W + tk.S + tk.N)
        self.build_right_materials()
        # self.icon = tk.PhotoImage(file='../game/data/images/3dots.gif', width="50", height="50")
        # button = tk.Button(self, image=self.icon)
        # button.grid(row=0, column=1, pady=self.ICON_PADDING, padx=self.ICON_PADDING)
        for i, icon in enumerate(glob.glob('../game/data/images/*')):
            col = i % 3
            row = i // 3
            print(row, col)
            img = Image.open(icon)
            img = img.resize((50, 50), Image.ANTIALIAS)
            self.object_icons.append(ImageTk.PhotoImage(img))
            self.button = tk.Button(self.right_obj_tab, image=self.object_icons[-1], text=icon.split('/')[-1], compound='top')
            # self.buttons.append(button)
            self.button.grid(row=row, column=col, pady=self.ICON_PADDING, padx=self.ICON_PADDING)

    def build_menu(self):
        self.menubar = tk.Menu(self)
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="New", command=self.new)
        self.filemenu.add_command(label="Open", command=do_nothing)

        self.filemenu.add_command(label="Save", command=do_nothing)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=self.quit)
        self.menubar.add_cascade(label="File", menu=self.filemenu)

        self.helpmenu = tk.Menu(self.menubar, tearoff=0)
        self.helpmenu.add_command(label="Help Index", command=do_nothing)
        self.helpmenu.add_command(label="About...", command=do_nothing)
        self.menubar.add_cascade(label="Help", menu=self.helpmenu)

        self.root.config(menu=self.menubar)


def main():
    root = tk.Tk()
    root.geometry("640x480+300+300")
    app = Example(root)
    root.mainloop()


if __name__ == '__main__':
    main()
