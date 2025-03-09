import pygame
import math

# Initialisation de Pygame
pygame.init()

# Configuration de l'écran
WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Système Solaire")

# Couleurs
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
GRAY = (128, 128, 128)

# Constantes
G = 6.67430e-11
SCALE = 100 / 1.5e11  # 1.5e11 m = 100 pixels
TIME_STEP = 3600 * 24  # 1 jour en secondes
zoom_factor = 1.0

class CelestialBody:
    def __init__(self, name, x, y, radius, color, mass, velocity_x, velocity_y):
        self.name = name
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.orbit = []

    def update_position(self, bodies):
        total_fx = total_fy = 0
        for other in bodies:
            if self == other:
                continue
            dx = other.x - self.x
            dy = other.y - self.y
            distance = math.sqrt(dx**2 + dy**2)
            force = (G * self.mass * other.mass) / (distance**2)
            theta = math.atan2(dy, dx)
            fx = math.cos(theta) * force
            fy = math.sin(theta) * force
            total_fx += fx
            total_fy += fy
        
        self.velocity_x += (total_fx / self.mass) * TIME_STEP
        self.velocity_y += (total_fy / self.mass) * TIME_STEP
        self.x += self.velocity_x * TIME_STEP
        self.y += self.velocity_y * TIME_STEP
        self.orbit.append((self.x, self.y))

    def draw(self):
        x = int(self.x * SCALE * zoom_factor + WIDTH // 2)
        y = int(self.y * SCALE * zoom_factor + HEIGHT // 2)
        if len(self.orbit) > 2:
            pygame.draw.lines(screen, self.color, False, [(int(px * SCALE * zoom_factor + WIDTH // 2), int(py * SCALE * zoom_factor + HEIGHT // 2)) for px, py in self.orbit], 1)
        pygame.draw.circle(screen, self.color, (x, y), max(1, int(self.radius * zoom_factor)))

class Moon(CelestialBody):
    def __init__(self, name, planet, distance, radius, color, mass, velocity):
        # Position de la lune à une distance initiale de la planète sur une orbite circulaire
        # Placer la lune à un angle de 90° (en haut de la planète sur l'axe Y)
        angle = math.pi / 2  # Placer la lune au-dessus de la planète
        
        x_position = planet.x + distance * math.cos(angle)
        y_position = planet.y + distance * math.sin(angle)
        
        # Calcul de la vitesse orbitale initiale pour maintenir l'orbite circulaire
        orbital_velocity = math.sqrt(G * planet.mass / distance)
        
        # Initialisation avec une vitesse perpendiculaire à la ligne reliant la planète et la lune
        velocity_x = -orbital_velocity * math.sin(angle)  # Vitesse horizontale perpendiculaire
        velocity_y = orbital_velocity * math.cos(angle)   # Vitesse verticale perpendiculaire
        
        super().__init__(name, x_position, y_position, radius, color, mass, velocity_x, velocity_y)
        self.planet = planet
        self.distance = distance  # Garde la distance par rapport à la planète

    def update_position(self, bodies):
        # Calcul de la force gravitationnelle de la planète
        dx = self.planet.x - self.x
        dy = self.planet.y - self.y
        distance_to_planet = math.sqrt(dx**2 + dy**2)
        
        # Calculer la force gravitationnelle exercée par la planète sur la lune
        force_planet = (G * self.mass * self.planet.mass) / (distance_to_planet**2)
        angle = math.atan2(dy, dx)
        
        # Mise à jour de la vitesse de la lune en fonction de la gravité de la planète
        fx_planet = math.cos(angle) * force_planet
        fy_planet = math.sin(angle) * force_planet
        
        # Appliquer la vitesse à la lune (mouvement à cause de la planète)
        self.velocity_x += (fx_planet / self.mass) * TIME_STEP
        self.velocity_y += (fy_planet / self.mass) * TIME_STEP
        
        # Maintenant, on doit prendre en compte l'attraction des autres corps, mais de façon limitée
        total_fx = total_fy = 0
        for other in bodies:
            if self == other or other == self.planet:
                continue
            dx = other.x - self.x
            dy = other.y - self.y
            distance = math.sqrt(dx**2 + dy**2)
            force = (G * self.mass * other.mass) / (distance**2)
            angle = math.atan2(dy, dx)
            fx = math.cos(angle) * force
            fy = math.sin(angle) * force
            
            # Limiter l'effet de ces autres corps sur la lune pour éviter qu'elle s'éloigne trop
            total_fx += fx / 10  # Diviser par 10 pour réduire l'impact
            total_fy += fy / 10  # Diviser par 10 pour réduire l'impact
        
        # Réduire l'influence gravitationnelle du Soleil sur la lune
        if isinstance(self.planet, CelestialBody) and self.planet == earth:  # Si c'est une lune de la Terre, réduire l'influence du Soleil
            for other in bodies:
                if other == sun:  # Si le corps en question est le Soleil
                    dx = other.x - self.x
                    dy = other.y - self.y
                    distance = math.sqrt(dx**2 + dy**2)
                    force_sun = (G * self.mass * other.mass) / (distance**2)
                    force_sun /= 50  # Réduire l'influence gravitationnelle du Soleil (facteur de 50)
                    angle_sun = math.atan2(dy, dx)
                    fx_sun = math.cos(angle_sun) * force_sun
                    fy_sun = math.sin(angle_sun) * force_sun
                    total_fx += fx_sun / 10
                    total_fy += fy_sun / 10

        # Appliquer ces forces supplémentaires à la vitesse de la lune
        self.velocity_x += (total_fx / self.mass) * TIME_STEP
        self.velocity_y += (total_fy / self.mass) * TIME_STEP
        
        # Mise à jour de la position de la lune
        self.x += self.velocity_x * TIME_STEP
        self.y += self.velocity_y * TIME_STEP
        
        # Ajouter l'orbite de la lune
        self.orbit.append((self.x, self.y))


# Création des planètes et lunes
sun = CelestialBody("Soleil", 0, 0, 30, YELLOW, 1.989e30, 0, 0)
earth = CelestialBody("Terre", 1.5e11, 0, 10, BLUE, 5.972e24, 0, 29780)
mars = CelestialBody("Mars", 2.28e11, 0, 7, RED, 6.39e23, 0, 24070)
jupiter = CelestialBody("Jupiter", 7.78e11, 0, 20, ORANGE, 1.898e27, 0, 13070)

moon = Moon("Lune", earth, 3.84e8, 3, GRAY, 7.35e22, 1022)
phobos = Moon("Phobos", mars, 9.38e6, 2, GRAY, 1.07e16, 2138)
deimos = Moon("Deimos", mars, 2.34e7, 2, GRAY, 1.48e15, 1351)

bodies = [sun, earth, mars, jupiter, moon, phobos, deimos]

running = True
while running:
    screen.fill(BLACK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                zoom_factor *= 1.1  # Zoom in
            elif event.key == pygame.K_DOWN:
                zoom_factor /= 1.1  # Zoom out
    
    for body in bodies:
        body.update_position(bodies)
        body.draw()
    
    pygame.display.flip()
    pygame.time.delay(50)

pygame.quit()