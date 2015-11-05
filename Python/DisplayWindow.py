__author__ = 'Colin'
import tkinter as tk
from ColourFul import BlockContainer
from PIL import ImageGrab
import time


class Display(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.rectangle_size = 20  # size in pixels
        self.pack()
        self.canvas = tk.Canvas(self, width=300, height=200)
        self.canvas.pack()
        image = ImageGrab.grab()
        self.BC = BlockContainer(image.height, image.width, 25)
        columns, rows = self.BC.position_blocks()
        self.rectangles = [[None for y in range(rows)] for x in range(columns)]
        self.max_delay = 0.1
        self.run_screencap = True

    def update_pixel(self, xy, colour):
        if type(colour) == tuple:
            colour = self.tuple_to_hex(colour)
        x, y = xy
        if self.rectangles[x][y] is None:
            self.rectangles[x][y] = \
                self.canvas.create_rectangle(x * self.rectangle_size,
                                             y * self.rectangle_size,
                                             x * self.rectangle_size + self.rectangle_size,
                                             y * self.rectangle_size + self.rectangle_size,
                                             fill=colour)
        else:
            self.canvas.itemconfig(self.rectangles[x][y], fill=colour)
        self.canvas.update_idletasks()

    def run(self, gui=True):
        start = time.time()
        image = ImageGrab.grab().load()
        self.BC.calculate_colours(image)
        if gui:
            for block in self.BC.blocks:
                self.update_pixel((block.x, block.y), block.colour)
        end = time.time()
        diff = end - start
        diff = max(0, self.max_delay - diff)
        if self.run_screencap:
            self.after(int(diff * 1000), self.run, gui)

    @staticmethod
    def tuple_to_hex(tuple):
        string = "#"
        for x in tuple:
            if len(hex(x)[2:]) == 1:
                string += '0'
            string += hex(x)[2:]
        return string


if __name__ == "__main__":
    root = tk.Tk()
    display = Display(root)
    display.run(True)
    display.mainloop()
