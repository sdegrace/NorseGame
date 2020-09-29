import tkinter as tk
from tkinter import ttk
import glob
from PIL import ImageTk, Image

from game.lib.lib import Material


def do_nothing():
    pass


class Example(tk.Frame):
    ICON_PADDING = 4

    def __init__(self, root):
        super().__init__()
        self.root = root
        self.materials = {mat.name: (tk.IntVar(), mat) for mat in Material.from_yaml('../game/data/materials.yaml')}
        for var, _ in self.materials.values():
            var.set(1)
        self.icons = []
        self.buttons = []
        self.initUI()

    def initUI(self):
        self.master.title("Scene Builder")
        self.pack(fill=tk.BOTH, expand=True)
        self.build_menu()
        self.build_left_bar()
        self.add_icons()

        self.columnconfigure(2, weight=1)
        # self.columnconfigure(3, pad=7)
        # self.columnconfigure(4, pad=7)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(5, pad=7)

        self.scene_view = tk.Canvas(self, bg="white")
        self.scene_view.grid(row=0, column=2, columnspan=2, rowspan=4, padx=5, sticky=tk.E + tk.W + tk.S + tk.N)

        # hbtn = tk.Button(self, text="Help")
        # hbtn.grid(row=5, column=0, padx=5)
        #
        # obtn = tk.Button(self, text="OK")
        # obtn.grid(row=5, column=3)

    def build_left_bar(self):
        self.notebook = ttk.Notebook(self)
        self.mat_tab = tk.Frame(self.notebook)
        self.obj_tab = tk.Frame(self.notebook)
        self.notebook.add(self.mat_tab, text='Materials')
        self.notebook.add(self.obj_tab, text='Objects')
        self.notebook.grid(row=0, column=1, rowspan=4,  sticky=tk.E + tk.W + tk.S + tk.N)

        # self.label1 = ttk.Label(self.mat_tab, text='Materials').grid(row=1, column=1)
        # self.label2 = ttk.Label(self.obj_tab, text='Objects').grid(row=1, column=1)

        for name, (var, mat) in self.materials.items():
            if var.get():
                check=tk.Checkbutton(master=self.mat_tab, text=name, variable=var)
                check.pack(side=tk.TOP)



    # def build_bottom_bar(self):
    #     for name, (var, mat) in self.materials.items():


    def add_icons(self):
        # self.icon = tk.PhotoImage(file='../game/data/images/3dots.gif', width="50", height="50")
        # button = tk.Button(self, image=self.icon)
        # button.grid(row=0, column=1, pady=self.ICON_PADDING, padx=self.ICON_PADDING)
        for i, icon in enumerate(glob.glob('../game/data/images/*')):
            col = i % 3
            row = i // 3
            print(row, col)
            img = Image.open(icon)
            img = img.resize((50, 50), Image.ANTIALIAS)
            self.icons.append(ImageTk.PhotoImage(img))
            self.button = tk.Button(self, image=self.icons[-1], text=icon, compound='top')
            # self.buttons.append(button)
            self.button.grid(row=row, column=4 + col, pady=self.ICON_PADDING, padx=self.ICON_PADDING)

    def build_menu(self):
        self.menubar = tk.Menu(self)
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="New", command=do_nothing)
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
