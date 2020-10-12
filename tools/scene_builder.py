import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox, colorchooser
from tkinter import ttk
from math import ceil, floor, sqrt
from tools.image_processing_tools import *

from tools.mixins import Painting, Panel, Canvas
from game.lib.lib import Material, Scene


def rounddown(x):
    return int(floor(x / 10.0)) * 10


def do_nothing():
    pass


class Example(tk.Frame, Painting, Panel, Canvas):
    ICON_PADDING = 4

    def __init__(self, root, scaling_factor=10):
        super().__init__()
        self.root = root
        self.scaling_factor = scaling_factor
        default_button = tk.Button()
        self.fg_default = default_button.cget('foreground')
        self.bg_default = default_button.cget('background')
        self.active_shape_fg = None
        self.active_shape_bg = None
        self.active_shape_fg = self.fg_default
        self.active_shape_bg = self.bg_default
        self.current_2pt_1st_pt = None
        self.current_3pt_1st_pt = None
        self.current_3pt_2nd_pt = None
        self.current_bound_paint = do_nothing
        self.active_shape_button = None

        self.scene_view = None
        self.current_paint_stroke = 0
        self.current_scene = None
        self.has_changes = False
        self.current_draw_shape = None
        self.materials = {mat.name: (tk.IntVar(), mat, None) for mat in
                          Material.from_yaml('../game/data/materials.yaml')}
        self.current_material = None
        self.current_object = None
        for var, mat, button in self.materials.values():
            var.set(1)
        self.object_icons = []
        self.object_buttons = []
        self.material_buttons = []
        self.shape_buttons = []
        self.master.title("Scene Builder")
        self.pack(fill=tk.BOTH, expand=True)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self.init_UI()
        self.shape_mapping = {'circle': circle,
                              'line': line,
                              'rectangle': rectangle,
                              'arc': arc}

    def init_UI(self):
        self.build_menu()
        # self.build_left_bar()
        # self.build_right_bar()

        self.bottom_frame = tk.Frame(master=self)
        self.bottom_frame.grid(row=1, column=0, columnspan=3, sticky=tk.E + tk.W + tk.S + tk.N)
        # tk.Label(master=self.bottom_frame, text='TEST', bg='red').pack(fill=tk.BOTH, expand=True)

        self.left_notebook = ttk.Notebook(self)
        self.left_notebook.grid(row=0, column=0, sticky=tk.E + tk.W + tk.S + tk.N)

        self.right_notebook = ttk.Notebook(self)
        self.right_notebook.grid(row=0, column=2, sticky=tk.E + tk.W + tk.S + tk.N)

        self.main_editor_frame = tk.Frame(master=self)
        self.main_editor_frame.grid(row=0, column=1, padx=5, sticky=tk.E + tk.W + tk.S + tk.N)

    def build_menu(self):
        self.menubar = tk.Menu(self)
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="New Scene", command=self.new_scene)
        self.filemenu.add_command(label="New Object", command=self.new_object)
        self.filemenu.add_command(label='New Material', command=self.new_material)
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

    def new_scene(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.init_UI()
        # filetypes = [('all files', '.*'), ('yamls', '.yaml')]
        # savepath = filedialog.asksaveasfilename(parent=self,
        #                                         initialdir='../game/data/',
        #                                         title="Please select a file to save the scene:")
        if self.current_scene is not None and self.has_changes:
            response = messagebox.askyesno('Discard Changes?',
                                           '''If you create a new scene now, your existing changes will be discarded. 
                                           Do you really want to discard these changes?''')
            if not response:
                return

        name = simpledialog.askstring('Name', 'What is the name of the new scene?', parent=self)
        length = simpledialog.askfloat('Length', 'How long will the scene be, in meters?', parent=self)
        width = simpledialog.askfloat('Width', 'How wide will the scene be, in meters?', parent=self)
        length *= 10
        width *= 10
        self.build_canvas(length * 10, width * 10)
        self.current_scene = Scene(name, (ceil(length), ceil(width)))
        # img = ImageTk.PhotoImage(image=Image.fromarray(self.current_scene.layout))
        # self.scene_view.create_image((0, 0), anchor='nw', image=img)
        self.build_right_bar()
        self.build_left_bar()
        self.build_bottom_bar()

    def new_material(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.init_UI()

    def new_object(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.init_UI()

    def build_from_array(self, img):
        for y, row in enumerate(img):
            for x, col in enumerate(row):
                pass


def main():
    root = tk.Tk()
    root.geometry("640x480+300+300")
    app = Example(root)
    root.mainloop()


if __name__ == '__main__':
    main()
