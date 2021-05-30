import pygame, sys
from random import choice, seed
from pygame.locals import *

seed(2)

def bound(low, high, value):
    return max(low, min(high, value))


class Cell:
    def __init__(self, xy, color):
        self.x = xy[0]
        self.y = xy[1]
        self.color = color
        #self.rect = (self.x, self.y, cell_side, cell_side)

    def update(self):
        self.y += 1
        #self.rect = (self.x, self.y, cell_side, cell_side)
    
    def move(self, movement):
        self.x += movement
        #self.rect = (self.x, self.y, cell_side, cell_side)


    def can_move(self, axis, movement = 0):
        if axis == 'x':

            if (self.x + movement, self.y) in blocked_cells:
                return False
            if movement == -1 and self.x + movement < 0:
                return False
            elif movement == 1 and self.x + movement > cell_count_col - 1:
                return False

        elif axis == 'y':

            if (self.x, self.y + 1) in blocked_cells:
                return False
            if self.y >= cell_count_row - 1:
                return False
        
        return True

    def draw(self):
        r = pygame.Rect(self.x * cell_side, self.y * cell_side, cell_side, cell_side)
        pygame.draw.rect(screen, self.color, r)
    
    def get_position(self):
        return (self.x, self.y)

    def get_color(self):
        return self.color

    def change_color(self, color):
        self.color = color

    def __str__(self):
        return str(self.get_position())


def get_blocks(block_type, shade):
    blocks = []

    color = black_color

    if block_type == 'i':
        blocks =   [[(3, -1), (4, -1), (5, -1), (6, -1)],
                    [(4, -2), (4, -1), (4, 0), (4, 1)],
                    [(5, -1), (4, -1), (3, -1), (2, -1)],
                    [(4, 0), (4, -1), (4, -2), (4, -3)]]

        color = (   bound(0, 255, i_color[0] + shade[0]), 
                    bound(0, 255, i_color[1] + shade[1]), 
                    bound(0, 255, i_color[2] + shade[2]))
        

    elif block_type == 's':
        blocks =   [[(3, -1), (4, -1), (4, -2), (5, -2)],
                    [(4, -2), (4, -1), (5, -1), (5, 0)],
                    [(5, -1), (4, -1), (4, 0), (3, 0)],
                    [(4, 0), (4, -1), (3, -1), (3, -2)]]

        color = (   bound(0, 255, s_color[0] + shade[0]), 
                    bound(0, 255, s_color[1] + shade[1]), 
                    bound(0, 255, s_color[2] + shade[2]))

    elif block_type == 'j':
        blocks =   [[(3, -1), (4, -1), (5, -1), (3, -2)],
                    [(4, 0), (4, -1), (4, -2), (5, -2)],
                    [(3, -1), (4, -1), (5, -1), (5, 0)],
                    [(4, -2), (4, -1), (4, 0), (3, 0)]]

        color = (   bound(0, 255, j_color[0] + shade[0]), 
                    bound(0, 255, j_color[1] + shade[1]), 
                    bound(0, 255, j_color[2] + shade[2])) 

    elif block_type == 't':
        blocks =    [[(3, -1), (4, -1), (5, -1), (4, -2)],
                    [(4, -2), (4, -1), (4, 0), (5, -1)],
                    [(3, -1), (4, -1), (5, -1), (4, 0)],
                    [(3, -1), (4, -1), (4, -2), (4, 0)]]

        color = (   bound(0, 255, t_color[0] + shade[0]), 
                    bound(0, 255, t_color[1] + shade[1]), 
                    bound(0, 255, t_color[2] + shade[2])) 

    elif block_type == 'l':
        blocks =   [[(3, -1), (4, -1), (5, -1), (5, -2)],
                    [(4, -2), (4, -1), (4, 0), (5, 0)],
                    [(3, -1), (4, -1), (5, -1), (3, 0)],
                    [(4, 0), (4, -1), (4, -2), (3, -2)]]

        color = (   bound(0, 255, l_color[0] + shade[0]), 
                    bound(0, 255, l_color[1] + shade[1]), 
                    bound(0, 255, l_color[2] + shade[2])) 

    elif block_type == 'z':
        blocks =   [[(4, -2), (4, -1), (3, -2), (5, -1)],
                    [(4, 0), (4, -1), (5, -1), (5, -2)],
                    [(3, -1), (4, -1), (4, 0), (5, 0)],
                    [(4, -2), (4, -1), (3, -1), (3, 0)]]

        color = (   bound(0, 255, z_color[0] + shade[0]), 
                    bound(0, 255, z_color[1] + shade[1]), 
                    bound(0, 255, z_color[2] + shade[2])) 

    elif block_type == 'o':
        blocks =   [[(4, -1), (4, -2), (5, -1), (5, -2)],
                    [(4, -1), (4, -2), (5, -1), (5, -2)],
                    [(4, -1), (4, -2), (5, -1), (5, -2)],
                    [(4, -1), (4, -2), (5, -1), (5, -2)]]

        color = (   bound(0, 255, o_color[0] + shade[0]), 
                    bound(0, 255, o_color[1] + shade[1]), 
                    bound(0, 255, o_color[2] + shade[2])) 

    all_rotations = []
    rotation = []

    for block in blocks:
        for cell_pos in block:
            cell = Cell(cell_pos, color)
            rotation.append(cell)

        all_rotations.append(rotation)
        rotation = []
        
    return all_rotations


