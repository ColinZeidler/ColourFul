__author__ = 'Colin'

from PIL import ImageGrab
import time


class Block(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        #(R, G, B)
        self.colour = (0, 0, 0)

    def calculate_colour(self, screen_shot):
        red = blue = green = count = 0
        start_x = self.x * self.width
        start_y = self.y * self.height
        for x in range(start_x, start_x + self.width, 10):
            for y in range(start_y, start_y + self.height, 10):
                r, g, b = screen_shot[x, y]
                red += r
                green += g
                blue += b
                count += 1
        red = red // count
        green = green // count
        blue = blue // count
        self.colour = red, green, blue
        return self.colour

    def calculate_image_pos(self):
        pos_x = self.x*self.width
        pos_y = self.y*self.height
        end_x = pos_x + self.width
        end_y = pos_y + self.height
        return pos_x, pos_y, end_x, end_y

    def __str__(self):
        return "block: {}, {}; colour: {}".format(self.x, self.y, self.colour)

    def __repr__(self):
        return "block: {}, {}; colour: {}".format(self.x, self.y, self.colour)


class BlockContainer(object):
    def __init__(self, height, width, blocks):
        self.blocks = []
        self.block_count = blocks
        self.height = height
        self.width = width

    def position_blocks(self):
        """
        assumes we have at least 4 blocks
        blocks get x,y based on top left corner
        :return:
        """

        count = 4  # start with 1 in each corner
        sides = 0
        top = 0
        bottom = 0
        while count < self.block_count-6:
            top += 2
            bottom += 2
            sides += 1
            count += 6
        remainder = self.block_count - count
        if remainder >= 4:
            while remainder >= 4:
                top += 1
                bottom += 1
                sides += 1
                remainder -= 4

        if remainder == 3:
            top += 1
            sides += 1
            remainder -= 3
        elif remainder == 2:
            top += 1
            bottom += 1
            remainder -= 2
        elif remainder == 1:
            top += 1
            remainder -= 1
        print("remainder: {}, t: {}, b: {}, s: {}".format(remainder, top, bottom, sides))
        print("plus 4 corners")

        block_width = self.width // (top + 2)
        block_height = self.height // (sides + 2)

        #create blocks and assign positions
        for x in range(top + 2):
            for y in range(sides + 2):
                ok = False
                if x == 0 or x == top + 1:
                    ok = True
                if y == 0 or y == sides + 1:
                    ok = True
                if x == (top + 2) // 2 and y == sides + 1:
                    ok = False
                if ok:
                    self.blocks.append(Block(x, y, block_width, block_height))
        return top+2, sides+2

    def calculate_colours(self, screen_shot):
        for block in self.blocks:
            block.calculate_colour(screen_shot)

if __name__ == "__main__":
    image = ImageGrab.grab()

    blocks = BlockContainer(image.height, image.width, 25)
    blocks.position_blocks()
    while True:
        start = time.time()
        image = ImageGrab.grab().load()
        blocks.calculate_colours(image)
        end = time.time()
        print(end - start)