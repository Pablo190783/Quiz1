from PIL import Image, ImageDraw
import os
import shutil
from moviepy.editor import ImageSequenceClip

# Rutas absolutas
temp_folder = "/Users/pablostiefel/Documents/QuizFutbolYouTube/temp"
output_barra = "/Users/pablostiefel/Documents/QuizFutbolYouTube/output/barra.mp4"

# Limpiar el directorio temporal
if os.path.exists(temp_folder):
    shutil.rmtree(temp_folder)
os.makedirs(temp_folder)

def esquina_redonda(radio, relleno):
    """Dibuja una esquina redondeada"""
    corner = Image.new('RGBA', (radio, radio), (0, 0, 0, 0))
    draw = ImageDraw.Draw(corner)
    draw.pieslice((0, 0, radio * 2, radio * 2), 180, 270, fill=relleno)
    return corner

def dibujar_rectangulo_redondeado(draw, xy, radio, relleno):
    """Dibuja un rectángulo redondeado en el lienzo existente"""
    x0, y0, x1, y1 = xy
    ancho = x1 - x0
    alto = y1 - y0
    radio = min(radio, ancho // 2, alto // 2)
    
    if ancho <= 2 or alto <= 2 or radio < 1:
        draw.rectangle((x0, y0, x1 - 1, y1 - 1), fill=relleno)
        return
    
    esquina = esquina_redonda(radio, relleno)
    img = Image.new('RGBA', (ancho, alto), (0, 0, 0, 0))
    img_draw = ImageDraw.Draw(img)
    
    img_draw.rectangle((radio, 0, ancho - radio, alto), fill=relleno)
    img_draw.rectangle((0, radio, ancho, alto - radio), fill=relleno)
    
    img.paste(esquina, (0, 0))
    img.paste(esquina.rotate(90), (0, alto - radio))
    img.paste(esquina.rotate(180), (ancho - radio, alto - radio))
    img.paste(esquina.rotate(270), (ancho - radio, 0))
    
    draw._image.paste(img, (x0, y0), img)

# Generar imágenes para la barra animada
fps = 24
duration = 10
total_frames = fps * duration
canvas_width = 1050  # Ancho del lienzo más grande
canvas_height = 52   # Alto del lienzo más grande
max_width = 960      # Ancho máximo de la barra blanca y verde
bar_height = 36      # Alto de las barras
x_offset = 45        # Centrar barras: (1050 - 960) / 2
y_offset = 8         # Centrar barras: (52 - 36) / 2
widths = []
for frame in range(total_frames):
    t = frame / fps
    width = max(1, int(max_width * (1 - (t / duration) ** 1.5)))
    widths.append(width)
    img = Image.new("RGBA", (canvas_width, canvas_height), (255, 255, 255, 255))  # Lienzo blanco opaco
    draw = ImageDraw.Draw(img)
    # Dibujar lienzo blanco redondeado
    radius_white = min(12, canvas_width // 2, canvas_height // 2)
    dibujar_rectangulo_redondeado(draw, (0, 0, canvas_width, canvas_height), radius_white, (255, 255, 255))
    # Dibujar barra blanca redondeada
    draw.rounded_rectangle((x_offset, y_offset, x_offset + max_width, y_offset + bar_height), radius=radius_white, fill=(255, 255, 255))
    # Dibujar barra verde redondeada
    radius_green = min(12, width // 2, bar_height // 2, (width - 2) // 2)
    dibujar_rectangulo_redondeado(draw, (x_offset, y_offset, x_offset + width, y_offset + bar_height), radius_green, (0, 255, 0))
    img_path = os.path.join(temp_folder, f"frame_{frame:04d}.png")
    img.save(img_path, "PNG", optimize=True)
    if frame in [0, 60, 120, 180, 239]:
        shutil.copy(img_path, os.path.join(temp_folder, f"sample_frame_{frame:04d}.png"))

print(f"Total frames: {total_frames}, Widths range: {max(widths)} to {min(widths)}")

# Verificar imágenes generadas
frame_files = [os.path.join(temp_folder, f"frame_{i:04d}.png") for i in range(total_frames)]
for f in frame_files[:5] + frame_files[-5:]:
    if not os.path.exists(f):
        print(f"Error: {f} no existe")
        exit(1)

# Crear clip de la barra
barra_clip = ImageSequenceClip(frame_files, fps=fps).set_duration(10)

# Guardar el video de la barra con codec libx264
barra_clip.write_videofile(
    output_barra,
    fps=24,
    codec="libx264",
    ffmpeg_params=["-pix_fmt", "yuv420p"]
)