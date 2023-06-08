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
speed = 2  # Agent movement speed
omega_range = (0.5, 2.0)  # Range of natural frequencies
K = 1.0  # Coupling strength
dt = 0.1  # Time step
repulsion_radius = 6 * radius  # Radius for collision avoidance
attraction_force = 0.01  # Strength of the attraction force
steering_force = pygame.Vector2(1, 0)  # Steering force direction for the swarm

# Create agents
agents = []
for _ in range(N):
    x = random.uniform(radius, width - radius)
    y = random.uniform(radius, height - radius)
    phase = random.uniform(0, 2 * math.pi)
    omega = random.uniform(*omega_range)
    agents.append((x, y, phase, omega))

# Define hurdles
num_hurdles = 3
hurdles = []
for _ in range(num_hurdles):
    hurdle_x = random.uniform(radius, width - radius)
    hurdle_y = random.uniform(radius, height - radius)
    hurdles.append((hurdle_x, hurdle_y))

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

        # Apply collision avoidance with hurdles
        for hurdle in hurdles:
            hurdle_x, hurdle_y = hurdle
            dx = hurdle_x - x
            dy = hurdle_y - y
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

        # Draw the agents as circles
        pygame.draw.circle(screen, (0, 0, 0), (int(x), int(y)), radius)

    # Draw hurdles as rectangles
    for hurdle in hurdles:
        hurdle_x, hurdle_y = hurdle
        pygame.draw.rect(screen, (255, 0, 0), (hurdle_x - radius, hurdle_y - radius, radius * 2, radius * 2))

    pygame.display.flip()
    clock.tick(60)  # Limit the frame rate to 60 FPS

pygame.quit()
