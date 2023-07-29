# -*- coding: utf-8 -*-
"""
Created on Mon Jul 10 15:24:32 2023

@author: DELL
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Jul  5 12:13:13 2023
@author: DELL
"""

import pygame
import math
import random

# Initialize Pygame
pygame.init()

# Set up the simulation window
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

# Define constants
N = 15  # Number of agents
radius = 5  # Agent radius
speed = 49  # Agent movement speed
omega_range = (2, 8)  # Range of natural frequencies
K = 0.1    # Coupling strength
dt = 0.01  # Time step
repulsion_radius = 6 * radius  # Radius for collision avoidance
attraction_force = 0.01  # Strength of the attraction force

# Create agents
agents = []
for _ in range(N):
    x = random.uniform(radius, width - radius)
    y = random.uniform(radius, height - radius)
    phase = random.uniform(0, 2 * math.pi)
    omega = random.uniform(*omega_range)
    agents.append((x, y, phase, omega))

# Run the simulation
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))  # Clear the screen

    # Calculate the average position of the swarm
    avg_position = pygame.Vector2()
    for x, y, _, _ in agents:
        avg_position += pygame.Vector2(x, y)
    avg_position /= N

    # Get the cursor position
    cursor_position = pygame.mouse.get_pos()

    for i in range(N):
        x, y, phase, omega = agents[i]

        # Calculate the average phase difference
        avg_phase_diff = 0.0
        for j in range(N):
            if j != i:
                diff = agents[j][2] - phase
                avg_phase_diff += math.sin(diff)
        avg_phase_diff /= N - 1

        # Update the phase using the Kuramoto model
        phase += (omega + K * avg_phase_diff) * dt

        # Update the position based on the phase and steering force
        steering_force = pygame.Vector2(cursor_position) - pygame.Vector2(x, y)
        steering_force = steering_force.normalize()
        steering_force *= 98

        x += (speed * math.cos(phase) + steering_force.x) * dt
        y += (speed * math.sin(phase) + steering_force.y) * dt

        # Wrap around the screen boundaries
        x = x % width
        y = y % height

        agents[i] = (x, y, phase, omega)

        # Apply collision avoidance with other agents
        for j in range(N):
            if j != i:
                dx = agents[j][0] - x
                dy = agents[j][1] - y
                distance = math.sqrt(dx ** 2 + dy ** 2)
                if distance < repulsion_radius:
                    repulsion_force = (repulsion_radius - distance) / distance
                    x -= repulsion_force * dx
                    y -= repulsion_force * dy

        # Apply attraction force towards the average position
        dx = avg_position.x - x
        dy = avg_position.y - y
        x += attraction_force * dx
        y += attraction_force * dy

        # Wrap around the screen boundaries after collision avoidance and attraction
        x = x % width
        y = y % height

        agents[i] = (x, y, phase, omega)

        # Draw the agents as arrow shapes
        arrow_length = radius * 2
        arrow_angle = math.pi / 4  # Angle of the arrowhead
        arrow_points = [
            (x + arrow_length * math.cos(phase), y + arrow_length * math.sin(phase)),
            (x + arrow_length * math.cos(phase + arrow_angle), y + arrow_length * math.sin(phase + arrow_angle)),
            (x + arrow_length * math.cos(phase + math.pi), y + arrow_length * math.sin(phase + math.pi)),
            (x + arrow_length * math.cos(phase - arrow_angle), y + arrow_length * math.sin(phase - arrow_angle))
        ]

        # Draw the arrow shape
        pygame.draw.polygon(screen, (0, 0, 0), arrow_points)

    pygame.display.flip()
    clock.tick(60)  # Limit the frame rate to 60 FPS

pygame.quit()
