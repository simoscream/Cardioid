import argparse
from pathlib import Path
from src.config import RenderConfig, StyleConfig
from src.renderers.png_renderer import PNGRenderer
from src.renderers.svg_renderer import SVGRenderer
from src.series_generator import SeriesGenerator, get_default_series_dir
from src.video_exporter import VideoExporter, get_default_video_path

def get_default_image_path(table: float, modulo: int, fmt: str, style: StyleConfig) -> Path:
    """Génère un nom de fichier image strictement explicite et représentatif des paramètres."""
    t_str = f"{int(table)}" if table.is_integer() else f"{table}"
    name_parts = [f"image_table_{t_str}", f"modulo_{modulo}"]
    if style.show_labels:
        name_parts.append(f"labelstep_{style.label_step}")
    if not style.show_circle:
        name_parts.append("nocircle")
    if not style.show_points:
        name_parts.append("nopoints")

    filename = "_".join(name_parts) + f".{fmt.lower()}"
    return Path("output/images") / filename

def main():
    parser = argparse.ArgumentParser(
        description="Générateur de figures géométriques basées sur les tables de multiplication modulaires."
    )
    # Options pour génération unitaire
    parser.add_argument("-t", "--table", type=float, default=2.0, help="Table de multiplication / multiplicateur (ex: 2)")
    parser.add_argument("-m", "--modulo", type=int, default=100, help="Modulo / nombre de points sur le cercle (ex: 100)")
    parser.add_argument("-o", "--output", type=str, default=None, help="Chemin personnalisé du fichier ou dossier de sortie")
    parser.add_argument("-f", "--format", type=str, choices=["png", "svg"], default="png", help="Format d'image unitaire (png ou svg)")

    # Options de style & Titre
    parser.add_argument("--width", type=int, default=800, help="Largeur de l'image en pixels")
    parser.add_argument("--height", type=int, default=800, help="Hauteur de l'image en pixels")
    parser.add_argument("--show-labels", action="store_true", help="Afficher la numérotation des points sur le cercle")
    parser.add_argument("--label-step", type=int, default=5, help="Afficher les numéros tous les N points (par défaut: 5)")
    parser.add_argument("--hide-title", action="store_true", help="Masquer le titre d'identification en bas de l'image")
    parser.add_argument("--title-position", type=str, choices=["right", "left"], default="right", help="Position du titre en bas ('right' par défaut ou 'left')")
    parser.add_argument("--hide-circle", action="store_true", help="Masquer le cercle extérieur")
    parser.add_argument("--hide-points", action="store_true", help="Masquer les points sur le cercle")

    # Options pour série & vidéo
    parser.add_argument("--series", action="store_true", help="Générer une série d'images PNG dans un sous-dossier structuré")
    parser.add_argument("--video", action="store_true", help="Générer une vidéo MP4 complète avec FFmpeg")
    parser.add_argument("--start-table", type=float, default=2.0, help="Table de départ (ex: 2.0)")
    parser.add_argument("--end-table", type=float, default=10.0, help="Table de fin (ex: 10.0)")
    parser.add_argument("--step", type=float, default=0.05, help="Pas d'incrémentation (ex: 0.05)")
    parser.add_argument("--fps", type=int, default=30, help="Images par seconde (FPS) pour la vidéo MP4")

    args = parser.parse_args()

    style = StyleConfig(
        show_circle=not args.hide_circle,
        show_points=not args.hide_points,
        show_labels=args.show_labels,
        label_step=args.label_step,
        show_title=not args.hide_title,
        title_position=args.title_position
    )

    # 1. Mode Série / Vidéo
    if args.series or args.video:
        generator = SeriesGenerator(
            modulo=args.modulo,
            start_table=args.start_table,
            end_table=args.end_table,
            step=args.step,
            style=style
        )
        target_series_dir = Path(args.output) if (args.series and args.output and not args.video) else get_default_series_dir(args.start_table, args.end_table, args.modulo, style)
        frames_dir = generator.generate(target_series_dir)

        if args.video:
            target_video_path = Path(args.output) if args.output else get_default_video_path(args.start_table, args.end_table, args.modulo, style)
            exporter = VideoExporter(fps=args.fps)
            saved_video = exporter.create_video(frames_dir, target_video_path)
            print(f"🎉 Processus vidéo terminé : {saved_video.resolve()}")
        return

    # 2. Mode Image Unitaire (PNG / SVG)
    fmt = args.format.lower()
    if args.output:
        ext = Path(args.output).suffix.lower().lstrip('.')
        if ext in ["png", "svg"]:
            fmt = ext

    target_image_path = Path(args.output) if args.output else get_default_image_path(args.table, args.modulo, fmt, style)

    config = RenderConfig(
        table=args.table,
        modulo=args.modulo,
        width=args.width,
        height=args.height,
        style=style
    )

    renderer_cls = SVGRenderer if fmt == "svg" else PNGRenderer
    renderer = renderer_cls(config)
    saved_path = renderer.render(target_image_path)
    print(f" Image {fmt.upper()} générée avec succès : {saved_path.resolve()}")

if __name__ == "__main__":
    main()
