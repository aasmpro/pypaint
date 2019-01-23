from tkinter import *
from tkinter.colorchooser import askcolor
from PIL import Image, ImageDraw


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
        self.eraser_on = False

        tools_frame = Frame(self)
        tools_frame.pack(fill='x')

        self.brush_button = Button(tools_frame, text='brush', command=self.use_brush)
        self.brush_button.pack(side="left", padx=5, pady=5)

        self.color1_button = Button(tools_frame, command=self.choose_color1, highlightbackground=self.color1,
                                    background=self.color1, activebackground=self.color1)
        self.color1_button.pack(side="left", padx=0, pady=5)

        self.color2_button = Button(tools_frame, command=self.choose_color2, highlightbackground=self.color2,
                                    background=self.color2, activebackground=self.color2)
        self.color2_button.pack(side="left", padx=0, pady=5)

        self.color1_button.bind("<Enter>", self.set_color1_button)
        self.color2_button.bind("<Enter>", self.set_color2_button)

        self.eraser_button = Button(tools_frame, text='eraser', command=self.use_eraser)
        self.eraser_button.pack(side="left", padx=5, pady=5)

        self.choose_size_button = Scale(tools_frame, from_=1, to=20, orient=HORIZONTAL, command=self.size)
        self.choose_size_button.pack(side="left", padx=5, pady=5)

        self.save_button = Button(tools_frame, text='save', command=self.save)
        self.save_button.pack(side="left", padx=5, pady=5)

        canvas_frame = Frame(self)
        canvas_frame.pack(fill='x')

        self.canvas = Canvas(canvas_frame, bg='white', width=600, height=600)
        self.canvas.pack(side="left", padx=5, pady=5)

        self.image = Image.new('RGB', (600, 600), 'white')
        self.draw = ImageDraw.Draw(self.image)

        self.active_button = self.brush_button
        self.brush_button.config(relief=SUNKEN)

        self.canvas.bind('<B1-Motion>', self.paint)
        self.canvas.bind('<ButtonRelease-1>', self.reset)

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

    def use_brush(self):
        self.activate_button(self.brush_button)

    def choose_color1(self):
        self.eraser_on = False
        self.color1 = askcolor(color=self.color1)[1]
        self.set_color1_button(None)

    def choose_color2(self):
        self.eraser_on = False
        self.color2 = askcolor(color=self.color1)[1]
        self.set_color2_button(None)

    def use_eraser(self):
        self.activate_button(self.eraser_button, eraser_mode=True)

    def activate_button(self, some_button, eraser_mode=False):
        self.active_button.config(relief=RAISED)
        some_button.config(relief=SUNKEN)
        self.active_button = some_button
        self.eraser_on = eraser_mode

    def paint(self, event):
        paint_color = 'white' if self.eraser_on else self.color1
        if self.old_x and self.old_y:
            self.canvas.create_line(self.old_x, self.old_y, event.x, event.y,
                                    width=self.line_width, fill=paint_color,
                                    capstyle=ROUND, smooth=TRUE, splinesteps=1)

            self.draw.line([self.old_x, self.old_y, event.x, event.y], width=self.line_width, fill=paint_color)

        self.old_x = event.x
        self.old_y = event.y

    def create_rectangle(self, event):
        if self.shape_x and self.shape_y:
            pass

    def reset(self, event):
        self.old_x, self.old_y = None, None

    def save(self):
        self.image.save("image.png")

    def size(self, size):
        self.line_width = int(size)


if __name__ == '__main__':
    Paint()
