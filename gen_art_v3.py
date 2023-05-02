import random, math, pygame


def radians(degrees):
    """convert degrees to radians"""
    return math.pi / 180 * degrees


def blue(scale=0.8):
    """return the rgb of a shade of blue"""
    assert 0 <= scale <= 1, f"scale must be between 0 and 1 inclusive, not {scale}"
    num = int(scale * 255)
    return (num // 2, 2 * num // 3, num)


class Node:
    def __init__(self, x, y, speed, angle):
        """create a node"""
        self.x = x
        self.y = y
        self.speed = speed
        self.angle = angle
        self.dx = math.sin(self.angle) * self.speed
        self.dy = math.cos(self.angle) * self.speed

    def move(self):
        """move the node"""
        self.x = self.x + self.dx
        self.y = self.y + self.dy

    def draw(self):
        """draw the node to the screen"""
        pygame.draw.circle(screen, blue(), (int(self.x), int(self.y)), node_radius)

    def reflect(self):
        """reflect off a boundary of the screen"""
        if self.x > winwidth - node_radius:  # right edge
            self.x = 2 * (winwidth - node_radius) - self.x
            self.angle = -self.angle
        elif self.x < node_radius:  # left edge
            self.x = 2 * node_radius - self.x
            self.angle = -self.angle
        if self.y > winheight - node_radius:  # bottom edge
            self.y = 2 * (winheight - node_radius) - self.y
            self.angle = math.pi - self.angle
        elif self.y < node_radius:  # top edge
            self.y = 2 * node_radius - self.y
            self.angle = math.pi - self.angle
        self.dx = math.sin(self.angle) * self.speed
        self.dy = math.cos(self.angle) * self.speed


winwidth = 800  # width of window
winheight = 600  # height of window
background = (5, 5, 5)  # this is close to black

# set generative parameters
gridsize = 40

def _hash(x, y):
    return x // gridsize, y // gridsize

num_nodes = 600
node_radius = 0
thresh = gridsize ** 2

# initialize pygame
screen = pygame.display.set_mode((winwidth, winheight))
clock = pygame.time.Clock()
pygame.init()
pygame.display.set_caption("Triangles v3")
pygame.event.set_allowed([pygame.QUIT, pygame.KEYUP, pygame.KEYDOWN])

# create nodes
nodes = []
count = 0
while count < num_nodes:
    x = random.randint(0, winwidth)
    y = random.randint(0, winheight)
    if (
        (x - winwidth / 4) ** 2 + (y - winheight / 4) ** 2 > 250 ** 2
        and (x - winwidth) ** 2 + (y - winheight) ** 2 > 425 ** 2
        and x ** 2 + (y - winheight) ** 2 > 200 ** 2
        and (x - winwidth) ** 2 + y ** 2 > 175 ** 2
    ):
        speed = random.randint(150, 200) / 600
        angle = radians(random.randint(0, 359))
        nodes.append(Node(x, y, speed, angle))
        count += 1

# the game loop: (press q to quit)
quit = False
while not quit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit = True
            break
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                quit = True
                break
    if quit:
        break

    screen.fill(background)
    for node in nodes:
        node.move()
        node.reflect()
        node.draw()

    hashmap = {}
    for node in nodes:
        hashmap.setdefault(_hash(int(node.x), int(node.y)), []).append(node)

    for key in hashmap.keys():
        local_nodes = hashmap[key]
        for i, node1 in enumerate(local_nodes):
            for node2 in local_nodes[i + 1 :]:
                x1, y1 = node1.x, node1.y
                x2, y2 = node2.x, node2.y
                d_squared = (x1 - x2) ** 2 + (y1 - y2) ** 2
                if d_squared < thresh:
                    pygame.draw.aaline(
                        screen,
                        blue((thresh - d_squared) / thresh),
                        (x1, y1),
                        (x2, y2),
                    )

    clock.tick()
    pygame.display.flip()
    print(clock.get_fps())

pygame.quit()
