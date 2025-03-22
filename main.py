import pygame
from pygame.locals import *
from random import uniform, randint, choice
from random import random
from time import time
from math import copysign, sin, cos, tau


class Firework:
	delete = False
	
	def __init__(self, x, y):
		colors = (
			0x0000ff,
			0x00ff00,
			0x00ffff,
			0xff0000,
			0xff00ff,
			0xffff00,
			0xffffff
		)
		
		self.x = x
		self.y = y
		self.color = choice(colors)
		self.target = uniform(0, screen.get_height()/3)
		
	
	def tick(self):
		if self.y < self.target:
			targ = randint(2, 50)
			velocity = uniform(5, 50)
			offset = tau/targ*random()
			
			for i in range(targ):
				particles.append(FireworkParticle(self.x, self.y, self.color, tau/targ*i+offset, velocity))
			deleted.append(self)
			return
		
		
		self.y -= 10 * dt
	
	
	def render(self):
		pygame.draw.rect(screen, 0x141414, (self.x-5, self.y-10, 10, 10))


class FireworkParticle:
	def __init__(self, x, y, color, angle, vel):
		self.x = x
		self.y = y
		self.color = color
		self.angle = angle
		self.vel = vel
		self.wait = uniform(3, 5)
		self.stime = 0
		self.phase = 0
	
	
	def tick(self):
		change_x = sin(self.angle) * self.vel
		change_y = cos(self.angle) * self.vel
		
		if self.vel < .1:
			change_y += .5
			
			if self.stime == 0:
				self.stime = time()
				self.phase = 1
		
		match self.phase:
			case 1:
				if time() - self.stime > self.wait:
					self.wait = uniform(3, 5)
					self.phase = 2
					self.stime = time()
			
			case 2:
				if time() - self.stime > self.wait:
					deleted.append(self)
		
		self.x += change_x * dt
		self.y += change_y * dt
		
		self.vel *= .95
	
	
	def render(self):
		if self.phase >= 2:
			if (time() - self.stime) * 100 % 50 > 25:
				return
				
		pygame.draw.circle(screen, self.color, (self.x, self.y), 5)


class FireworkLauncher:
	def __init__(self, x):
		self.x = x
		self.y = screen.get_height()
		self.target = None
		self.wait = uniform(.1, 3)
		self.stime = time()
	
	
	def tick(self):
		if time() - self.stime < self.wait:
			return
		
		if self.target is not None:
			if dist1D(self.target, self.x) <= 1:
				self.target = None
			
				self.wait = uniform(.1, 3)
				self.stime = time()
			
			else:
				self.x -= copysign(dt, self.x - self.target)
		
		else:
			if randint(0, 1):
				while self.target is None or 10 > self.target > screen.get_width() - 10:
					self.target = self.x + uniform(-100, 100)
			
			else:
				fireworks.append(Firework(self.x, self.y))
				
				self.wait = uniform(.1, 3)
				self.stime = time()
		
	
	def render(self):
		pygame.draw.rect(screen, 0xffffff, (self.x-10, self.y - 20, 20, 20))
		


def render_debug(obj):
	global debug_coords
	
	x = obj.x
	y = obj.y
	
	debug_coords = x, y
	
	try: targ = obj.target
	except: targ = 0
	
	try: t = obj.wait - (time() - obj.stime)
	except: t = 0
		
	try: color = obj.color
	except: color = 0
	
	if targ is not None: targ = round(targ, 2)
		
	
	t = max(0, t)
	
	x = font.render(f'X: {x:.2f}', True, 0xffffffff)
	y = font.render(f'Y: {y:.2f}', True, 0xffffffff)
	targ = font.render(f'Target: {targ}', True, 0xffffffff)
	t = font.render(f'Time until action: {t:.2f}s', True, 0xffffffff)
	color = font.render(f'Color: #{color:X}', True, color << 8)
	
	screen.blit(x, (0, 0))
	screen.blit(y, (0, 50))
	screen.blit(targ, (0, 100))
	screen.blit(t, (0, 150))
	screen.blit(color, (0, 200))



pygame.init()
screen = pygame.display.set_mode()
clock = pygame.time.Clock()

font = pygame.font.SysFont('arial', 50)


dist1D = lambda a, b: abs(a - b)


deleted = []
particles = []
fireworks = []
launchers = [FireworkLauncher(uniform(10, screen.get_width() - 10)) for i in range(5)]

debug_coords = None

running = True
while running:
	screen.fill(0)
	
	for ev in pygame.event.get():
		if ev.type == QUIT:
			running = False
	
	clock.tick()
	fps = clock.get_fps()
	dt = 60 / fps if fps > 0 else 0
	
	if debug_coords:
		pygame.draw.circle(screen, 0xff0000, debug_coords, 10)
	
	deleted.clear()
	for particle in particles:
		particle.tick()
		particle.render()
	
	for particle in deleted:
		particles.remove(particle)
	
	deleted.clear()
	for firework in fireworks:
		firework.tick()
		firework.render()
	
	for firework in deleted:
		fireworks.remove(firework)
	
	for launcher in launchers:
		launcher.tick()
		launcher.render()
	
	debug_coords = None
	#if particles:
	#	render_debug(particles[0])
	
	pygame.display.flip()


pygame.quit()
