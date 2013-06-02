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
	def __init__(self, position, direction, columns, rows):
		self.position=position
		self.direction=direction
		self.columns=columns
		self.rows=rows
	def move(self):
		if self.direction==0:
			self.position[0]-=1
			self.position[1]+=1	
		elif self.direction==1:
			self.position[1]+=1
		elif self.direction==2:
			self.position[0]+=1
		elif self.direction==3:
			self.position[0]+=1
			self.position[1]-=1
		elif self.direction==4:
			self.position[1]-=1
		else: self.position[0]-=1
		
		if self.position[0]<0:
			self.position[0]+=self.rows
		if self.position[1]<0:
			self.position[1]+=self.columns
		if self.position[0]>=self.rows:
			self.position[0]-=self.rows
		if self.position[1]>=self.columns:
			self.position[1]-=self.columns
		
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
		self.particles=[]
		#self.place_particles(self.particles)
		self.init_particles(particles)
		
	def place_particles(self, particles):
		while particles > 0:
			i = random.randint(0,self.columns-1)
			j = random.randint(0,self.rows-1)
			if self.nodes[i][j] == 0:
				self.nodes[i][j] = 1
				particles -=1
	
	def init_particles(self, p_nr):
		positions=range(self.rows*self.columns)
		random.shuffle(positions)
		for i in range(p_nr):
			self.particles.append(particle([positions[i]/self.columns, positions[i]%self.rows], random.randint(0,5), self.rows, self.columns))
		
	def move(self):
		for particle in self.particles:
			particle.move()
		#self.check_collision()


	
	#def check_collision(self):

		
	def draw(self):
		for p in self.particles:
			pygame.draw.polygon(self.window, (80,80,80), hexagon(((self.rows+self.columns-1)*self.radius/4.+p.position[1]*self.latticevec[0][0]+p.position[0]*self.latticevec[1][0]+1, size[1]/2+p.position[1]*self.latticevec[0][1]+p.position[0]*self.latticevec[1][1]), self.radius-1), 0)
		for i in range(self.rows):
			for j in range(self.columns):
				pygame.draw.polygon(self.window, (200,200,200), hexagon(((self.rows+self.columns-1)*self.radius/4.+j*self.latticevec[0][0]+i*self.latticevec[1][0], size[1]/2+j*self.latticevec[0][1]+i*self.latticevec[1][1]), self.radius), 2)


size=(800,600)			
pygame.init()
fps=pygame.time.Clock()
window=pygame.display.set_mode(size)
(hex_lines, hex_columns)=(30, 40)
hexlatt=hex_lattice(hex_lines, hex_columns, min(int(float(size[0])/(hex_lines+hex_columns-1)/2), int(float(size[1])/(hex_lines+hex_columns))), 50 , window, size)
#~ hexlatt=hex_lattice(5,3,20, window, size)
#~ hex1=hexagon(size, 20)
while 1:
	window.fill(pygame.Color(255,255,255))
	#~ pygame.draw.polygon(window,(0,0,0), hex1, 2)
	hexlatt.draw()
	pygame.display.update()
	hexlatt.move()
	fps.tick(10)
