import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from tkinter import ttk
import glob
from math import ceil
from PIL import ImageTk, Image

from game.lib.lib import Material, Scene


def do_nothing():
    pass


def contrasting_text_color(hex_str):
    (r, g, b) = (hex_str[:2], hex_str[2:4], hex_str[4:])
    print(hex_str)
    return '#000000' if 1 - (int(r, 16) * 0.299 + int(g, 16) * 0.587 + int(b, 16) * 0.114) / 255 < 0.5 else '#ffffff'


class Example(tk.Frame):
    ICON_PADDING = 4

    def __init__(self, root):
        super().__init__()
        default_button = tk.Button()
        self.fg_default = default_button.cget('foreground')
        self.bg_default = default_button.cget('background')
        self.active_shape_fg = None
        self.active_shape_bg = None
        self.active_shape_fg = self.fg_default
        self.active_shape_bg = self.bg_default
        self.active_shape_button = None
        self.root = root
        self.scene_view = None
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
        self.initUI()

    def initUI(self):
        self.master.title("Scene Builder")
        self.pack(fill=tk.BOTH, expand=True)
        self.build_menu()
        # self.build_left_bar()
        # self.build_right_bar()

        self.bottom_frame = tk.Frame(master=self)
        self.bottom_frame.grid(row=1, column=0, columnspan=3, sticky=tk.E + tk.W + tk.S + tk.N)
        # tk.Label(master=self.bottom_frame, text='TEST', bg='red').pack(fill=tk.BOTH, expand=True)

        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        # self.columnconfigure(3, pad=7)
        # self.columnconfigure(4, pad=7)
        # self.rowconfigure(3, weight=1)
        # self.rowconfigure(5, pad=7)

        self.left_notebook = ttk.Notebook(self)
        self.left_notebook.grid(row=0, column=0, sticky=tk.E + tk.W + tk.S + tk.N)

        self.right_notebook = ttk.Notebook(self)
        self.right_notebook.grid(row=0, column=2, sticky=tk.E + tk.W + tk.S + tk.N)

        self.scene_view_frame = tk.Frame(master=self)
        self.scene_view_frame.grid(row=0, column=1, padx=5, sticky=tk.E + tk.W + tk.S + tk.N)

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

        self.scene_view.bind("<ButtonPress-2>", self.scroll_start)
        self.scene_view.bind("<B2-Motion>", self.scroll_move)

        self.xsb.grid(row=1, column=0, sticky="ew")
        self.ysb.grid(row=0, column=1, sticky="ns")
        self.scene_view_frame.grid_rowconfigure(0, weight=1)
        self.scene_view_frame.grid_columnconfigure(0, weight=1)

    def scroll_start(self, event):
        self.scene_view.scan_mark(event.x, event.y)

    def scroll_move(self, event):
        self.scene_view.scan_dragto(event.x, event.y, gain=1)

    def new(self):
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
        self.build_canvas(length * 10 + 5, width * 10 + 5)
        self.current_scene = Scene(name, (ceil(length), ceil(width)))
        img = ImageTk.PhotoImage(image=Image.fromarray(self.current_scene.layout))
        self.scene_view.create_image((0, 0), anchor='nw', image=img)
        self.scene_view.create_rectangle(0, 0, length * 10, width * 10)
        self.build_right_bar()
        self.build_left_bar()
        self.build_bottom_bar()

    def build_right_materials(self):
        for i, (name, (activated, material, button)), in enumerate(self.materials.items()):
            if button is None:
                button = tk.Button(master=self.right_mat_tab, text=name, bg=material.color,
                                   fg=contrasting_text_color(material.color[1:]),
                                   command=self.material_button_generator(material))
            if activated:
                button.grid(column=i % 3, row=i // 3, pady=self.ICON_PADDING, padx=self.ICON_PADDING)
            else:
                button.grid_forget()

    def shape_func_generator(self, shape, button):
        def func():
            for b in self.shape_buttons:
                b.config(fg=self.fg_default, bg=self.bg_default)
            button.config(fg=self.active_shape_fg, bg=self.active_shape_bg)
            self.current_draw_shape = shape
            self.active_shape_button = button

        return func

    def material_button_generator(self, material):
        def func():
            self.current_material = material
            fg = material.color
            bg = contrasting_text_color(material.color[1:])
            self.active_shape_fg = fg
            self.active_shape_bg = bg
            if self.active_shape_button is not None:
                self.active_shape_button.config(fg=fg, bg=bg)

        return func

    def build_bottom_bar(self):
        self.shape_frame = tk.Frame(self.bottom_frame)
        self.shape_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.coord_frame = tk.Frame(self.bottom_frame)
        self.coord_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.fill_frame = tk.Frame(self.bottom_frame)
        self.fill_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.snap_frame = tk.Frame(self.bottom_frame)
        self.snap_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        line_button = tk.Button(self.shape_frame, text='Line')
        line_button.config(command=self.shape_func_generator('line', line_button))
        line_button.grid(row=0, column=0)

        rectangle_button = tk.Button(self.shape_frame, text='Rectangle')
        rectangle_button.config(command=self.shape_func_generator('rectangle', rectangle_button))
        rectangle_button.grid(row=1, column=0)

        circle_button = tk.Button(self.shape_frame, text='Circle')
        circle_button.config(command=self.shape_func_generator('circle', circle_button))
        circle_button.grid(row=0, column=1)

        ellipse_button = tk.Button(self.shape_frame, text='Ellipse')
        ellipse_button.config(command=self.shape_func_generator('ellipse', ellipse_button))
        ellipse_button.grid(row=1, column=1)

        arc_button = tk.Button(self.shape_frame, text='Arc')
        arc_button.config(command=self.shape_func_generator('arc', arc_button))
        arc_button.grid(row=0, column=2)

        freehand_button = tk.Button(self.shape_frame, text='Freehand')
        freehand_button.config(command=self.shape_func_generator('freehand', freehand_button))
        freehand_button.grid(row=1, column=2)

        self.shape_buttons = [line_button, rectangle_button, circle_button, ellipse_button, arc_button, freehand_button]

    def build_left_bar(self):
        self.left_mat_tab = tk.Frame(self.left_notebook)
        self.left_obj_tab = tk.Frame(self.left_notebook)
        self.left_notebook.add(self.left_mat_tab, text='Materials')
        self.left_notebook.add(self.left_obj_tab, text='Objects')

        # self.label1 = ttk.Label(self.mat_tab, text='Materials').grid(row=1, column=1)
        # self.label2 = ttk.Label(self.obj_tab, text='Objects').grid(row=1, column=1)

        for name, (var, mat, button) in self.materials.items():
            if var.get():
                check = tk.Checkbutton(master=self.left_mat_tab, text=name, variable=var)
                check.pack(side=tk.TOP)

    def build_right_bar(self):
        self.right_mat_tab = tk.Frame(self.right_notebook)
        self.right_obj_tab = tk.Frame(self.right_notebook)
        self.right_notebook.add(self.right_mat_tab, text='Materials')
        self.right_notebook.add(self.right_obj_tab, text='Objects')

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
            button = tk.Button(self.right_obj_tab, image=self.object_icons[-1], text=icon.split('/')[-1],
                               compound='top')
            # self.buttons.append(button)
            button.grid(row=row, column=col, pady=self.ICON_PADDING, padx=self.ICON_PADDING)

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
