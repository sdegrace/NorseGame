from tools.image_processing_tools import *
import tkinter as tk
from functools import partial
from tkinter import ttk
from PIL import ImageTk, Image, ImageColor
import glob
from tkinter import colorchooser

from game.lib.lib import Material



class MaterialMixin:

    def build_material_editor(self):
        self.main_editor_entry_frame.grid_columnconfigure(1, weight=1)
        tk.Label(self.main_editor_entry_frame, text='Name').grid(row=0, column=0)
        tk.Label(self.main_editor_entry_frame, text='Density').grid(row=1, column=0)
        tk.Label(self.main_editor_entry_frame, text='Ultimate Tensile Strength').grid(row=2, column=0)
        tk.Label(self.main_editor_entry_frame, text='Tensile Yield').grid(row=3, column=0)
        tk.Label(self.main_editor_entry_frame, text='Ultimate Compressive Strength').grid(row=4, column=0)
        tk.Label(self.main_editor_entry_frame, text='Compressive Yield').grid(row=5, column=0)
        tk.Label(self.main_editor_entry_frame, text='Ultimate Shear Strength').grid(row=6, column=0)
        tk.Label(self.main_editor_entry_frame, text='Shear Yield').grid(row=7, column=0)
        tk.Label(self.main_editor_entry_frame, text='Modulus of Elasticity').grid(row=8, column=0)
        tk.Label(self.main_editor_entry_frame, text='Shear Modulus').grid(row=9, column=0)
        tk.Label(self.main_editor_entry_frame, text='Strain at Fracture').grid(row=10, column=0)
        tk.Label(self.main_editor_entry_frame, text='Color').grid(row=11, column=0)

        self.name = tk.Entry(self.main_editor_entry_frame)
        self.name.grid(row=0, column=1, sticky=tk.E+tk.W)
        self.density = tk.Entry(self.main_editor_entry_frame)
        self.density.grid(row=1, column=1, sticky=tk.E+tk.W)
        self.tensile_ult = tk.Entry(self.main_editor_entry_frame)
        self.tensile_ult.grid(row=2, column=1, sticky=tk.E+tk.W)
        self.tensile_yield = tk.Entry(self.main_editor_entry_frame)
        self.tensile_yield.grid(row=3, column=1, sticky=tk.E+tk.W)
        self.compressive_ult = tk.Entry(self.main_editor_entry_frame)
        self.compressive_ult.grid(row=4, column=1, sticky=tk.E+tk.W)
        self.compressive_yield = tk.Entry(self.main_editor_entry_frame)
        self.compressive_yield.grid(row=5, column=1, sticky=tk.E+tk.W)
        self.shear_ult = tk.Entry(self.main_editor_entry_frame)
        self.shear_ult.grid(row=6, column=1, sticky=tk.E+tk.W)
        self.shear_yield = tk.Entry(self.main_editor_entry_frame)
        self.shear_yield.grid(row=7, column=1, sticky=tk.E+tk.W)
        self.mod_of_elasticity = tk.Entry(self.main_editor_entry_frame)
        self.mod_of_elasticity.grid(row=8, column=1, sticky=tk.E+tk.W)
        self.shear_modulus = tk.Entry(self.main_editor_entry_frame)
        self.shear_modulus.grid(row=9, column=1, sticky=tk.E+tk.W)
        self.strain_at_fracture = tk.Entry(self.main_editor_entry_frame)
        self.strain_at_fracture.grid(row=10, column=1, sticky=tk.E+tk.W)
        self.color_var = tk.StringVar()
        self.color = tk.Entry(self.main_editor_entry_frame, textvariable=self.color_var)
        self.color.grid(row=11, column=1, sticky=tk.E+tk.W)

        # self.incl_tensile_ult = tk.IntVar()
        # check = tk.Checkbutton(self.main_editor_canvas_frame, text='Include?', variable=self.incl_tensile_ult).grid(row=2, column=2)
        # check.select()
        self.color_button = tk.Button(self.main_editor_entry_frame, text='Select Color', command=self.select_color).grid(row=11, column=2)

    def select_color(self):
        color = colorchooser.askcolor(initialcolor=self.color_var.get() if self.color_var.get() else None)
        self.color_var.set(color[1])

    def save_material(self, file):
        mat_dict = {'name': self.name.get(),
                    'density': self.density.get(),
                    'tensile_ult': self.tensile_ult.get(),
                    'tensile_yield': self.tensile_yield.get(),
                    'compressive_yield': self.compressive_yield.get(),
                    'compressive_ult': self.compressive_ult.get(),
                    'shear_yield': self.shear_yield.get(),
                    'shear_ult': self.shear_ult.get(),
                    'mod_of_elasticity': self.mod_of_elasticity.get(),
                    'shear_modulus': self.shear_modulus.get(),
                    'strain_at_fracture': self.strain_at_fracture.get(),
                    'color': self.color_var.get()}


        file.write(Material(**{key:var for key, var in mat_dict.items() if var}).to_yaml() + '---\n')


