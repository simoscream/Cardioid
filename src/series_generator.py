from pathlib import Path
from typing import Union, List, Optional
from src.config import RenderConfig, StyleConfig
from src.renderers.png_renderer import PNGRenderer

def get_default_series_dir(start_table: float, end_table: float, modulo: int, style: Optional[StyleConfig] = None) -> Path:
    """Génère un nom de dossier explicite pour la série (ex: frames_table_2.0_to_10.0_modulo_200_labelstep_5)."""
    start_str = f"{int(start_table)}" if start_table.is_integer() else f"{start_table}"
    end_str = f"{int(end_table)}" if end_table.is_integer() else f"{end_table}"
    parts = [f"frames_table_{start_str}_to_{end_str}", f"modulo_{modulo}"]

    if style and style.show_labels:
        parts.append(f"labelstep_{style.label_step}")

    dir_name = "_".join(parts)
    return Path("output/frames") / dir_name

class SeriesGenerator:
    """Générateur de séquences d'images PNG structurées avec nom de frame explicite (table et modulo)."""

    def __init__(self, modulo: int = 200, start_table: float = 2.0, end_table: float = 10.0, step: float = 0.05, style: Optional[StyleConfig] = None):
        self.modulo = modulo
        self.start_table = start_table
        self.end_table = end_table
        self.step = step
        self.style = style if style else StyleConfig()

    def generate(self, output_dir: Optional[Union[str, Path]] = None) -> Path:
        """Génère la série d'images PNG et retourne le chemin du dossier les contenant."""
        if output_dir:
            out_dir = Path(output_dir)
        else:
            out_dir = get_default_series_dir(self.start_table, self.end_table, self.modulo, self.style)

        out_dir.mkdir(parents=True, exist_ok=True)

        generated_files = []
        current_table = self.start_table
        frame_idx = 1

        total_frames = int(round((self.end_table - self.start_table) / self.step)) + 1
        print(f"🎬 Début de la génération de la série : {total_frames} images dans '{out_dir}'...")

        while current_table <= self.end_table + 1e-9:
            config = RenderConfig(
                table=round(current_table, 4),
                modulo=self.modulo,
                style=self.style
            )
            renderer = PNGRenderer(config)
            
            t_str = f"{int(current_table)}" if current_table.is_integer() else f"{current_table:.2f}"
            frame_filename = out_dir / f"frame_{frame_idx:04d}_t{t_str}_m{self.modulo}.png"
            saved_path = renderer.render(frame_filename)
            generated_files.append(saved_path)

            if frame_idx % 20 == 0 or frame_idx == total_frames:
                print(f"  [Frame {frame_idx}/{total_frames}] {saved_path.name}")

            current_table += self.step
            frame_idx += 1

        print(f"✅ Série terminée ! {len(generated_files)} images enregistrées dans {out_dir.resolve()}")
        return out_dir
