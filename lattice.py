#!/usr/bin/python

import pygame, math, random, pdb

def hexagon(center, radius):
	upperleft=(center[0]-radius/math.sqrt(3), center[1]-radius)
	upperright=(center[0]+radius/math.sqrt(3), center[1]-radius)
	lowerleft=(center[0]-radius/math.sqrt(3), center[1]+radius)
	lowerright=(center[0]+radius/math.sqrt(3), center[1]+radius)
	left=(center[0]-2/math.sqrt(3)*radius, center[1])
	right=(center[0]+2/math.sqrt(3)*radius, center[1])
	return (upperleft, upperright, right, lowerright, lowerleft, left)

class particle:
	#direction: 0 up, clockwise up to 5
	def __init__(self, position, direction):
		self.position=position
		self.direction=direction
	#~ def move(self):
		
class hex_lattice:
	def __init__(self,rows, columns, r, particles, window, size):
		self.rows=rows
		self.columns=columns
		#each node has a value for the position and one for the movement direction
		self.nodes=[[0 for i in range(columns)] for j in range(rows)]
		self.radius=r
		self.particles=particles
		self.r_u=r/math.sqrt(3)*2.
		self.latticevec=((self.r_u*1.5, self.radius), (self.r_u*1.5, -self.radius))
		self.window=window
		self.size=size
		self.place_particles(self.particles)
		
	def place_particles(self, particles):
		while particles > 0:
			i = random.randint(0,self.columns-1)
			j = random.randint(0,self.rows-1)
			if self.nodes[i][j] == 0:
				self.nodes[i][j] = 1
				particles -=1
	
	#~ def check_collision(self):
		
	def draw(self):
		for i in enumerate(self.nodes):
			for j in enumerate(i[1]):
				if j[1]==1:
					pygame.draw.polygon(self.window, (80,80,80), hexagon(((self.rows+self.columns-1)*self.radius/4.+j[0]*self.latticevec[0][0]+i[0]*self.latticevec[1][0]+1, size[1]/2+j[0]*self.latticevec[0][1]+i[0]*self.latticevec[1][1]), self.radius-1), 0)
				pygame.draw.polygon(self.window, (200,200,200), hexagon(((self.rows+self.columns-1)*self.radius/4.+j[0]*self.latticevec[0][0]+i[0]*self.latticevec[1][0], size[1]/2+j[0]*self.latticevec[0][1]+i[0]*self.latticevec[1][1]), self.radius), 2)


size=(800,600)			
pygame.init()
fps=pygame.time.Clock()
window=pygame.display.set_mode(size)
(hex_lines, hex_columns)=(10, 10)
hexlatt=hex_lattice(hex_lines, hex_columns, min(int(float(size[0])/(hex_lines+hex_columns-1)/2), int(float(size[1])/(hex_lines+hex_columns))), 50 , window, size)
#~ hexlatt=hex_lattice(5,3,20, window, size)
#~ hex1=hexagon(size, 20)
while 1:
	window.fill(pygame.Color(255,255,255))
	#~ pygame.draw.polygon(window,(0,0,0), hex1, 2)
	hexlatt.draw()
	pygame.display.update()
	fps.tick(3)
