#!/usr/bin/env python
# coding=utf-8
# Boid implementation in Python using PyGame
from __future__ import division  # required in Python 2.7
import sys
import numpy
import pygame
#import modules.boid
sys.path.append("..")

from modules.boid import *

# === main === (lower_case names)

# --- init ---

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Set the title of the window
pygame.display.set_caption('Boids')

# --- objects ---

# lists
boid_list = pygame.sprite.Group()
# This is a list of every sprite.
all_sprites_list = pygame.sprite.Group()

# --- create boids and obstacles at random positions on the screen ---

# Place boids
for i in range(NUM_BOIDS):
    boid = Boid(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT),
                100, 40, 5, 10, 100, 60, MAX_BOID_VELOCITY, "resources/img/boid.png")
    # Add the boid to the lists of objects
    boid_list.add(boid)
    all_sprites_list.add(boid)

# --- mainloop ---

clock = pygame.time.Clock()

running = True

while running:

    # --- events ---

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    # --- updates ---

    # Scan for boids and predators to pay attention to
    for boid in boid_list:
        closeboid = []
        for otherboid in boid_list:
            if otherboid == boid:
                continue
            distance = boid.distance(otherboid, False)
            if distance < 200:
                closeboid.append(otherboid)

        # TODO Make boids do something random if they do not move
        # Attempt to initiate random movement if there is a standstill
        # if len(closeboid) == 0:
        #     print boid.velocityY
        # Apply the rules of the boids
        boid.cohesion(closeboid)
        boid.alignment(closeboid)
        boid.separation(closeboid, 20)

        # Attempt to initiate random movement if there is a standstill
        # Neither of these if statements work
        # if -0.1 <= boid.velocityX <= 0.1 and -0.1 <= boid.velocityY <= 0.1:
        # if boid.velocityX == 0 and boid.velocityY == 0:
        #     boid.go_to_middle()
        #     print boid.velocityY
        boid.update(False)

        # --- draws ---

    # Background colour
    screen.fill(BLACK)

    # Draw all the spites
    all_sprites_list.draw(screen)

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
    pygame.time.delay(10)
    # Used to manage how fast the screen updates
    clock.tick(120)

# --- the end ---
pygame.quit()
sys.exit()