class CanvasMixin:

    def build_canvas(self, max_x=100, max_y=100):
        if self.scene_view is not None:
            self.scene_view.destroy()
        # self.scene_view_frame.config(width=max_x, height=max_y)
        self.scene_view = tk.Canvas(self.main_editor_canvas_frame, bg="white", width=max_x, height=max_y)
        self.scene_size = [max_x, max_y]
        self.xsb = tk.Scrollbar(self.main_editor_canvas_frame, orient="horizontal", command=self.scene_view.xview)
        self.ysb = tk.Scrollbar(self.main_editor_canvas_frame, orient="vertical", command=self.scene_view.yview)
        self.scene_view.configure(yscrollcommand=self.ysb.set, xscrollcommand=self.xsb.set)
        self.scene_view.configure(scrollregion=(0, 0, max_x, max_y))
        self.scene_view.grid(row=0, column=0)

        self.scene_view.bind("<ButtonPress-2>", self.scroll_start)
        self.scene_view.bind("<B2-Motion>", self.scroll_move)
        self.root.bind("<Control-z>", self.undo)
        self.eraser_bind()

        self.xsb.grid(row=1, column=0, sticky="ew")
        self.ysb.grid(row=0, column=1, sticky="ns")
        self.main_editor_canvas_frame.grid_rowconfigure(0, weight=1)
        self.main_editor_canvas_frame.grid_columnconfigure(0, weight=1)

    def scroll_start(self, event):
        self.scene_view.scan_mark(event.x, event.y)

    def scroll_move(self, event):
        self.scene_view.scan_dragto(event.x, event.y, gain=1)

    def eraser(self, event):
        print('pressed!')
        self.scene_view.delete(tk.CURRENT)

    def eraser_bind(self):
        self.scene_view.bind('<Button-3>', self.eraser)
        self.scene_view.bind('<B3-Motion>', self.eraser)


