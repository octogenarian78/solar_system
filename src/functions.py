"""
@file functions.py
@brief Fonctions utilitaires pour les calculs d'orbites et mises à jour d'animation.

Ce fichier contient des fonctions pour calculer les orbites elliptiques des planètes
et mettre à jour leurs positions dans l'animation.

@author Pierre JAUFFRES
@date 2025-02-22
"""

import numpy as np

def get_orbit(a, e, num_points=200):
    """
    @brief Calcule les coordonnées d'une orbite elliptique.


    Cette fonction calcule les coordonnées x et y d'une orbite elliptique en fonction du demi-grand axe et de l'excentricité.

    @param a: Demi-grand axe de l'orbite.
    @param e: Excentricité de l'orbite.
    @param num_points: Nombre de points pour tracer l'orbite (par défaut 200).

    @return: Coordonnées x et y de l'orbite.
    """
    theta = np.linspace(0, 2*np.pi, num_points)
    r = (a * (1 - e**2)) / (1 + e * np.cos(theta))
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    return x, y
def update(frame, planets, moons, planet_plots, moon_plots, planets_with_moons):
    """
    @brief Met à jour la position des planètes et de la lune à chaque frame.


    Cette fonction calcule les nouvelles positions des planètes et de la lune et les met à jour dans l'animation.

    @param frame: Index de l'animation.
    @param planets: Liste des objets Planet.
    @param moon: L'objet Moon.
    @param planet_plots: Dictionnaire des objets graphiques des planètes.
    @param moon_plot: Objet graphique de la lune.
    @param planets_with_moons: liste des planetes avec une lune

    @return: Liste des éléments graphiques mis à jour.
    """
    t = frame * 0.02

    for planet in planets:
        theta = t / planet.period
        r = (planet.semi_major_axis * (1 - planet.eccentricity**2)) / (1 + planet.eccentricity * np.cos(theta))
        x = r * np.cos(theta)
        y = r * np.sin(theta)
        planet_plots[planet.name].set_data(x, y)
        if planet in planets_with_moons:
            for moon in moons:
                if planet != moon.planet:
                    pass
                else:
                    moon_x = x + moon.orbit_radius * np.cos(moon.orbit_speed * t)
                    moon_y = y + moon.orbit_radius * np.sin(moon.orbit_speed * t)
                    moon_plots[moon.name].set_data(moon_x, moon_y)

    return list(planet_plots.values()) + list(moon_plots.values())
