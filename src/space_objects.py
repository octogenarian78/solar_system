"""
@file space_objects.py
@brief Définitions des classes pour les objets célestes du système solaire.

Ce fichier contient les classes CelestialBody, Star, Planet et Moon,
qui permettent de modéliser les objets du système solaire.

@author Pierre JAUFFRES
@date 2025-02-22
"""

class CelestialBody:
    """
    @class CelestialBody
    @brief Classe de base pour les objets célestes.
    
    @param name Nom de l'objet céleste.
    @param size Taille de l'objet (utilisée pour la représentation graphique).
    @param diameter_km Diamètre réelle de l'objet (donnée en km)
    """
    def __init__(self, name, size, diameter_km=None):
        self.name = name
        self.size = size  # Taille pour l'affichage
        self.diameter_km = diameter_km  # Diamètre réel en kilomètres (facultatif)
    
    def get_scaled_size(self, scale_factor=1e9):
        """
        @brief Calcule la taille à afficher en fonction du diamètre réel et d'un facteur d'échelle.

        @param scale_factor: Facteur d'échelle pour redimensionner la taille (par défaut 1e9).
        @return: Taille redimensionnée pour l'affichage.
        """
        if self.diameter_km:
            return self.diameter_km / scale_factor  # Conversion en taille affichée
        return self.size

class Star(CelestialBody):
    """
    @class Star
    @brief Classe représentant une étoile.
    
    @param name Nom de l'étoile.
    @param size Taille de l'étoile.
    @param mass Masse de l'étoile en kilogrammes.
    @param diameter_km Diamètre réelle de l'étoile (donnée en km)
    @param color: Couleur de létoile pour l'affichage.
    """
    def __init__(self, name, size, mass, diameter_km,color="yellow"):
        super().__init__(name, size, diameter_km)
        self.mass = mass
        self.color = color
    
    def get_scaled_size(self, scale_factor=1e9, star_reduction_factor=50):
        """
        @brief Calcule la taille à afficher en fonction du diamètre réel et d'un facteur d'échelle.
        
        Applique un facteur de réduction spécifique pour les étoiles afin qu'elles soient plus petites.

        @param scale_factor: Facteur d'échelle pour redimensionner la taille (par défaut 1e9).
        @param star_reduction_factor: Facteur de réduction spécifique aux étoiles (par défaut 100).
        @return: Taille redimensionnée pour l'affichage.

        """
        if self.diameter_km:
            # Applique un facteur de réduction spécifique aux étoiles
            return self.diameter_km / (scale_factor * star_reduction_factor)  
        return self.size


class Planet(CelestialBody):
    """
    @class Planet
    @brief Classe représentant une planète.
    
    Hérite de la classe CelestialBody et ajoute des informations sur l'orbite autour d'une étoile.
    
    @param name: Nom de la planète.
    @param size: Taille de la planète.
    @param star: Étoile autour de laquelle la planète orbite.
    @param semi_major_axis: Demi-grand axe de l'orbite en Unités Astronomiques.
    @param eccentricity: Excentricité de l'orbite.
    @param period: Période orbitale en années terrestres.
    @param diameter_km Diamètre réelle de la planète (donnée en km)
    @param color: Couleur de la planète pour l'affichage.
    """
    def __init__(self, name, size, star, semi_major_axis, eccentricity, period, diameter_km, color):
        super().__init__(name, size)
        self.star = star
        self.semi_major_axis = semi_major_axis
        self.eccentricity = eccentricity
        self.period = period
        self.diameter_km = diameter_km  # Diamètre de la planète en km
        self.color = color  # Couleur de la planète pour l'affichage


class Moon(CelestialBody):
    """
    @class Moon
    @brief Classe représentant une lune.
    
    @param name Nom de la lune.
    @param size Taille de la lune.
    @param planet Planète autour de laquelle la lune orbite.
    @param orbit_radius Rayon de l'orbite en UA.
    @param orbit_speed Vitesse orbitale de la lune.
    @param diameter_km Diamètre réelle de la lune (donnée en km)
    @param color: Couleur de la lune pour l'affichage.
    """
    def __init__(self, name, size, planet, orbit_radius, orbit_speed, diameter_km,color="gray"):
        super().__init__(name, size, diameter_km)
        self.planet = planet
        self.orbit_radius = orbit_radius
        self.orbit_speed = orbit_speed
        self.color = color