class PanelMixin:

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
        line_button.config(command=self.shape_func_generator([partial(self.paint_2pt_shape_start, shape='line'),
                                                              partial(self.paint_2pt_shape_move, shape='line'),
                                                              partial(self.paint_2pt_shape_end, shape='line')],
                                                             line_button))
        line_button.grid(row=0, column=0)

        rectangle_button = tk.Button(self.shape_frame, text='Rectangle')
        rectangle_button.config(
            command=self.shape_func_generator([partial(self.paint_2pt_shape_start, shape='rectangle'),
                                               partial(self.paint_2pt_shape_move, shape='rectangle'),
                                               partial(self.paint_2pt_shape_end, shape='rectangle')], rectangle_button))
        rectangle_button.grid(row=1, column=0)

        circle_button = tk.Button(self.shape_frame, text='Circle')
        circle_button.config(command=self.shape_func_generator([partial(self.paint_2pt_shape_start, shape='circle'),
                                                                partial(self.paint_2pt_shape_move, shape='circle'),
                                                                partial(self.paint_2pt_shape_end, shape='circle')],
                                                               circle_button))
        circle_button.grid(row=0, column=1)

        ellipse_button = tk.Button(self.shape_frame, text='Ellipse')
        ellipse_button.config(command=self.shape_func_generator('ellipse', ellipse_button))
        ellipse_button.grid(row=1, column=1)

        arc_button = tk.Button(self.shape_frame, text='Arc')
        arc_button.config(command=self.shape_func_generator([partial(self.paint_3pt_shape_start, shape='arc'),
                                                             partial(self.paint_3pt_shape_move_1st, shape='arc'),
                                                             partial(self.paint_3pt_shape_2nd_pt, shape='arc')],
                                                            arc_button))
        arc_button.grid(row=0, column=2)

        ellipse_button.config(state=tk.DISABLED)
        arc_button.config(state=tk.DISABLED)

        freehand_button = tk.Button(self.shape_frame, text='Freehand')
        freehand_button.config(command=self.shape_func_generator([self.paint_freehand_start,
                                                                  self.paint_freehand_move,
                                                                  self.paint_freehand_end], freehand_button))
        freehand_button.grid(row=1, column=2)

        self.shape_buttons = [line_button, rectangle_button, circle_button, ellipse_button, arc_button, freehand_button]

        ttk.Separator(self.shape_frame, orient=tk.VERTICAL).grid(row=0, column=3, rowspan=2, sticky=tk.N + tk.S)
        self.increase_scaling_factor = tk.Button(self.coord_frame, text='Zoom In', command=self.zoom_in)
        self.decrease_scaling_factor = tk.Button(self.coord_frame, text='Zoom Out', command=self.zoom_out)
        self.increase_scaling_factor.grid(row=1, column=0)
        self.decrease_scaling_factor.grid(row=1, column=1)

        # self.scaling_factor_scale = tk.Scale(self.coord_frame, from_=1, to=20, orient=tk.HORIZONTAL, command=self.rebuild_img, repeatinterval=300)
        # self.scaling_factor_scale.set(self.scaling_factor)
        # self.scaling_factor_scale.grid(row=1, column=0, columnspan=2, sticky=tk.E+tk.W)
        ttk.Separator(self.coord_frame, orient=tk.VERTICAL).grid(row=0, column=2, rowspan=2, sticky=tk.N + tk.S)
        show_button = tk.Button(self.snap_frame, text='show', command=self.show_bitmap)
        show_button.pack()
        # delete_button = tk.Button(self.shape_frame, text='Delete')
        # freehand_button.config(command=selection_fro.erasor_bind)
    def show_bitmap(self):
        print(self.bitmap)
        top = tk.Toplevel()
        img = Image.fromarray(self.bitmap)
        img= img.convert('RGB')
        img.show()
        img = ImageTk.PhotoImage(image=img)
        logolbl = tk.Label(top, image=img)
        logolbl.grid()

    def build_left_objects_notebook(self):
        self.left_obj_tab = tk.Frame(self.left_notebook)
        self.left_notebook.add(self.left_obj_tab, text='Objects')

    def build_left_materials_notebook(self):
        self.left_mat_tab = tk.Frame(self.left_notebook)
        self.left_notebook.add(self.left_mat_tab, text='Materials')

    def build_left_materials(self):
        for name, (var, mat, button) in self.materials.items():
            if var.get():
                check = tk.Checkbutton(master=self.left_mat_tab, text=name, variable=var)
                check.pack(side=tk.TOP)

    def build_right_materials_notebook(self):
        self.right_mat_tab = tk.Frame(self.right_notebook)
        self.right_notebook.add(self.right_mat_tab, text='Materials')

        self.build_right_materials()

    def build_right_objects_notebook(self):
        self.right_obj_tab = tk.Frame(self.right_notebook)
        self.right_notebook.add(self.right_obj_tab, text='Objects')
        self.build_right_objects()

    def build_right_objects(self):
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

    def undo(self, event):
        print('undo!')
        if self.current_paint_stroke == 0:
            return
        self.current_paint_stroke -= 1
        self.scene_view.delete('stroke_'+str(self.current_paint_stroke))

    def shape_func_generator(self, paint_functions, button):
        def func():
            for b in self.shape_buttons:
                b.config(fg=self.fg_default, bg=self.bg_default)
            button.config(fg=self.active_shape_fg, bg=self.active_shape_bg)
            self.scene_view.bind("<Button-1>", paint_functions[0])
            self.scene_view.bind("<B1-Motion>", paint_functions[1])
            self.scene_view.bind("<ButtonRelease-1>", paint_functions[2])
            self.active_shape_button = button

        return func

    def material_button_generator(self, material):
        def func():
            self.current_material = material
            bg = material.color
            fg = contrasting_text_color(material.color[1:])
            self.active_shape_fg = fg
            self.active_shape_bg = bg
            if self.active_shape_button is not None:
                self.active_shape_button.config(fg=fg, bg=bg)

        return func


