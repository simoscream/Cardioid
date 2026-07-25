import unittest
from pathlib import Path
from src.series_generator import SeriesGenerator, get_default_series_dir

class TestSeriesGenerator(unittest.TestCase):
    """Tests d'intégration pour le générateur de séries d'images."""

    def setUp(self):
        self.output_dir = Path("output/frames/test_series")

    def test_series_generation(self):
        generator = SeriesGenerator(modulo=50, start_table=2.0, end_table=2.2, step=0.1)
        out_dir = generator.generate(self.output_dir)

        # Doit générer 3 frames (2.0, 2.1, 2.2)
        frames = list(out_dir.glob("*.png"))
        self.assertEqual(len(frames), 3)
        for f in frames:
            self.assertTrue(f.exists())
            self.assertGreater(f.stat().st_size, 0)

    def test_default_naming(self):
        dir_path = get_default_series_dir(2.0, 10.0, 200)
        self.assertEqual(str(dir_path), "output/frames/frames_table_2_to_10_modulo_200")

    def tearDown(self):
        if self.output_dir.exists():
            for f in self.output_dir.glob("*"):
                f.unlink()
            self.output_dir.rmdir()

if __name__ == "__main__":
    unittest.main()
