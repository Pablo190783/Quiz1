import os
import shutil
from PIL import Image, ImageDraw
import traceback

BASE_DIR = "/Users/pablostiefel/Documents/QuizFutbolYouTube"
TEMP_FOLDER = os.path.join(BASE_DIR, "temp")

# Generar frames para la barra animada
fps = 24
duration = 10
total_frames = fps * duration
# Limpiar carpeta /temp/ si existe
if os.path.exists(TEMP_FOLDER):
    shutil.rmtree(TEMP_FOLDER)
os.makedirs(TEMP_FOLDER, exist_ok=True)
for frame in range(total_frames):
    print(f"Iniciando frame {frame}")
    try:
        t = frame / fps
        width = max(1, int(960 * (1 - t / duration)))
        img = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        x0 = 960 - width / 2
        x1 = 960 + width / 2
        print(f"Frame {frame}: t={t:.3f}, width={width}, x0={x0}, x1={x1}")
        if x0 >= x1:
            raise ValueError(f"Coordenadas inválidas: x0={x0}, x1={x1}")
        print(f"Dibujando rectangle para frame {frame}")
        draw.rectangle((x0, 960, x1, 996), fill=(0, 255, 0, 255))
        frame_path = os.path.join(TEMP_FOLDER, f"frame_{frame:04d}.png")
        print(f"Guardando: {frame_path}")
        img.save(frame_path)
        print(f"Guardado: {frame_path}")
    except Exception as e:
        print(f"Error en frame {frame}: {e}")
        traceback.print_exc()
        raise
print(f"Generados {total_frames} frames en {TEMP_FOLDER}")