class PaintingMixin:

    def draw_point(self, x, y, tags, save=False):
        self.scene_view.create_rectangle(x * self.scaling_factor, y * self.scaling_factor,
                                         (x + 1) * self.scaling_factor, (y + 1) * self.scaling_factor,
                                         fill=self.current_material.color,
                                         tags=list(tags)+['sf_'+str(self.scaling_factor)])
        if save:
            self.bitmap[y, x, :] = ImageColor.getcolor(self.current_material.color, 'RGBA')
            print(ImageColor.getcolor(self.current_material.color, 'RGBA'))
        # self.bitmap[y, x, 3] = 255

    def paint_freehand_move(self, event):
        print(self.current_paint_stroke)
        x, y = event.x // self.scaling_factor, event.y // self.scaling_factor
        self.draw_point(x, y, ('stroke_' + str(self.current_paint_stroke), 'freehand'), True)

    def paint_freehand_start(self, event):
        x, y = event.x // self.scaling_factor, event.y // self.scaling_factor
        self.draw_point(x, y, ('stroke_' + str(self.current_paint_stroke), 'freehand'), True)

    def paint_freehand_end(self, event):
        x, y = event.x // self.scaling_factor, event.y // self.scaling_factor
        self.draw_point(x, y, ('stroke_' + str(self.current_paint_stroke), 'freehand'), True)
        self.current_paint_stroke += 1

    def paint_2pt_shape_start(self, event, shape):
        print(event, shape)
        print(self.current_paint_stroke)
        self.current_2pt_1st_pt = (event.x // self.scaling_factor, event.y // self.scaling_factor)

    def paint_2pt_shape_move(self, event, shape):
        print(event, shape)
        self.scene_view.delete('active')
        x, y = event.x // self.scaling_factor, event.y // self.scaling_factor
        points = self.shape_mapping[shape](*self.current_2pt_1st_pt, x, y)
        for point in points:
            self.draw_point(*point, ('active',))

    def paint_2pt_shape_end(self, event, shape):
        print(event, shape)
        self.scene_view.delete('active')
        x, y = event.x // self.scaling_factor, event.y // self.scaling_factor
        points = self.shape_mapping[shape](*self.current_2pt_1st_pt, x, y)
        for point in points:
            self.draw_point(*point, (shape, 'stroke_' + str(self.current_paint_stroke)), True)
        self.current_paint_stroke += 1

    def paint_3pt_shape_start(self, event, shape):
        print(event, shape)
        print(self.current_paint_stroke)
        self.current_3pt_1st_pt = (event.x // self.scaling_factor, event.y // self.scaling_factor)

    def paint_3pt_shape_move_1st(self, event, shape):
        print(event, shape)
        self.scene_view.delete('active')
        x, y = event.x // self.scaling_factor, event.y // self.scaling_factor
        points = line(*self.current_3pt_1st_pt, x, y)
        for point in points:
            self.draw_point(*point, ('active',))

    def paint_3pt_shape_2nd_pt(self, event, shape):
        print(event, shape)
        self.scene_view.delete('active')
        x, y = event.x // self.scaling_factor, event.y // self.scaling_factor
        self.current_3pt_2nd_pt = (x, y)
        points = line(*self.current_3pt_1st_pt, x, y)
        for point in points:
            self.draw_point(*point, ('active',))
        self.scene_view.bind("<Motion>", partial(self.paint_3pt_shape_move_2nd, shape=shape))
        self.scene_view.bind("<Button-1>", partial(self.paint_3pt_shape_end, shape=shape))

    def paint_3pt_shape_move_2nd(self, event, shape):
        x, y = event.x // self.scaling_factor, event.y // self.scaling_factor
        self.scene_view.delete('active')
        points = arc(*self.current_3pt_1st_pt, *self.current_3pt_2nd_pt, x, y)
        for point in points:
            self.draw_point(*point, ('active',))

    def paint_3pt_shape_end(self, event, shape):
        x, y = event.x // self.scaling_factor, event.y // self.scaling_factor
        self.scene_view.delete('active')
        points = arc(*self.current_3pt_1st_pt, *self.current_3pt_2nd_pt, x, y)
        for point in points:
            self.draw_point(*point, (shape, 'stroke_' + str(self.current_paint_stroke)))
        self.current_paint_stroke += 1
