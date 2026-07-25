import argparse
from pathlib import Path
from src.config import RenderConfig, StyleConfig
from src.renderers.png_renderer import PNGRenderer
from src.renderers.svg_renderer import SVGRenderer
from src.series_generator import SeriesGenerator, get_default_series_dir
from src.video_exporter import VideoExporter, get_default_video_path

def get_default_image_path(table: float, modulo: int, fmt: str, style: StyleConfig) -> Path:
    """Generate an explicit and parameter-rich output image filepath."""
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
        description="Geometric figure generator based on modular multiplication tables."
    )
    # Options for single rendering
    parser.add_argument("-t", "--table", type=float, default=2.0, help="Multiplication factor / Table (e.g. 2.0)")
    parser.add_argument("-m", "--modulo", type=int, default=100, help="Modulo / Number of points around the circle (e.g. 100)")
    parser.add_argument("-o", "--output", type=str, default=None, help="Custom output file or directory path")
    parser.add_argument("-f", "--format", type=str, choices=["png", "svg"], default="png", help="Output image format (png or svg)")

    # Style & Title Overlay Options
    parser.add_argument("--width", type=int, default=800, help="Image width in pixels")
    parser.add_argument("--height", type=int, default=800, help="Image height in pixels")
    parser.add_argument("--show-labels", action="store_true", help="Display point numbers around the circle")
    parser.add_argument("--label-step", type=int, default=5, help="Display number labels every N points (default: 5)")
    parser.add_argument("--hide-title", action="store_true", help="Hide identification title overlay at the bottom")
    parser.add_argument("--title-position", type=str, choices=["right", "left"], default="right", help="Title position at the bottom ('right' by default or 'left')")
    parser.add_argument("--hide-circle", action="store_true", help="Hide outer circle")
    parser.add_argument("--hide-points", action="store_true", help="Hide points around the circle")

    # Series & Video Options
    parser.add_argument("--series", action="store_true", help="Generate a frame series sequence of PNG images")
    parser.add_argument("--video", action="store_true", help="Compile a complete MP4 animation video using FFmpeg")
    parser.add_argument("--start-table", type=float, default=2.0, help="Start table for series/video (default: 2.0)")
    parser.add_argument("--end-table", type=float, default=10.0, help="End table for series/video (default: 10.0)")
    parser.add_argument("--step", type=float, default=0.1, help="Table increment step for series/video (default: 0.1)")
    parser.add_argument("--fps", type=int, default=30, help="Frame rate for MP4 video export (default: 30)")

    args = parser.parse_args()

    style = StyleConfig(
        show_labels=args.show_labels,
        label_step=args.label_step,
        show_title=not args.hide_title,
        title_position=args.title_position,
        show_circle=not args.hide_circle,
        show_points=not args.hide_points
    )

    if args.series or args.video:
        series_dir = Path(args.output) if (args.output and args.series and not args.video) else get_default_series_dir(args.start_table, args.end_table, args.modulo)
        generator = SeriesGenerator(series_dir)

        print(f"Generating series: Table {args.start_table} to {args.end_table} (step {args.step}), Modulo {args.modulo}...")
        frames = generator.generate_series(
            start_table=args.start_table,
            end_table=args.end_table,
            step=args.step,
            modulo=args.modulo,
            style=style
        )
        print(f"✅ Generated {len(frames)} frames in directory: {series_dir}")

        if args.video:
            video_path = Path(args.output) if args.output else get_default_video_path(args.start_table, args.end_table, args.modulo)
            exporter = VideoExporter()
            print(f"Compiling video: {video_path}...")
            exporter.export_video(series_dir, video_path, fps=args.fps)
            print(f"🎉 Video successfully exported: {video_path}")

    else:
        out_fmt = args.format.lower()
        if args.output:
            out_path = Path(args.output)
        else:
            out_path = get_default_image_path(args.table, args.modulo, out_fmt, style)

        config = RenderConfig(
            table=args.table,
            modulo=args.modulo,
            width=args.width,
            height=args.height,
            style=style
        )

        if out_fmt == "png":
            renderer = PNGRenderer(config)
            renderer.render(out_path)
        else:
            renderer = SVGRenderer(config)
            renderer.render(out_path)

        print(f"🎉 Generated single image ({out_fmt.upper()}): {out_path}")

if __name__ == "__main__":
    main()
