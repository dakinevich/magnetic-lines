import pygame
import math
import time


def ti_norm(n):
    lengh = (n[0]**2 + n[1]**2)**0.5
    if lengh == 0:
        return[0, 0]
    return [n[0]/lengh, n[1]/lengh]


def ultra_sum(lst):
    return [sum([i[0] for i in lst]), sum([i[1] for i in lst])]


class MagnetPoint():
    def __init__(self, is_plus, x, y):
        self.is_plus = is_plus
        self.x = x
        self.y = y

    def culc_for_poit(self, x, y):
        state = 1
        lengh = ((x - self.x)**2 + (y - self.y)**2)
        xs = 0 if x == self.x else ((x - self.x)/lengh)*self.is_plus
        ys = 0 if y == self.y else ((y - self.y)/lengh)*self.is_plus
        return (xs, ys, state)

    def blit(self, screen):
        pygame.draw.circle(screen, (255, 0, 0), (self.x, self.y), 3)

    def get_trasers(self, n, r):
        ts = []
        dl = 360/n
        for i in range(n):
            ts.append(Traser(
                self.x + math.cos(math.radians(i*dl))*r,
                self.y + math.sin(math.radians(i*dl))*r))
        return ts


class Traser():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def next_iter(self, screen, points, iter_lengh):
        n_p = [i.culc_for_poit(self.x, self.y) for i in points]
        n_p = ti_norm(ultra_sum(n_p))
        n_x = self.x + n_p[0]*iter_lengh
        n_y = self.y + n_p[1]*iter_lengh
        pygame.draw.line(screen, (0, 0, 255), [self.x, self.y], [n_x, n_y], 1)
        self.x, self.y = n_x, n_y


pygame.init()

w, h = 1500, 750
iter_lengh = 4
display = pygame.display.set_mode((w, h))

points = []
points.append(MagnetPoint(1, 700, 200))
points.append(MagnetPoint(1, 200, 200))
points.append(MagnetPoint(-1, 700, 700))
trasers = []
for p in points:
    trasers += p.get_trasers(100, 3)

# prerender
display.fill((0, 0, 0))
[i.blit(display) for i in points]


running = True
mouse_pressed = False
t = time.time()
t1 = time.time()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    m_x, m_y = pygame.mouse.get_pos()

    if event.type == pygame.MOUSEBUTTONDOWN and not mouse_pressed:
        trasers += MagnetPoint(1, m_x, m_y).get_trasers(1, 0)
        mouse_pressed = True
    elif not event.type == pygame.MOUSEBUTTONDOWN:
        mouse_pressed = False

    # res = np.zeros((1366, 768), dtype=np.int32)
    # res = np.stack((res.astype(int),)*3, axis=-1)

    # pygame.surfarray.blit_array(display, res)
    # pygame.draw.circle(display, (0, 0, 255), (250, 250), 75)

    [i.next_iter(display, points, iter_lengh) for i in trasers]
    # [i.blit(display) for i in points]

    if time.time() > t1 + 1:
        to_pop = []
        for i in range(len(trasers)-1):
            trs = trasers[i]
            if not(-w < trs.x < 2*w) or not(-h < trs.y < 2*h):
                to_pop.append(i)
        [trasers.pop(i) for i in to_pop[::-1]]
        t1 = time.time()
    if time.time() > t + 0.01:
        pygame.display.flip()
        t = time.time()
    # display.fill((255, 255, 255))

pygame.quit()
