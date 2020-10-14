import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox, colorchooser
from tkinter import ttk
from math import ceil, floor, sqrt
import numpy as np
from tools.image_processing_tools import *

from tools.mixins import PaintingMixin, PanelMixin, CanvasMixin, MaterialMixin
from game.lib.lib import Material, Scene


def rounddown(x):
    return int(floor(x / 10.0)) * 10


def do_nothing():
    pass


def _from_rgb(rgb):
    """translates an rgb tuple of int to a tkinter friendly color code
    """
    return "#%02x%02x%02x" % rgb


class Example(tk.Frame, PaintingMixin, PanelMixin, CanvasMixin, MaterialMixin):
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
        self.scene_size = None
        self.current_paint_stroke = 0
        self.current_scene = None
        self.has_changes = False
        self.current_draw_shape = None
        self.materials = {mat.name: (tk.IntVar(), mat, None) for mat in
                          Material.from_yaml('../game/data/materials.yaml')}
        self.current_material = None
        self.current_object = None
        self.bitmap = None
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
        self.editor_type = None

    def init_UI(self):
        self.build_menu()

        self.bottom_frame = tk.Frame(master=self)
        self.bottom_frame.grid(row=1, column=0, columnspan=3, sticky=tk.E + tk.W + tk.S + tk.N)

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

        self.filemenu.add_command(label="Save", command=self.save)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=self.quit)
        self.menubar.add_cascade(label="File", menu=self.filemenu)

        self.helpmenu = tk.Menu(self.menubar, tearoff=0)
        self.helpmenu.add_command(label="Help Index", command=do_nothing)
        self.helpmenu.add_command(label="About...", command=do_nothing)
        self.menubar.add_cascade(label="Help", menu=self.helpmenu)

        self.root.config(menu=self.menubar)

    def save(self):
        filename = filedialog.asksaveasfilename(defaultextension='yaml', filetypes=[('yaml', '.yaml')], initialdir='../game/data/')
        with open(filename, mode='a') as file:
            if self.editor_type == 'material':
                self.save_material(file)
            elif self.editor_type == 'scene':
                self.save_scene(file)
            elif self.editor_type == 'object':
                self.save_object(file)

    def new_scene(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.init_UI()
        self.editor_type = 'scene'
        # filetypes = [('all files', '.*'), ('yamls', '.yaml')]
        # savepath = filedialog.asksaveasfilename(parent=self,
        #                                         initialdir='../game/data/',
        #                                         title="Please select a file to save the scene:")
        if self.current_scene is not None and self.current_paint_stroke > 0:
            response = messagebox.askyesno('Discard Changes?',
                                           '''If you create a new scene now, your existing changes will be discarded. 
                                           Do you really want to discard these changes?''')
            if not response:
                return

        name = simpledialog.askstring('Name', 'What is the name of the new scene?', parent=self)
        length = simpledialog.askfloat('Length', 'How long will the scene be, in meters?', parent=self)
        width = simpledialog.askfloat('Width', 'How wide will the scene be, in meters?', parent=self)
        self.grid_size = simpledialog.askinteger('Grid Size', 'How many centimeters per grid?', parent=self, initialvalue=100, minvalue=1)
        length *= self.grid_size
        width *= self.grid_size
        length = round(length)
        width = round(width)
        self.bitmap = np.zeros((length, width, 4))
        self.build_canvas(length*self.scaling_factor, width*self.scaling_factor)
        # img = ImageTk.PhotoImage(image=Image.fromarray(self.current_scene.layout))
        # self.scene_view.create_image((0, 0), anchor='nw', image=img)
        self.build_left_materials_notebook()
        self.build_left_objects_notebook()
        self.build_left_materials()
        self.build_right_materials_notebook()
        self.build_right_objects_notebook()
        self.build_right_materials()
        self.build_right_objects()
        self.build_bottom_bar()

    def new_material(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.editor_type = 'material'
        self.init_UI()
        self.build_material_editor()

    def new_object(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.init_UI()

    def rebuild_img(self, event):
        new_sf = int(event)
        mult = new_sf / self.scaling_factor
        self.scene_view.scale("all", mult, mult, 1*mult, 1*mult)
        self.scene_size = [self.scene_size[0]*mult, self.scene_size[1]*mult]
        self.scene_view.config(width=self.scene_size[0], height=self.scene_size[1])
        self.scaling_factor = new_sf

    def build_from_array(self, img):
        for y, row in enumerate(img):
            for x, col in enumerate(row):
                if col[3] != 0:
                    self.scene_view.create_rectangle(x * self.scaling_factor, y * self.scaling_factor,
                                                     (x + 1) * self.scaling_factor, (y + 1) * self.scaling_factor,
                                                     fill=_from_rgb(col[:3]),
                                                     tags=('bitmap', 'sf_'+str(self.scaling_factor)))


def main():
    root = tk.Tk()
    root.geometry("640x480+300+300")
    app = Example(root)
    root.mainloop()


if __name__ == '__main__':
    main()
