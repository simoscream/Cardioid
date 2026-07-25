import math
import unittest
from src.math_engine import (
    get_point_angle,
    get_point_coordinates,
    compute_destination_index,
    generate_all_points,
    generate_chords
)

class TestMathEngine(unittest.TestCase):
    """Tests unitaires pour le moteur mathématique (arithmétique modulaire et géométrie)."""

    def test_get_point_angle(self):
        modulo = 100
        # Le point 0 est situé en haut : -π/2 radians
        self.assertAlmostEqual(get_point_angle(0, modulo), -math.pi / 2.0)
        # Le point à un quart de tour (25) est à droite : 0 radians
        self.assertAlmostEqual(get_point_angle(25, modulo), 0.0)
        # Le point au demi tour (50) est en bas : π/2 radians
        self.assertAlmostEqual(get_point_angle(50, modulo), math.pi / 2.0)

    def test_invalid_modulo(self):
        with self.assertRaises(ValueError):
            get_point_angle(0, 0)
        with self.assertRaises(ValueError):
            compute_destination_index(1, 2, -10)

    def test_get_point_coordinates(self):
        center = (400.0, 400.0)
        radius = 100.0
        modulo = 4

        # Point 0 : haut (400, 300)
        x0, y0 = get_point_coordinates(0, modulo, center, radius)
        self.assertAlmostEqual(x0, 400.0)
        self.assertAlmostEqual(y0, 300.0)

        # Point 2 : bas (400, 500)
        x2, y2 = get_point_coordinates(2, modulo, center, radius)
        self.assertAlmostEqual(x2, 400.0)
        self.assertAlmostEqual(y2, 500.0)

    def test_compute_destination_index(self):
        table = 2
        modulo = 100
        # Point 0 -> 0
        self.assertEqual(compute_destination_index(0, table, modulo), 0)
        # Point 10 -> 20
        self.assertEqual(compute_destination_index(10, table, modulo), 20)
        # Point 60 -> (2 * 60) % 100 = 20
        self.assertEqual(compute_destination_index(60, table, modulo), 20)

    def test_floating_table(self):
        table = 2.5
        modulo = 100
        # Point 10 -> 25.0
        self.assertEqual(compute_destination_index(10, table, modulo), 25.0)

    def test_generate_all_points_count(self):
        points = generate_all_points(100, (400, 400), 300)
        self.assertEqual(len(points), 100)

    def test_generate_chords_count(self):
        chords = generate_chords(2, 100, (400, 400), 300)
        self.assertEqual(len(chords), 100)

if __name__ == "__main__":
    unittest.main()