class Shadow:

    def __init__(self, block_type):
        self.type = block_type
        self.shadows = get_blocks(block_type, (-100, -100, -100))
        self.shadow_index = 0 
        self.current_shadow = self.shadows[self.shadow_index]
        self.shadow_x = self.current_shadow[1].x
        self.active = True

    def update(self):
        if self.active:
            for cell in self.current_shadow:
                if not cell.can_move('y'):
                    return False

            for shadow in self.shadows:
                for cell in shadow:
                    cell.update()
            
            return True

    def draw(self):
        if self.active:
            for cell in self.current_shadow:
                cell.draw()

    def move_down(self):
        if self.active:
            moving_down = True
            while moving_down:
                moving_down = self.update()
    
    def hide(self):
        self.active = False
    

class Block:

    def __init__(self, block_type):
        self.type = block_type
        self.blocks = get_blocks(block_type, (0, 0, 0))
        self.index = 0 
        self.current_block = self.blocks[self.index]
        self.can_move = True
        self.x_pos = self.current_block[1].x

        self.shadow = Shadow(block_type)


    def update(self):

        if self.can_move:

            for cell in self.current_block:
                if not cell.can_move('y'):
                    self.can_move = False

                    global active_blocks
                    active_blocks.append(Block(choice(block_types)))
                    
                    global blocked_cells
                    for cell in self.current_block:
                        blocked_cells.append(cell.get_position())

                    self.shadow.hide()
                    
                    check_for_full_lines()

                    return False

            for block in self.blocks:
                for cell in block:
                    cell.update()
            
            
            return True

    def move(self, movement):

        for cell in self.current_block:
            if not cell.can_move('x', movement):
                return

        self.x_pos += movement

        for block in self.blocks:
            for cell in block:
                cell.move(movement)  
        
        self.update_shadow()
        

    def get_movement(self):

        if self.can_move:
            if pygame.mouse.get_focused():
                mouse_pos_x = int(pygame.mouse.get_pos()[0]/cell_side)
                
                if mouse_pos_x > self.x_pos: 
                    self.move(1)
                elif mouse_pos_x < self.x_pos:
                    self.move(-1) 

            else:
                movement = 0
                keys = pygame.key.get_pressed()

                if keys[pygame.K_LEFT]:
                    movement = -1
                if keys[pygame.K_RIGHT]:
                    movement = 1

                if movement != 0:
                    self.move(movement)  
                  

    def draw(self):

        self.shadow.draw()
        for cell in self.current_block:
            cell.draw()

    def inbound(self, block):
        for cell in block:
            if cell.x < 0 or cell.x >= cell_count_col:
                return False
        return True
    
    def block_collision(self, block):

        for cell in block:
            if cell.get_position() in blocked_cells:
                return True

        return False

    def spin(self):

        self.index += 1

        if self.index >= len(self.blocks):
            self.index = 0

        next_block = self.blocks[self.index]
        
        # if its an illegal spin (inside another block)
        # just dont let it happen

        if self.block_collision(next_block):
            return

        # if its an illegal spin (out of bounds) the move if a little 
        # to left of right to adjust
        # the 'i' block needs to be moved by two tiles instead of one

        if not self.inbound(next_block):
            movement = 2 if self.type == 'i' else 1 

            if next_block[1].x < cell_count_col/2:
                self.move(movement)
            else: 
                self.move(-movement)

        self.current_block = next_block
        self.update_shadow()

    def remove(self, cell_pos):
        cell_to_remove = None

        for cell in self.current_block:
            if cell_pos == cell.get_position():
                cell_to_remove = cell
                break

        if cell_to_remove != None:
            self.current_block.remove(cell_to_remove)

    def move_down(self):
        
        # keep updating until it can't anymore (blockage)
        moving_down = True
        while moving_down:
            moving_down = self.update()

    def update_shadow(self):

        # reset position
        for i in range(len(self.blocks)):
            for j in range(len(self.blocks[i])):
                self.shadow.shadows[i][j].x = self.blocks[i][j].x
                self.shadow.shadows[i][j].y = self.blocks[i][j].y

        # update current shadow if spined
        # and move it all the way down
        self.shadow.current_shadow = self.shadow.shadows[self.index]
        self.shadow.move_down()


