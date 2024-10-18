import pygame
import math
import sys

pygame.init()
pygame.font.init()

my_font = pygame.font.SysFont("Sans Serif", 20)

fps = 60
background_color = (255, 255, 255)
x = 0
z = 0
y = 0
fpang = 0
x_vel = 0
z_vel = 0
y_vel = 0
speed = 1
friction = 0.8
mouse_x = 0
mouse_y = 0
gravity = 0.4
list_cubes = []

clock = pygame.time.Clock()


def draw3dline(x1, y1, z1, x2, y2, z2):

    radian_fpang = math.radians(fpang)

    center_x = 500
    center_y = 300

    screendistance = 300

    x1diff = x1 - x
    y1diff = y1 - y
    z1diff = z1 - z
    x2diff = x2 - x
    y2diff = y2 - y
    z2diff = z2 - z

    translatedx1 = x1diff * math.cos(radian_fpang) + z1diff * math.sin(radian_fpang)
    translatedz1 = z1diff * math.cos(radian_fpang) - x1diff * math.sin(radian_fpang)
    translatedx2 = x2diff * math.cos(radian_fpang) + z2diff * math.sin(radian_fpang)
    translatedz2 = z2diff * math.cos(radian_fpang) - x2diff * math.sin(radian_fpang)

    if translatedz1 < 0 or translatedz2 < 0:
        return ()

    dispx1 = (translatedx1 / translatedz1) * screendistance + center_x
    dispy1 = (y1diff / translatedz1) * screendistance + center_y
    dispx2 = (translatedx2 / translatedz2) * screendistance + center_x
    dispy2 = (y2diff / translatedz2) * screendistance + center_y

    pygame.draw.line(screen, [0, 0, 0], (1000 - dispx1, 600 - dispy1), (1000 - dispx2, 600 - dispy2))


def draw3dquad(x1, y1, z1, x2, y2, z2, x3, y3, z3, x4, y4, z4, red, green, blue):

    radian_fpang = math.radians(fpang)

    center_x = 500
    center_y = 300

    screen_x = 1000
    screen_y = 600

    screendistance = 300

    x1diff = x1 - x
    y1diff = y1 - y
    z1diff = z1 - z
    x2diff = x2 - x
    y2diff = y2 - y
    z2diff = z2 - z
    x3diff = x3 - x
    y3diff = y3 - y
    z3diff = z3 - z
    x4diff = x4 - x
    y4diff = y4 - y
    z4diff = z4 - z

    translatedx1 = x1diff * math.cos(radian_fpang) + z1diff * math.sin(radian_fpang)
    translatedz1 = z1diff * math.cos(radian_fpang) - x1diff * math.sin(radian_fpang)
    translatedx2 = x2diff * math.cos(radian_fpang) + z2diff * math.sin(radian_fpang)
    translatedz2 = z2diff * math.cos(radian_fpang) - x2diff * math.sin(radian_fpang)
    translatedx3 = x3diff * math.cos(radian_fpang) + z3diff * math.sin(radian_fpang)
    translatedz3 = z3diff * math.cos(radian_fpang) - x3diff * math.sin(radian_fpang)
    translatedx4 = x4diff * math.cos(radian_fpang) + z4diff * math.sin(radian_fpang)
    translatedz4 = z4diff * math.cos(radian_fpang) - x4diff * math.sin(radian_fpang)

    if translatedz1 < 0 or translatedz2 < 0 or translatedz3 < 0 or translatedz4 < 0:
        return ()

    dispx1 = screen_x - ((translatedx1 / translatedz1) * screendistance + center_x)
    dispy1 = screen_y - ((y1diff / translatedz1) * screendistance + center_y)
    dispx2 = screen_x - ((translatedx2 / translatedz2) * screendistance + center_x)
    dispy2 = screen_y - ((y2diff / translatedz2) * screendistance + center_y)
    dispx3 = screen_x - ((translatedx3 / translatedz3) * screendistance + center_x)
    dispy3 = screen_y - ((y3diff / translatedz3) * screendistance + center_y)
    dispx4 = screen_x - ((translatedx4 / translatedz4) * screendistance + center_x)
    dispy4 = screen_y - ((y4diff / translatedz4) * screendistance + center_y)
    pygame.draw.polygon(screen, [red, green, blue],
                        [(dispx1, dispy1), (dispx2, dispy2), (dispx3, dispy3), (dispx4, dispy4)], 0)


def draw3dcube(cubx, cuby, cubz, xwidth, ywidth, zheight):
    draw3dline(cubx, cuby, cubz, cubx+xwidth, cuby, cubz)
    draw3dline(cubx, cuby, cubz, cubx, cuby, cubz + zheight)
    draw3dline(cubx + xwidth, cuby, cubz, cubx + xwidth, cuby, cubz + zheight)
    draw3dline(cubx, cuby, cubz + zheight, cubx + xwidth, cuby, cubz + zheight)

    draw3dline(cubx, cuby + ywidth, cubz, cubx+xwidth, cuby + ywidth, cubz)
    draw3dline(cubx, cuby + ywidth, cubz, cubx, cuby + ywidth, cubz + zheight)
    draw3dline(cubx + xwidth, cuby + ywidth, cubz, cubx + xwidth, cuby + ywidth, cubz + zheight)
    draw3dline(cubx, cuby + ywidth, cubz + zheight, cubx + xwidth, cuby + ywidth, cubz + zheight)

    draw3dline(cubx, cuby, cubz, cubx, cuby + ywidth, cubz)
    draw3dline(cubx + xwidth, cuby, cubz, cubx + xwidth, cuby + ywidth, cubz)
    draw3dline(cubx, cuby, cubz + zheight, cubx, cuby + ywidth, cubz + zheight)
    draw3dline(cubx + xwidth, cuby, cubz + zheight, cubx + xwidth, cuby + ywidth, cubz + zheight)


