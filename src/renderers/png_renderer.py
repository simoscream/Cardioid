from pathlib import Path
from typing import Union
from PIL import Image, ImageDraw, ImageFont
from src.config import RenderConfig
from src.renderers.base import BaseRenderer
from src.math_engine import generate_all_points, generate_chords

class PNGRenderer(BaseRenderer):
    """Moteur de rendu d'image matricielle PNG avec Pillow."""

    def render(self, output_path: Union[str, Path]) -> Path:
        out_path = Path(output_path)
        out_path.parent.mkdir(parents=True, exist_ok=True)

        cfg = self.config
        style = cfg.style

        # Image principale avec canal Alpha pour l'anticrénelage et les transparences
        img = Image.new("RGBA", (cfg.width, cfg.height), style.background_color + (255,))
        draw_layer = Image.new("RGBA", (cfg.width, cfg.height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(draw_layer)

        cx, cy = cfg.center
        r = cfg.circle_radius

        # 1. Tracé du cercle englobant
        if style.show_circle:
            bbox = [cx - r, cy - r, cx + r, cy + r]
            draw.ellipse(bbox, outline=style.circle_color, width=1)

        # 2. Tracé des cordes (multiplicateur x modulo)
        chords = generate_chords(cfg.table, cfg.modulo, cfg.center, r)
        for (x1, y1), (x2, y2) in chords:
            draw.line([(x1, y1), (x2, y2)], fill=style.line_color, width=int(style.line_width))

        # 3. Tracé des points sur le cercle
        points = generate_all_points(cfg.modulo, cfg.center, r)
        if style.show_points:
            pt_r = style.point_radius
            for px, py in points:
                draw.ellipse([px - pt_r, py - pt_r, px + pt_r, py + pt_r], fill=style.point_color)

        # 4. Tracé des numéros des points (tous les label_step points)
        font = ImageFont.load_default()
        if style.show_labels:
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
                draw.text((tx, ty), str(i), fill=style.text_color, font=font, anchor="mm")

        # 5. Incrustation du titre d'identification en bas (droite par défaut ou gauche)
        if style.show_title:
            title_str = cfg.formatted_title
            margin = 20.0
            y_pos = cfg.height - margin

            if style.title_position.lower() == "left":
                x_pos = margin
                anchor_mode = "ld"  # left-down
            else:
                x_pos = cfg.width - margin
                anchor_mode = "rd"  # right-down

            draw.text((x_pos, y_pos), title_str, fill=style.text_color, font=font, anchor=anchor_mode)

        # Fusion des calques
        final_img = Image.alpha_composite(img, draw_layer)
        final_img.convert("RGB").save(out_path, "PNG")
        return out_path