def lower_line(line_y):

    global blocked_cells

    for i in range(cell_count_col):
        cell_pos = (i, line_y)
        found = False

        for block in active_blocks:
            for cell in block.current_block:
                if cell_pos == cell.get_position():
                    blocked_cells.remove(cell_pos)
                    cell.update()
                    blocked_cells.append(cell.get_position())
                    found = True
            if found: break


def remove_line(line_y):

    pivot_y = line_y

    # remove from blocked cells array
    # then remove from blocks

    for i in range(cell_count_col):
        remove_cell = (i, line_y)
        blocked_cells.remove(remove_cell)

        for block in active_blocks:
            block.remove(remove_cell)

    # lower all lines above the removed one

    for i in range(pivot_y - 1, -1, -1):
        lower_line(i)

    # add to score
    global overall_score
    overall_score += 10
    print('Score: ', overall_score)

    # then check again for new completed lines

    check_for_full_lines()
    
    
# check the whole board for complete lines
# bottom up checking every time a piece is down

def check_for_full_lines():

    for i in range(cell_count_row, -1, -1):
        full_line = True

        for j in range(cell_count_col):
            cell = (j, i)

            if cell not in blocked_cells:
                full_line = False

        if full_line:
            remove_line(i)
        i += 1
    

def draw_game():
    x_offset = 0
    y_offset = 0

    for block in active_blocks:
        block.draw()

    for i in range(cell_count_row):
        for j in range(cell_count_col):
            r = pygame.Rect(x_offset, y_offset, cell_side, cell_side)
            pygame.draw.rect(screen, grey_color, r, 1)
            x_offset += cell_side

        x_offset = 0
        y_offset += cell_side


# MAIN
pygame.init()
pygame.display.set_caption("Tetris")
clock = pygame.time.Clock()

FPS = 60
cell_side = 30
screen_w, screen_h = 300, 600 
cell_count_row, cell_count_col = (int(screen_h/cell_side), int(screen_w/cell_side))

screen = pygame.display.set_mode((screen_w, screen_h))

black_color = (0, 0, 0)
white_color = (255, 255, 255)
grey_color = (25, 25, 25)
red_color = (255, 100, 100)
teal_color = (100, 255, 255)
green_color = (100, 255, 100)

i_color = (52, 180, 235)
j_color = (26, 30, 240)
l_color = (240, 162, 26)
o_color = (245, 233, 10)
s_color = (10, 242, 33)
t_color = (126, 10, 250)
z_color = (245, 17, 29)

overall_score = 0

block_types = ['i', 's', 'j', 't', 'l', 'z', 'o']
active_blocks = [Block(choice(block_types))]
blocked_cells = []

UPDATEBLOCKS = USEREVENT + 1
pygame.time.set_timer(UPDATEBLOCKS, 500, 0)
pygame.mouse.set_visible(False)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == UPDATEBLOCKS:
            for block in active_blocks:
                block.update()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                active_blocks[-1].spin()
            if event.key == pygame.K_SPACE:
                active_blocks[-1].move_down()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                active_blocks[-1].move_down()
            if event.button == 3:
                active_blocks[-1].spin()
    
    active_blocks[-1].get_movement()
    
    screen.fill(black_color)
    draw_game()
    pygame.display.update()
    clock.tick(FPS)