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
        self.update_pixel((0, 0), (100, 20, 30))
        image = ImageGrab.grab()
        self.BC = BlockContainer(image.height, image.width, 25)
        self.BC.position_blocks()

    def update_pixel(self, xy, colour):
        if type(colour) == tuple:
            colour = self.tuple_to_hex(colour)

        self.canvas.create_rectangle(xy[0] * self.rectangle_size,
                                     xy[1] * self.rectangle_size,
                                     xy[0] * self.rectangle_size + self.rectangle_size,
                                     xy[1] * self.rectangle_size + self.rectangle_size,
                                     fill=colour)
        self.canvas.update_idletasks()

    def run(self):
        start = time.time()
        image = ImageGrab.grab()
        self.BC.calculate_colours(image)
        for block in self.BC.blocks:
            self.update_pixel((block.x, block.y), block.colour)
        end = time.time()
        diff = end - start
        diff = max(0, 0.1 - diff)
        print(diff)
        self.after(int(diff * 1000), self.run)

    @staticmethod
    def tuple_to_hex(tuple):
        string = "#"
        for x in tuple:
            string += hex(x)[2:]
        return string


if __name__ == "__main__":
    root = tk.Tk()
    display = Display(root)
    display.run()
    display.mainloop()