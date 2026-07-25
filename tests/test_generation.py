import os
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path
from PIL import Image
from src.config import RenderConfig, StyleConfig
from src.renderers.png_renderer import PNGRenderer
from src.renderers.svg_renderer import SVGRenderer

class TestGeneration(unittest.TestCase):
    """Tests d'intégration pour les moteurs de rendu PNG et SVG."""

    def setUp(self):
        self.output_dir = Path("output/images/test_output")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def test_png_generation(self):
        config = RenderConfig(table=2.0, modulo=50, width=400, height=400)
        renderer = PNGRenderer(config)
        out_path = self.output_dir / "test_table2_m50.png"
        saved = renderer.render(out_path)

        self.assertTrue(saved.exists())
        self.assertGreater(saved.stat().st_size, 0)
        img = Image.open(saved)
        self.assertEqual(img.size, (400, 400))

    def test_svg_generation(self):
        config = RenderConfig(table=3.0, modulo=60, width=500, height=500)
        renderer = SVGRenderer(config)
        out_path = self.output_dir / "test_table3_m60.svg"
        saved = renderer.render(out_path)

        self.assertTrue(saved.exists())
        self.assertGreater(saved.stat().st_size, 0)
        # Vérification XML valide
        tree = ET.parse(saved)
        root = tree.getroot()
        self.assertTrue(root.tag.endswith("svg"))
        self.assertEqual(root.attrib["width"], "500")
        self.assertEqual(root.attrib["height"], "500")

    def tearDown(self):
        # Nettoyage des fichiers temporaires de test
        for f in self.output_dir.glob("*"):
            f.unlink()
        if self.output_dir.exists():
            self.output_dir.rmdir()

if __name__ == "__main__":
    unittest.main()
