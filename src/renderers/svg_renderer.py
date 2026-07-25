from pathlib import Path
from typing import Union, Tuple
from src.config import RenderConfig
from src.renderers.base import BaseRenderer
from src.math_engine import generate_all_points, generate_chords

def rgba_to_svg(color: Tuple[int, ...]) -> str:
    """Convertit un tuple (r, g, b) ou (r, g, b, a) en chaîne CSS pour SVG."""
    if len(color) == 3:
        return f"rgb({color[0]}, {color[1]}, {color[2]})"
    elif len(color) == 4:
        alpha = round(color[3] / 255.0, 3)
        return f"rgba({color[0]}, {color[1]}, {color[2]}, {alpha})"
    raise ValueError(f"Format de couleur invalide : {color}")

class SVGRenderer(BaseRenderer):
    """Moteur de rendu d'image vectorielle au format SVG."""

    def render(self, output_path: Union[str, Path]) -> Path:
        out_path = Path(output_path)
        out_path.parent.mkdir(parents=True, exist_ok=True)

        cfg = self.config
        style = cfg.style

        cx, cy = cfg.center
        r = cfg.circle_radius

        svg_lines = [
            '<?xml version="1.0" encoding="UTF-8" standalone="no"?>',
            f'<svg width="{cfg.width}" height="{cfg.height}" viewBox="0 0 {cfg.width} {cfg.height}" xmlns="http://www.w3.org/2000/svg">',
            f'  <!-- Fond -->',
            f'  <rect width="100%" height="100%" fill="{rgba_to_svg(style.background_color)}" />'
        ]

        # 1. Cercle principal
        if style.show_circle:
            svg_lines.append(f'  <!-- Cercle principal -->')
            svg_lines.append(
                f'  <circle cx="{cx:.2f}" cy="{cy:.2f}" r="{r:.2f}" '
                f'stroke="{rgba_to_svg(style.circle_color)}" fill="none" stroke-width="1" />'
            )

        # 2. Cordes
        svg_lines.append(f'  <!-- Cordes modulaires -->')
        svg_lines.append(f'  <g stroke="{rgba_to_svg(style.line_color)}" stroke-width="{style.line_width}" stroke-linecap="round">')
        chords = generate_chords(cfg.table, cfg.modulo, cfg.center, r)
        for (x1, y1), (x2, y2) in chords:
            svg_lines.append(f'    <line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" />')
        svg_lines.append(f'  </g>')

        # 3. Points sur le cercle
        points = generate_all_points(cfg.modulo, cfg.center, r)
        if style.show_points:
            svg_lines.append(f'  <!-- Points -->')
            svg_lines.append(f'  <g fill="{rgba_to_svg(style.point_color)}">')
            for px, py in points:
                svg_lines.append(f'    <circle cx="{px:.2f}" cy="{py:.2f}" r="{style.point_radius:.2f}" />')
            svg_lines.append(f'  </g>')

        # 4. Étiquettes / Numéros des points (tous les label_step points)
        if style.show_labels:
            svg_lines.append(f'  <!-- Numéros des points -->')
            svg_lines.append(f'  <g fill="{rgba_to_svg(style.text_color)}" font-family="sans-serif" font-size="12" text-anchor="middle" dominant-baseline="central">')
            label_offset = 15.0
            step = max(1, style.label_step)
            for i, (px, py) in enumerate(points):
                if i % step != 0:
                    continue
                dx = px - cx
                dy = py - cy
                dist = (dx**2 + dy**2)**0.5
                if dist > 0:
                    tx = px + (dx / dist) * label_offset
                    ty = py + (dy / dist) * label_offset
                else:
                    tx, ty = px, py
                svg_lines.append(f'    <text x="{tx:.2f}" y="{ty:.2f}">{i}</text>')
            svg_lines.append(f'  </g>')

        # 5. Titre en bas (droite ou gauche)
        if style.show_title:
            margin = 20.0
            y_pos = cfg.height - margin
            if style.title_position.lower() == "left":
                x_pos = margin
                anchor = "start"
            else:
                x_pos = cfg.width - margin
                anchor = "end"

            svg_lines.append(f'  <!-- Titre d\'identification -->')
            svg_lines.append(
                f'  <text x="{x_pos:.2f}" y="{y_pos:.2f}" fill="{rgba_to_svg(style.text_color)}" '
                f'font-family="sans-serif" font-size="14" font-weight="bold" text-anchor="{anchor}">{cfg.formatted_title}</text>'
            )

        svg_lines.append('</svg>')

        out_path.write_text('\n'.join(svg_lines), encoding='utf-8')
        return out_path
