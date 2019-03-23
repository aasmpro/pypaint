from tkinter import *
from tkinter.colorchooser import askcolor
from PIL import Image, ImageDraw
import datetime


class Paint(Frame):
    def __init__(self):
        self.root = Tk()
        super().__init__()
        self.master.title("Paint")

        self.old_x = None
        self.old_y = None
        self.shape_x = None
        self.shape_y = None
        self.line_width = 1
        self.color1 = 'black'
        self.color2 = 'white'

        tools_frame = Frame(self)
        tools_frame.pack(fill='both')

        # color buttons
        self.color1_button = Button(tools_frame, command=self.choose_color1, highlightbackground=self.color1,
                                    background=self.color1, activebackground=self.color1)
        self.color1_button.pack(side="left", padx=0, pady=5)

        self.color2_button = Button(tools_frame, command=self.choose_color2, highlightbackground=self.color2,
                                    background=self.color2, activebackground=self.color2)
        self.color2_button.pack(side="left", padx=0, pady=5)

        self.color1_button.bind("<Enter>", self.set_color1_button)
        self.color2_button.bind("<Enter>", self.set_color2_button)

        # tool buttons
        self.brush_button = Button(tools_frame, text='\u23FA', command=self.use_brush, height=1, width=1)
        self.brush_button.pack(side="left", padx=(60, 0), pady=5)

        self.line_button = Button(tools_frame, text='\\', command=self.use_line, height=1, width=1)
        self.line_button.pack(side="left", padx=0, pady=5)

        self.circle_button = Button(tools_frame, text='\u20DD', command=self.use_circle, height=1, width=1)
        self.circle_button.pack(side="left", padx=0, pady=5)

        self.rectangle_button = Button(tools_frame, text='\u20DE', command=self.use_rectangle, height=1, width=1)
        self.rectangle_button.pack(side="left", padx=0, pady=5)

        self.f_circle_button = Button(tools_frame, text='\u25CF', command=self.use_f_circle, height=1, width=1)
        self.f_circle_button.pack(side="left", padx=0, pady=5)

        self.f_rectangle_button = Button(tools_frame, text='\u25A0', command=self.use_f_rectangle, height=1, width=1)
        self.f_rectangle_button.pack(side="left", padx=0, pady=5)

        self.eraser_button = Button(tools_frame, text='\u232B', command=self.use_eraser, height=1, width=1)
        self.eraser_button.pack(side="left", padx=0, pady=5)

        self.choose_size_button = Scale(tools_frame, from_=1, to=50, orient=HORIZONTAL, command=self.size)
        self.choose_size_button.pack(side="left", padx=5, pady=5)

        # save button
        self.save_button = Button(tools_frame, text='save', command=self.save)
        self.save_button.pack(side="right", padx=0, pady=5)

        # canvas
        canvas_frame = Frame(self)
        canvas_frame.pack(fill='both')

        self.canvas = Canvas(canvas_frame, bg='white', width=600, height=600)
        self.canvas.pack(side="left", padx=0, pady=0)

        self.canvas.bind("<Button-1>", self.draw_shape)
        self.canvas.bind('<B1-Motion>', self.paint)
        self.canvas.bind('<ButtonRelease-1>', self.reset)
        self.canvas.bind('<Motion>', self.set_position)

        # cursor position
        footer_frame = Frame(self)
        footer_frame.pack(fill='both')

        self.shape_label = Label(footer_frame, text='')
        self.shape_label.pack(side='left')

        self.position_label = Label(footer_frame, text='x = 0  y = 0')
        self.position_label.pack(side='right')

        # PIL image variable
        self.image = Image.new('RGB', (600, 600), 'white')
        self.draw = ImageDraw.Draw(self.image)

        self.active_button = self.brush_button
        self.brush_button.config(relief=SUNKEN)

        self.pack()
        self.root.mainloop()

    def set_color1_button(self, event):
        self.color1_button['background'] = self.color1
        self.color1_button['highlightbackground'] = self.color1
        self.color1_button['activebackground'] = self.color1

    def set_color2_button(self, event):
        self.color2_button['background'] = self.color2
        self.color2_button['highlightbackground'] = self.color2
        self.color2_button['activebackground'] = self.color2

    def choose_color1(self):
        self.color1 = askcolor(color=self.color1)[1]
        self.set_color1_button(None)  # changing button color too

    def choose_color2(self):
        self.color2 = askcolor(color=self.color2)[1]
        self.set_color2_button(None)  # changing button color too

    # changing tool
    def use_brush(self):
        self.activate_button(self.brush_button)

    def use_line(self):
        self.activate_button(self.line_button)

    def use_circle(self):
        self.activate_button(self.circle_button)

    def use_rectangle(self):
        self.activate_button(self.rectangle_button)

    def use_f_circle(self):
        self.activate_button(self.f_circle_button)

    def use_f_rectangle(self):
        self.activate_button(self.f_rectangle_button)

    def use_eraser(self):
        self.activate_button(self.eraser_button)

    # changing active tool style
    def activate_button(self, some_button):
        self.shape_label['text'] = ''
        self.shape_x, self.shape_y = None, None
        self.active_button.config(relief=RAISED)
        some_button.config(relief=SUNKEN)
        self.active_button = some_button

    # for PIL.ImageDraw.rectangle and PIL.ImageDraw.ellipse last mouse x and y positions must be less than next x and y
    # to represent the top left side to bottom right side, so this function fix x and y positions in other situations.
    def fix_positions(self, lx, ly, nx, ny):
        if lx >= nx and ly >= ny:
            nx, lx = lx, nx
            ny, ly = ly, ny
        elif lx >= nx and ly <= ny:
            nx, lx = lx, nx
        elif lx <= nx and ly >= ny:
            ny, ly = ly, ny

        return [lx, ly, nx, ny]

    # drawing line, circle or rectangle
    def draw_shape(self, event):
        if self.shape_x and self.shape_y:
            if self.active_button == self.line_button:
                self.canvas.create_line(self.shape_x, self.shape_y, event.x, event.y,
                                        width=self.line_width, fill=self.color1)
                self.draw.line([self.shape_x, self.shape_y, event.x, event.y], width=self.line_width, fill=self.color1)

            elif self.active_button == self.circle_button or self.active_button == self.f_circle_button:
                fill = None if self.active_button == self.circle_button else self.color2
                self.canvas.create_oval(self.shape_x, self.shape_y, event.x, event.y,
                                        width=self.line_width, fill=fill, outline=self.color1)
                self.draw.ellipse(self.fix_positions(self.shape_x, self.shape_y, event.x, event.y),
                                  width=self.line_width, fill=fill, outline=self.color1)

            elif self.active_button == self.rectangle_button or self.active_button == self.f_rectangle_button:
                fill = None if self.active_button == self.rectangle_button else self.color2
                self.canvas.create_rectangle(self.shape_x, self.shape_y, event.x, event.y,
                                             width=self.line_width, fill=fill, outline=self.color1)
                self.draw.rectangle(self.fix_positions(self.shape_x, self.shape_y, event.x, event.y),
                                    width=self.line_width, fill=fill, outline=self.color1)

            self.shape_label['text'] = ''
            self.shape_x, self.shape_y = None, None

        elif not self.active_button == self.brush_button and not self.active_button == self.eraser_button:
            self.shape_x = event.x
            self.shape_y = event.y
            self.shape_label['text'] = 'shape start from x = {}  y = {}'.format(self.shape_x, self.shape_y)

    def paint(self, event):
        # using second color for eraser tool
        paint_color = self.color2 if self.active_button == self.eraser_button else self.color1
        if self.old_x and self.old_y and (
                self.active_button == self.brush_button or self.active_button == self.eraser_button):
            self.canvas.create_line(self.old_x, self.old_y, event.x, event.y,
                                    width=self.line_width, fill=paint_color,
                                    capstyle=ROUND, smooth=TRUE, splinesteps=1)

            self.draw.line([self.old_x, self.old_y, event.x, event.y], width=self.line_width, fill=paint_color)

        self.old_x = event.x
        self.old_y = event.y

    def set_position(self, event):
        self.position_label['text'] = 'x = {}  y = {}'.format(event.x, event.y)

    def size(self, size):
        self.line_width = int(size)

    def reset(self, event):
        self.old_x, self.old_y = None, None

    def save(self):
        self.image.save("image{}.png".format(datetime.datetime.now().strftime("%Y%m%d%H%M%S")))


if __name__ == '__main__':
    Paint()
