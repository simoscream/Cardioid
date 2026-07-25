import math
from typing import List, Tuple

def get_point_angle(index: float, modulo: int) -> float:
    """
    Calcule l'angle en radians d'un point sur le cercle.
    Le point 0 est situé en haut (-π/2).
    """
    if modulo <= 0:
        raise ValueError("Le modulo doit être un entier strictement positif.")
    return -math.pi / 2.0 + (2.0 * math.pi * index) / modulo

def get_point_coordinates(index: float, modulo: int, center: Tuple[float, float], radius: float) -> Tuple[float, float]:
    """
    Calcule les coordonnées cartésiennes (x, y) d'un point d'indice (entier ou flottant) sur le cercle.
    """
    angle = get_point_angle(index, modulo)
    cx, cy = center
    x = cx + radius * math.cos(angle)
    y = cy + radius * math.sin(angle)
    return (x, y)

def compute_destination_index(index: float, table: float, modulo: int) -> float:
    """
    Calcule l'indice de destination pour la table de multiplication courante modulo m.
    Exemple: i=3, n=2, m=10 -> (2 * 3) % 10 = 6
    """
    if modulo <= 0:
        raise ValueError("Le modulo doit être un entier strictement positif.")
    return (table * index) % modulo

def generate_all_points(modulo: int, center: Tuple[float, float], radius: float) -> List[Tuple[float, float]]:
    """
    Génère la liste des coordonnées (x, y) de tous les points régulièrement espacés de 0 à modulo - 1.
    """
    return [get_point_coordinates(i, modulo, center, radius) for i in range(modulo)]

def generate_chords(table: float, modulo: int, center: Tuple[float, float], radius: float) -> List[Tuple[Tuple[float, float], Tuple[float, float]]]:
    """
    Génère la liste des cordes sous la forme d'une paire de coordonnées :
    [((x_départ, y_départ), (x_arrivée, y_arrivée)), ...]
    """
    chords = []
    for i in range(modulo):
        start_pt = get_point_coordinates(i, modulo, center, radius)
        dest_idx = compute_destination_index(i, table, modulo)
        end_pt = get_point_coordinates(dest_idx, modulo, center, radius)
        chords.append((start_pt, end_pt))
    return chords
