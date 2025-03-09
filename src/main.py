"""
@file main.py
@brief Animation du système solaire simplifié en utilisant Matplotlib.

Ce script crée une animation du système solaire simplifié avec le Soleil, des planètes et leurs lunes.
Il utilise les classes Star, Planet et Moon pour modéliser les objets célestes.

@author Pierre JAUFFRES
@date 2025-02-22
"""
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from space_objects import Star, Planet, Moon
from functions import get_orbit, update
import matplotlib.colors as mcolors

# Création du Soleil
sun = Star("Soleil", size=12, mass=1.989e30, diameter_km=1392000, color="#FFD700")

# Création des planètes
# Planètes
planets_full = [
    Planet("Mercure", 3, sun, 0.39, 0.205, 0.24, diameter_km=4879, color='#B4B4B4'),
    Planet("Vénus", 6, sun, 0.72, 0.007, 0.62, diameter_km=12104, color='#D5C79E'),
    Planet("Terre", 6, sun, 1.0, 0.017, 1.0, diameter_km=12742, color='#1E90FF'),
    Planet("Mars", 4, sun, 1.52, 0.093, 1.88, diameter_km=6779, color='#FF4500'),
    Planet("Jupiter", 8, sun, 5.2, 0.048, 11.86, diameter_km=139822, color="#D97F1F"),
    Planet("Saturne", 9, sun, 9.58, 0.056, 29.46, diameter_km=116460, color="#F4C200"),
    Planet("Uranus", 7, sun, 19.18, 0.046, 84.01, diameter_km=50724, color="#4A9B8F"),
    Planet("Neptune", 8, sun, 30.07, 0.010, 164.8, diameter_km=49244, color="#4C6A92"),
]

# Création des lunes
moons_full = [
    # Lunes de la Terre
    Moon("Lune", 2, planets_full[2], 0.05, 12, diameter_km=3474, color="#D3D3D3"),  # Lune de la Terre
    # Lunes de Mars
    Moon("Phobos", 1, planets_full[3], 0.01, 8, diameter_km=22, color="#6D6D6D"),  # Lune de Mars
    Moon("Deimos", 1, planets_full[3], 0.02, 16, diameter_km=12, color="#A8A8A8"),  # Lune de Mars
    # Lunes de Jupiter
    Moon("Io", 1, planets_full[4], 0.0035, 9, diameter_km=3643, color="#F4A300"),  # Lune de Jupiter
    Moon("Europe", 1, planets_full[4], 0.009, 10, diameter_km=3121, color="#B0E0E6"),  # Lune de Jupiter
    Moon("Ganymède", 1, planets_full[4], 0.015, 11, diameter_km=5268, color="#C0C0C0"),  # Lune de Jupiter
    Moon("Callisto", 1, planets_full[4], 0.02, 13, diameter_km=4821, color="#8B7D7B"),  # Lune de Jupiter
    # Lunes de Saturne
    Moon("Titan", 1, planets_full[5], 0.012, 22, diameter_km=5150, color="#D17A27"),  # Lune de Saturne
    Moon("Rhéa", 1, planets_full[5], 0.03, 10, diameter_km=1528, color="#C0C0C0"),  # Lune de Saturne
    Moon("Iapetus", 1, planets_full[5], 0.075, 15, diameter_km=1469, color="#2F2F2F"),  # Lune de Saturne
    Moon("Dione", 1, planets_full[5], 0.075, 10, diameter_km=1123, color="#DCDCDC"),  # Lune de Saturne
    Moon("Téthys", 1, planets_full[5], 0.078, 10, diameter_km=1062, color="#F8F8FF"),  # Lune de Saturne
    # Lunes d'Uranus
    Moon("Miranda", 1, planets_full[6], 0.008, 6, diameter_km=471, color="#B0C4DE"),  # Lune d'Uranus
    Moon("Ariel", 1, planets_full[6], 0.015, 8, diameter_km=1157, color="#7EC8E6"),  # Lune d'Uranus
    Moon("Umbriel", 1, planets_full[6], 0.019, 7, diameter_km=1169, color="#4B4B4B"),  # Lune d'Uranus
    Moon("Titania", 1, planets_full[6], 0.03, 9, diameter_km=1578, color="#A3BFD9"),  # Lune d'Uranus
    Moon("Oberon", 1, planets_full[6], 0.03, 10, diameter_km=1523, color="#708090"),  # Lune d'Uranus
    # Lunes de Neptune
    Moon("Triton", 1, planets_full[7], 0.007, 15, diameter_km=2706, color="#7FFFD4"),  # Lune de Neptune
    Moon("Nereid", 1, planets_full[7], 0.032, 7, diameter_km=340, color="#4B6D60"),  # Lune de Neptune
]


