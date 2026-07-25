from dataclasses import dataclass, field
from typing import Tuple, Optional

@dataclass
class StyleConfig:
    """Configuration du style visuel de la figure."""
    background_color: Tuple[int, int, int] = (15, 23, 42)        # Bleu nuit sombre (Slate 900)
    circle_color: Tuple[int, int, int, int] = (255, 255, 255, 60)     # Cercle blanc semi-transparent
    line_color: Tuple[int, int, int, int] = (236, 72, 153, 160)       # Cordes rose vif (Pink 500) avec transparence
    point_color: Tuple[int, int, int, int] = (56, 189, 248, 255)      # Points bleu ciel (Sky 400)
    text_color: Tuple[int, int, int, int] = (241, 245, 249, 220)      # Numéros des points et titre
    line_width: float = 1.5
    point_radius: float = 3.0
    show_circle: bool = True
    show_points: bool = True
    show_labels: bool = False
    label_step: int = 5                                           # Afficher l'étiquette tous les N points (ex: 5)
    show_title: bool = True                                       # Afficher le titre d'identification (Table | Modulo)
    title_position: str = "right"                                 # Position du titre: 'right' (bas droite) ou 'left' (bas gauche)

@dataclass
class RenderConfig:
    """Configuration du rendu d'image."""
    table: float = 2.0
    modulo: int = 100
    width: int = 800
    height: int = 800
    margin: int = 60
    style: StyleConfig = field(default_factory=StyleConfig)

    @property
    def center(self) -> Tuple[float, float]:
        """Centre de l'image (cx, cy)."""
        return (self.width / 2.0, self.height / 2.0)

    @property
    def circle_radius(self) -> float:
        """Rayon du cercle inscrit en tenant compte des marges."""
        return (min(self.width, self.height) - 2 * self.margin) / 2.0

    @property
    def formatted_title(self) -> str:
        """Titre explicite par défaut."""
        t_str = f"{int(self.table)}" if self.table.is_integer() else f"{self.table:.2f}"
        return f"Table {t_str}  |  Modulo {self.modulo}"
