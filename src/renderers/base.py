from abc import ABC, abstractmethod
from pathlib import Path
from typing import Union
from src.config import RenderConfig

class BaseRenderer(ABC):
    """Classe abstraite de base pour les moteurs de rendu."""
    
    def __init__(self, config: RenderConfig):
        self.config = config

    @abstractmethod
    def render(self, output_path: Union[str, Path]) -> Path:
        """Exécute le rendu et sauvegarde le fichier vers output_path."""
        pass