def fill3dcube(center_x, center_z, base_y, x_width, z_width, y_height, red, green, blue):

    x_corner = round(center_x - x_width/2)
    z_corner = round(center_z - z_width/2)
    max_x = round(center_x + x_width/2)
    max_z = round(center_z + z_width/2)
    max_y = base_y + y_height

    # Base quad
    draw3dquad(x_corner, base_y, z_corner, max_x, base_y, z_corner, max_x, base_y, max_z, x_corner, base_y, max_z,
               red, green, blue)

    # Top Quad
    draw3dquad(x_corner, max_y, z_corner, max_x, max_y, z_corner, max_x, max_y, max_z, x_corner, max_y, max_z,
               red, green, blue)

    # Square without the z direction
    draw3dquad(x_corner, base_y, z_corner, max_x, base_y, z_corner, max_x, max_y, z_corner, x_corner, max_y, z_corner,
               red, green, blue)

    # Square without the x direction
    draw3dquad(x_corner, base_y, z_corner, x_corner, base_y, max_z, x_corner, max_y, max_z, x_corner, max_y, z_corner,
               red, green, blue)

    # Quad with max z
    draw3dquad(x_corner, base_y, max_z, max_x, base_y, max_z,  max_x, max_y, max_z, x_corner, max_y, max_z,
               red, green, blue)

    # Quad with max x
    draw3dquad(max_x, base_y, z_corner, max_x, base_y, max_z, max_x, max_y, max_z, max_x, max_y, z_corner,
               red, green, blue)


class Cubes:
    def __init__(self, number, cubex, cubez, cubey, xwidth, zwidth, yheight, color_r, color_g, color_b):
        self.cubex = number
        self.cubex = cubex
        self.cubez = cubez
        self.cubey = cubey
        self.xwidth = xwidth
        self.zwidth = zwidth
        self.yheight = yheight
        self.color_r = color_r
        self.color_g = color_g
        self.color_b = color_b

    def draw(self):
        fill3dcube(self.cubex, self.cubez, self.cubey, self.xwidth, self.zwidth, self.yheight,
                   self.color_r, self.color_g, self.color_b)


list_cubes.append(Cubes(1, 200, 400, -100, 50, 50, 250, 50, 50, 50))
list_cubes.append(Cubes(2, 200, 400, -100, 60, 60, 20, 50, 50, 50))
list_cubes.append(Cubes(3, 200, 400, 150, 60, 60, 20, 50, 50, 50))
list_cubes.append(Cubes(4, -200, 400, -100, 50, 50, 250, 50, 50, 50))
list_cubes.append(Cubes(5, -200, 400, -100, 60, 60, 20, 50, 50, 50))
list_cubes.append(Cubes(6, -200, 400, 150, 60, 60, 20, 50, 50, 50))
list_cubes.append(Cubes(7, 200, 700, -100, 50, 50, 225, 50, 50, 50))
list_cubes.append(Cubes(8, -200, 700, -100, 50, 50, 225, 50, 50, 50))
list_cubes.append(Cubes(9, 200, 1000, -100, 40, 35, 175, 50, 50, 50))
list_cubes.append(Cubes(10, -200, 1000, -100, 40, 35, 175, 50, 50, 50))
list_cubes.append(Cubes(11, 200, 1300, -100, 40, 30, 100, 50, 50, 50))
list_cubes.append(Cubes(12, -200, 1300, -100, 40, 30, 100, 50, 50, 50))

screen = pygame.display.set_mode(size=(1000, 600))
pygame.display.set_caption('Bens Test Game')
screen.fill(background_color)

pygame.display.flip()

running = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # Ingame Events are processed

    r_radian = math.radians(fpang)

    keys = pygame.key.get_pressed()

    if keys[pygame.K_w]:
        x_vel += speed * (0 - math.cos(math.radians(fpang - 90)))
        z_vel += speed * (0 - math.sin(math.radians(fpang - 90)))

    if keys[pygame.K_s]:
        x_vel -= speed * (0 - math.cos(math.radians(fpang - 90)))
        z_vel -= speed * (0 - math.sin(math.radians(fpang - 90)))

    if keys[pygame.K_d]:
        x_vel += speed * (0 - math.cos(math.radians(fpang)))
        z_vel += speed * (0 - math.sin(math.radians(fpang)))
    if keys[pygame.K_a]:
        x_vel -= speed * (0 - math.cos(math.radians(fpang)))
        z_vel -= speed * (0 - math.sin(math.radians(fpang)))
    if keys[pygame.K_SPACE]:
        if y == 0:
            y_vel += 10
    if keys[pygame.K_h]:
        pygame.display.quit()
        sys.exit()
    # Physics

    if y > 0:
        y_vel -= gravity
    elif y < 0:
        y = 0
        y_vel = 0

    y += y_vel
    x += x_vel
    z += z_vel
    if abs(x_vel) > 0.1:
        x_vel *= friction
    else:
        x_vel = 0

    if abs(z_vel) > 0.1:
        z_vel *= friction
    else:
        z_vel = 0

    # Mouse movement

    (mouse_x, mouse_y) = pygame.mouse.get_rel()
    fpang += (mouse_x/4)
    pygame.mouse.set_pos(500, 300)
    pygame.mouse.set_visible(False)

    # Text is rendered
    text_surface = my_font.render("x: " + str(round(x)) + " z: "+ str(round(z)) + " y: " + str(round(y)), False, (0, 0, 0))

    # Graphics are drawn
    screen.fill(background_color)

    for obj in list_cubes:
        obj.draw()

    screen.blit(text_surface, (0, 0))
    pygame.display.update()

    clock.tick(fps)
