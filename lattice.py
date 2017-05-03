#!/usr/bin/python

import pygame, math, random, pdb


def hexagon(center, radius):
    upperleft = (center[0] - radius / math.sqrt(3), center[1] - radius)
    upperright = (center[0] + radius / math.sqrt(3), center[1] - radius)
    lowerleft = (center[0] - radius / math.sqrt(3), center[1] + radius)
    lowerright = (center[0] + radius / math.sqrt(3), center[1] + radius)
    left = (center[0] - 2 / math.sqrt(3) * radius, center[1])
    right = (center[0] + 2 / math.sqrt(3) * radius, center[1])
    return (upperleft, upperright, right, lowerright, lowerleft, left)


class Particle:
    # direction: 0 up, clockwise up to 5
    def __init__(self, position, direction, columns, rows, lattice_vec, radius, color=(80, 80, 80)):
        self.position = position
        self.direction = direction
        self.columns = columns
        self.rows = rows
        self.color = color
        self.lattice_vec = lattice_vec
        self.radius = radius

    def move(self, nodes):
        nodes[self.position[0]][self.position[1]].remove(self)

        if self.direction == 0:
            self.position[0] -= 1
            self.position[1] += 1
        elif self.direction == 1:
            self.position[1] += 1
        elif self.direction == 2:
            self.position[0] += 1
        elif self.direction == 3:
            self.position[0] += 1
            self.position[1] -= 1
        elif self.direction == 4:
            self.position[1] -= 1
        else:
            self.position[0] -= 1

        if self.position[0] < 0:
            self.position[0] += self.rows
        if self.position[1] < 0:
            self.position[1] += self.columns
        if self.position[0] >= self.rows:
            self.position[0] -= self.rows
        if self.position[1] >= self.columns:
            self.position[1] -= self.columns

        try:
            nodes[self.position[0]][self.position[1]].append(self)
        except IndexError:
            pdb.set_trace()

    def draw(self, window):
        center = ((self.rows + self.columns - 1) * self.radius / 4.
                       + self.position[0] * self.lattice_vec[0][0]
                       + self.position[1] * self.lattice_vec[1][0] + 1,
                   size[1] / 2 + self.position[0] * self.lattice_vec[0][1]
                       + self.position[1] * self.lattice_vec[1][1])
        pygame.draw.polygon(window, self.color, hexagon(center, self.radius - 1), 0)


class HexLattice:
    def __init__(self, rows, columns, r, particles, window, size):
        self.rows = rows
        self.columns = columns
        # each node has a value for the position and one for the movement direction
        self.nodes = [[[] for i in range(columns)] for j in range(rows)]
        self.radius = r
        self.r_u = r / math.sqrt(3) * 2.
        self.latticevec = ((self.r_u * 1.5, self.radius), (self.r_u * 1.5, -self.radius))
        self.window = window
        self.size = size
        self.particles = []
        self.initialize_particles(particles)

    def initialize_particles(self, particle_number):
        positions = range(self.rows * self.columns)
        random.shuffle(positions)
        for i in range(particle_number):
            color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            self.particles.append(Particle([positions[i] / self.columns, positions[i] % self.rows],
                                           random.randint(0, 5), self.columns, self.rows,
                                           self.latticevec, self.radius, color))
            self.nodes[positions[i] / self.columns][positions[i] % self.rows].append(
                self.particles[-1])

    def init_testparticles(self, p_nr):
        if p_nr == 3:
            self.particles.append(
                Particle([self.columns / 2, self.rows / 2], 0, self.columns, self.rows,
                         (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))))
            self.particles.append(
                Particle([self.columns / 2, self.rows / 2], 2, self.columns, self.rows,
                         (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))))
            self.particles.append(
                Particle([self.columns / 2, self.rows / 2], 4, self.columns, self.rows,
                         (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))))
            for p in self.particles:
                self.nodes[p.position[0]][p.position[1]].append(p)
                p.move(self.nodes)
                p.direction = (p.direction + 3) % 6
        else:
            self.particles.append(
                Particle([self.columns / 2, self.rows / 2], 0, self.columns, self.rows,
                         (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))))
            self.particles.append(
                Particle([self.columns / 2, self.rows / 2], 3, self.columns, self.rows,
                         (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))))
            for p in self.particles:
                self.nodes[p.position[0]][p.position[1]].append(p)
                p.move(self.nodes)
                p.direction = (p.direction + 3) % 6

    def move(self):
        for particle in self.particles:
            particle.move(self.nodes)
        self.check_collision()

    def check_collision(self):
        for i in range(len(self.nodes)):
            for j in range(len(self.nodes[i])):
                if len(self.nodes[i][j]) == 2:
                    if abs(self.nodes[i][j][0].direction - self.nodes[i][j][1].direction) == 3:
                        if random.randint(0, 1) == 0:
                            self.nodes[i][j][1].direction = (self.nodes[i][j][0].direction - 2) % 6
                            self.nodes[i][j][0].direction = (self.nodes[i][j][0].direction + 1) % 6
                        else:
                            self.nodes[i][j][1].direction = (self.nodes[i][j][0].direction + 2) % 6
                            self.nodes[i][j][0].direction = (self.nodes[i][j][0].direction - 1) % 6
                elif len(self.nodes[i][j]) == 3:
                    self.nodes[i][j][0].direction = (self.nodes[i][j][0].direction + 3) % 6
                    self.nodes[i][j][1].direction = (self.nodes[i][j][1].direction + 3) % 6
                    self.nodes[i][j][2].direction = (self.nodes[i][j][2].direction + 3) % 6

    def draw(self):
        for p in self.particles:
            p.draw(self.window)
        for i in range(self.rows):
            for j in range(self.columns):
                center =((self.rows + self.columns - 1) * self.radius / 4.
                             + i *self.latticevec[0][0]
                             + j * self.latticevec[1][0],
                          size[1] / 2 + i * self.latticevec[0][1]
                             + j * self.latticevec[1][1]
                         )
                pygame.draw.polygon(self.window, (200, 200, 200), hexagon(center, self.radius), 2)


size = (800, 600)
pygame.init()
fps = pygame.time.Clock()
window = pygame.display.set_mode(size)
(hex_lines, hex_columns) = (50, 50)
hexlatt = HexLattice(hex_lines, hex_columns,
                     min(int(float(size[0]) / (hex_lines + hex_columns - 1) / 2),
                         int(float(size[1]) / (hex_lines + hex_columns))),
                     500, window, size)

while 1:
    window.fill(pygame.Color(255, 255, 255))
    hexlatt.draw()
    pygame.display.update()
    hexlatt.move()
    fps.tick(10)