planets_with_moons_full = [
    planets_full[2],  # Terre
    planets_full[3],  # Mars
    planets_full[4],  # Jupiter
    planets_full[5],  # Saturne
    planets_full[6],  # Uranus
    planets_full[7]   # Neptune
]


planets_small = [
    Planet("Mercure", 3, sun, 0.39, 0.205, 0.24, diameter_km=4879, color='#B4B4B4'),
    Planet("Vénus", 6, sun, 0.72, 0.007, 0.62, diameter_km=12104, color='#D5C79E'),
    Planet("Terre", 6, sun, 1.0, 0.017, 1.0, diameter_km=12742, color='#1E90FF'),
    Planet("Mars", 4, sun, 1.52, 0.093, 1.88, diameter_km=6779, color='#FF4500')
]

moons_small = [
    Moon("Lune", 2, planets_small[2], 0.05, 12, diameter_km=3474, color="#D3D3D3"),
    Moon("Phobos", 1, planets_small[3], 0.01, 8, diameter_km=22, color="#6D6D6D"),
    Moon("Deimos", 1, planets_small[3], 0.02, 16, diameter_km=12, color="#A8A8A8")
]

planets_with_moons_small = [
    planets_small[2],
    planets_small[3]
]






planets,moons,planets_with_moons = planets_full,moons_full,planets_with_moons_full

planets,moons,planets_with_moons = planets_small,moons_small,planets_with_moons_small

# Calcul des paramètres d'affichage
max_distance = max(planet.semi_major_axis for planet in planets)
scale_factor = max(planet.diameter_km for planet in planets) / 10
max_orbit_radius = max_distance * 1.2

# Configuration de la figure
fig, ax = plt.subplots(figsize=(6, 6))
fig.patch.set_facecolor('black')
ax.set_facecolor('black')
ax.set_xlim(-max_orbit_radius, max_orbit_radius)
ax.set_ylim(-max_orbit_radius, max_orbit_radius)
ax.set_aspect('equal')
ax.set_xticks([])
ax.set_yticks([])
ax.set_title("Système Solaire (simplifié)", color='white')

# Ajout du Soleil
ax.plot(0, 0, 'o', markersize=sun.get_scaled_size(scale_factor, star_reduction_factor=25), label=sun.name, color=sun.color)

# Ajout des planètes et de leurs orbites
planet_plots = {}
moon_plots = {}
for planet in planets:
    x, y = get_orbit(planet.semi_major_axis, planet.eccentricity)
    orbit_color = mcolors.to_rgba(planet.color, alpha=0.3)
    ax.plot(x, y, '--', alpha=0.5, color=orbit_color)
    planet_plots[planet.name], = ax.plot([], [], 'o', label=planet.name, markersize=planet.get_scaled_size(scale_factor), color=planet.color)

# Ajout des lunes
for moon in moons:
    moon_plots[moon.name], = ax.plot([], [], 'o', color=moon.color, markersize=moon.get_scaled_size(scale_factor), label=moon.name)

# Légende
ax.legend(loc='upper left', bbox_to_anchor=(1, 1), facecolor='white', edgecolor='white', frameon=True, labelspacing=1.2, fontsize='large')

# Animation
ani = animation.FuncAnimation(fig, update, fargs=(planets, moons, planet_plots, moon_plots, planets_with_moons), interval=50)
plt.show()
