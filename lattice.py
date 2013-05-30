#!/usr/bin/python

import pygame
import math

def hexagon(center, radius):
	upperleft=(center[0]-radius/math.sqrt(3), center[1]-radius)
	upperright=(center[0]+radius/math.sqrt(3), center[1]-radius)
	lowerleft=(center[0]-radius/math.sqrt(3), center[1]+radius)
	lowerright=(center[0]+radius/math.sqrt(3), center[1]+radius)
	left=(center[0]-2/math.sqrt(3)*radius, center[1])
	right=(center[0]+2/math.sqrt(3)*radius, center[1])
	return (upperleft, upperright, right, lowerright, lowerleft, left)
	
class hex_lattice:
	def __init__(self,rows, columns, r, window, size):
		self.nodes=[[0 for i in range(columns)] for j in range(rows)]
		self.radius=r
		self.r_u=r/math.sqrt(3)*2.
		self.latticevec=((self.r_u*1.5, self.radius), (self.r_u*1.5, -self.radius))
		self.window=window
		self.size=size
	def draw(self):
		for i in enumerate(self.nodes):
			for j in enumerate(i[1]):
				if j[1]==0:
					pygame.draw.polygon(self.window, (200,200,200), hexagon((j[0]*self.latticevec[0][0]+i[0]*self.latticevec[1][0], size[1]/2+j[0]*self.latticevec[0][1]+i[0]*self.latticevec[1][1]), self.radius), 1)
				else:
					pygame.draw.polygon(self.window, (0,0,0), hexagon((j[0]*self.latticevec[0][0]+i[0]*self.latticevec[1][0], size[1]/2+j[0]*self.latticevec[0][1]+i[0]*self.latticevec[1][1]), self.radius), 0)


size=(800,600)			
pygame.init()
fps=pygame.time.Clock()
window=pygame.display.set_mode(size)
(hex_lines, hex_columns)=(10, 10)
hexlatt=hex_lattice(hex_lines, hex_columns, min(int(float(size[0])/(hex_lines+hex_columns-1)/2), int(float(size[1])/(hex_lines+hex_columns))) , window, size)
#~ hexlatt=hex_lattice(5,3,20, window, size)
#~ hex1=hexagon(size, 20)
while 1:
	window.fill(pygame.Color(255,255,255))
	#~ pygame.draw.polygon(window,(0,0,0), hex1, 2)
	hexlatt.draw()
	pygame.display.update()
	fps.tick(30)
