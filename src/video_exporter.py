import subprocess
from pathlib import Path
from typing import Union, Optional
from src.config import StyleConfig

def get_default_video_path(start_table: float, end_table: float, modulo: int, style: Optional[StyleConfig] = None) -> Path:
    """Génère un nom de fichier vidéo explicite (ex: video_table_2.0_to_10.0_modulo_200_labelstep_5.mp4)."""
    start_str = f"{int(start_table)}" if start_table.is_integer() else f"{start_table}"
    end_str = f"{int(end_table)}" if end_table.is_integer() else f"{end_table}"
    parts = [f"video_table_{start_str}_to_{end_str}", f"modulo_{modulo}"]

    if style and style.show_labels:
        parts.append(f"labelstep_{style.label_step}")

    filename = "_".join(parts) + ".mp4"
    return Path("output/videos") / filename

class VideoExporter:
    """Exporteur vidéo de séquences d'images PNG vers un fichier MP4 avec FFmpeg."""

    def __init__(self, fps: int = 30):
        self.fps = fps

    def create_video(self, frames_dir: Union[str, Path], output_mp4: Union[str, Path]) -> Path:
        f_dir = Path(frames_dir)
        out_mp4 = Path(output_mp4)
        out_mp4.parent.mkdir(parents=True, exist_ok=True)

        cmd = [
            "ffmpeg",
            "-y",                                      # Écraser le fichier de sortie s'il existe
            "-framerate", str(self.fps),               # Images par seconde
            "-pattern_type", "glob",
            "-i", str(f_dir / "*.png"),               # Utilisation de glob pour capter les frames avec table et modulo
            "-c:v", "libx264",                         # Codec H.264
            "-pix_fmt", "yuv420p",                     # Format universel
            str(out_mp4)
        ]

        print(f"🎥 Compilation vidéo MP4 avec FFmpeg ({self.fps} fps)...")
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            raise RuntimeError(f"Erreur FFmpeg lors de la création de la vidéo :\n{result.stderr}")

        print(f"🎬 Vidéo MP4 générée avec succès : {out_mp4.resolve()}")
        return out_mp4
