import pygame
import math
pygame.init()
win = pygame.display.set_mode((1000, 1000))

def average_angles(a1, a2):
    # Convert angles to unit vectors
    x1, y1 = math.cos(math.radians(a1)), math.sin(math.radians(a1))
    x2, y2 = math.cos(math.radians(a2)), math.sin(math.radians(a2))

    # Average the vectors
    avg_x = (x1 + x2) / 2
    avg_y = (y1 + y2) / 2

    # Convert the resulting vector back to an angle
    avg_angle = math.degrees(math.atan2(avg_y, avg_x))
    
    return avg_angle

def rotate(origin, point, angle):
    """
    Rotate a point clockwise by a given angle around a given origin.
    The angle should be given in degrees.

    Args:
        origin: The point to rotate around
        point: The point to rotate
        angle: The angle to rotate around in degrees
    """
    angle = math.radians(angle)
    cos = math.cos(angle)
    sin = math.sin(angle)
    ydiff = (point[1] - origin[1])
    xdiff = (point[0] - origin[0])
    
    qx = origin[0] + cos * xdiff - sin * ydiff
    qy = origin[1] + sin * xdiff + cos * ydiff
    return qx, qy

def draw_rounded_polygon(surface, colour, points, border_radius, width):
    wrapped = points + [points[0]]
    angs = [math.degrees(math.atan2(wrapped[i+1][1]-wrapped[i][1], wrapped[i+1][0]-wrapped[i][0]))-90 for i in range(len(wrapped)-1)]
    for i in range(len(points)):
        p1, p2 = points[i], points[i-1]

        a = average_angles(angs[i], angs[i-1])-180
        p1_start = rotate(p1, (p1[0], p1[1]-border_radius/2), angs[i-1])
        p2_end = rotate(p2, (p2[0], p2[1]+border_radius/2), angs[i-1])
        pygame.draw.line(surface, colour, p1_start, p2_end, width)
        p = (
            p1[0]+math.cos(math.radians(a))*border_radius,
            p1[1]+math.sin(math.radians(a))*border_radius
        )
        a1, a2 = -angs[i]%360, -angs[i-1]%360
        if (a2 - a1 + 180) % 360 - 180 > 180:
            a1, a2 = a2, a1
        pygame.draw.arc(surface, colour, 
                        (p[0]-border_radius, p[1]-border_radius, border_radius*2, border_radius*2), 
                        math.radians(a1), math.radians(a2), width)

class Point:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
    
    @property
    def pos(self):
        return (self.x, self.y)
    
    @pos.setter
    def pos(self, value):
        self.x, self.y = value
    
    def constrain(self, opoint, osize=None):
        ox, oy = opoint[0], opoint[1]
        if osize is None:
            osize = opoint[2]
        phi = math.atan2(oy - self.y, ox - self.x)-math.pi
        self.x, self.y = ox+math.cos(phi)*osize, oy+math.sin(phi)*osize
    
    def findOnCircle(self, angle):
        return self.x+math.cos(math.radians(angle))*self.size, self.y+math.sin(math.radians(angle))*self.size
    
    def angleTo(self, opoint):
        return math.degrees(math.atan2(opoint[1] - self.y, opoint[0] - self.x))-180 % 360
    
    def __getitem__(self, key):
        if key == 0:
            return self.x
        elif key == 1:
            return self.y
        elif key == 2:
            return self.size
        else:
            raise IndexError("Index out of range")
    
    def __setitem__(self, key, value):
        if key == 0:
            self.x = value
        elif key == 1:
            self.y = value
        elif key == 2:
            self.size = value
        else:
            raise IndexError("Index out of range")
    
    def __str__(self):
        return f"Point({self.x}, {self.y}, {self.size})"
    def __repr__(self): return str(self)

ps = [Point(250, 250, i) for i in [29, 35, 39, 52, 45]]

clock = pygame.time.Clock()
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
    win.fill((0, 0, 0))

    ps[-1].pos = pygame.mouse.get_pos()
    for i in range(len(ps)-1):
        ps[i].constrain(ps[i+1])#, 25)#42)
    
    newps = []
    tmp = []
    for i in range(len(ps)):
        if i == len(ps) - 1:
            ps2 = [90, 135, 180, -135, -90]
            ang = ps[i - 1].angleTo(ps[i])
        else:
            ang = ps[i].angleTo(ps[i + 1])
            if i == 0:
                ps2 = [-90, -45, 0, 45, 90]
            else:
                ps2 = [90, -90]
        for j in ps2:
            newp = ps[i].findOnCircle(ang + j)
            pygame.draw.circle(win, (255, 50, 50), newp, 2, 3)
            if i == len(ps) - 1 or i == 0:
                newps.append(newp)
            else:
                if j == 90:
                    newps.append(newp)
                else:
                    tmp.append(newp)
    newps.extend(tmp[::-1])
    
    draw_rounded_polygon(win, (10, 255, 50), newps, 10, 5)

    pygame.display.update()
    clock.tick(60)
