import os
import sys
import shutil
import traceback
import logging
from PIL import Image, ImageDraw
from moviepy.editor import ImageClip, CompositeVideoClip, ImageSequenceClip, concatenate_videoclips

# Configurar logging
logging.basicConfig(
    filename="/Users/pablostiefel/Documents/QuizFutbolYouTube/generar_video.log",
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Rutas absolutas
BASE_DIR = "/Users/pablostiefel/Documents/QuizFutbolYouTube"
OUTPUT_BASE = os.path.join(BASE_DIR, "output")
TEMP_BASE = os.path.join(BASE_DIR, "temp")
IMAGES_BASE = os.path.join(BASE_DIR, "images")

def generate_video(video_index):
    image_folder = os.path.join(IMAGES_BASE, f"video{video_index}")
    temp_folder = os.path.join(TEMP_BASE, f"video{video_index}")
    output_folder = os.path.join(OUTPUT_BASE, f"video{video_index}")
    output_video = os.path.join(output_folder, f"video_final_{video_index}.mp4")

    # Validar directorios
    for folder in [image_folder, temp_folder, output_folder]:
        if not os.path.exists(folder):
            os.makedirs(folder, exist_ok=True)
        if not os.access(folder, os.W_OK):
            error_msg = f"No se puede escribir en {folder}"
            print(error_msg, flush=True)
            logging.error(error_msg)
            raise PermissionError(error_msg)

    # Limpiar carpeta temporal
    if os.path.exists(temp_folder):
        shutil.rmtree(temp_folder)
    os.makedirs(temp_folder, exist_ok=True)

    # Generar frames para la barra animada
    fps = 24
    duration = 10
    total_frames = fps * duration  # 240 frames
    frame_paths = []

    print(f"Total frames esperados para video {video_index}: {total_frames}", flush=True)
    logging.info(f"Total frames esperados para video {video_index}: {total_frames}")

    for frame in range(total_frames):
        print(f"Iniciando frame {frame+1}/{total_frames} para video {video_index}", flush=True)
        logging.info(f"Iniciando frame {frame+1}/{total_frames} para video {video_index}")
        try:
            t = frame / fps
            width = max(1, int(960 * (1 - t / duration)))
            img = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            x0 = 480
            x1 = x0 + width
            print(f"Frame {frame}: t={t:.3f}, width={width}, x0={x0}, x1={x1}", flush=True)
            logging.info(f"Frame {frame}: t={t:.3f}, width={width}, x0={x0}, x1={x1}")
            if x0 >= x1:
                error_msg = f"Coordenadas inválidas: x0={x0}, x1={x1}"
                print(error_msg, flush=True)
                logging.error(error_msg)
                raise ValueError(error_msg)
            draw.rounded_rectangle((x0, 960, x1, 996), radius=5, fill=(0, 255, 0, 255))
            frame_path = os.path.join(temp_folder, f"frame_{frame:04d}.png")
            print(f"Guardando: {frame_path}", flush=True)
            logging.info(f"Guardando: {frame_path}")
            img.save(frame_path)
            # Verificar que el archivo existe y no está vacío
            if not os.path.exists(frame_path) or os.path.getsize(frame_path) == 0:
                error_msg = f"Archivo no creado o vacío: {frame_path}"
                print(error_msg, flush=True)
                logging.error(error_msg)
                raise IOError(error_msg)
            print(f"Guardado: {frame_path}", flush=True)
            logging.info(f"Guardado: {frame_path}")
            frame_paths.append(frame_path)
        except Exception as e:
            error_msg = f"Error en frame {frame}: {e}"
            print(error_msg, flush=True)
            logging.error(error_msg)
            traceback.print_exc(file=sys.stdout)
            raise

    print(f"Generados {len(frame_paths)} frames en {temp_folder}", flush=True)
    logging.info(f"Generados {len(frame_paths)} frames en {temp_folder}")

    # Validar que todos los frames existan
    missing_frames = [f for f in frame_paths if not os.path.exists(f) or os.path.getsize(f) == 0]
    if missing_frames:
        error_msg = f"Faltan frames o están vacíos: {missing_frames}"
        print(error_msg, flush=True)
        logging.error(error_msg)
        raise FileNotFoundError(error_msg)

    # Crear clip de la barra
    print(f"Creando timer_clip para video {video_index}...", flush=True)
    logging.info(f"Creando timer_clip para video {video_index}")
    try:
        timer_clip = ImageSequenceClip(frame_paths, fps=fps, load_images=True).set_duration(10)
    except Exception as e:
        error_msg = f"Error creando timer_clip: {e}"
        print(error_msg, flush=True)
        logging.error(error_msg)
        traceback.print_exc(file=sys.stdout)
        raise

    # Cargar diapositivas dinámicamente
    slides = [f for f in sorted(os.listdir(image_folder)) if f.startswith(f"quiz_futbol_video{video_index}_") and f.endswith(".png")]
    if len(slides) != 64:
        error_msg = f"Se esperaban 64 diapositivas, pero se encontraron {len(slides)} en {image_folder}"
        print(error_msg, flush=True)
        logging.error(error_msg)
        raise ValueError(error_msg)

    # Crear clips para cada diapositiva
    clips = []
    for i, slide in enumerate(slides):
        img_path = os.path.join(image_folder, slide)
        try:
            if i % 2 == 0:  # Pregunta
                clip = ImageClip(img_path).set_duration(10)
                # Crear una copia del timer_clip para esta pregunta
                final_clip = CompositeVideoClip([clip, timer_clip.set_duration(10)])
                clips.append(final_clip)
            else:  # Respuesta
                clip = ImageClip(img_path).set_duration(5)
                clips.append(clip)
        except Exception as e:
            error_msg = f"Error procesando diapositiva {slide}: {e}"
            print(error_msg, flush=True)
            logging.error(error_msg)
            traceback.print_exc(file=sys.stdout)
            raise

    # Concatenar clips
    print(f"Concatenando clips para video {video_index}...", flush=True)
    logging.info(f"Concatenando clips para video {video_index}")
    try:
        final_video = concatenate_videoclips(clips, method="compose")
    except Exception as e:
        error_msg = f"Error concatenando clips: {e}"
        print(error_msg, flush=True)
        logging.error(error_msg)
        traceback.print_exc(file=sys.stdout)
        raise

    # Guardar video
    print(f"Generando video en {output_video}...", flush=True)
    logging.info(f"Generando video en {output_video}")
    try:
        final_video.write_videofile(
            output_video,
            fps=24,
            codec="libx264",
            audio=False,  # Audio se agrega en agregar_audio_completo.py
            ffmpeg_params=["-pix_fmt", "yuv420p"],
            verbose=True,
            logger='bar'
        )
    except Exception as e:
        error_msg = f"Error escribiendo video {output_video}: {e}"
        print(error_msg, flush=True)
        logging.error(error_msg)
        traceback.print_exc(file=sys.stdout)
        raise

    # Limpieza (opcional, comentado para depuración)
    # final_video.close()
    # timer_clip.close()
    # shutil.rmtree(temp_folder, ignore_errors=True)
    print(f"Video generado en {output_video}", flush=True)
    logging.info(f"Video generado en {output_video}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        error_msg = "Uso: python generar_video.py <video_index>"
        print(error_msg, flush=True)
        logging.error(error_msg)
        sys.exit(1)
    
    try:
        video_index = int(sys.argv[1])
        print(f"Iniciando generación de video {video_index}", flush=True)
        logging.info(f"Iniciando generación de video {video_index}")
        generate_video(video_index)
    except ValueError as e:
        error_msg = f"Error: video_index debe ser un entero. Recibido: {sys.argv[1]}"
        print(error_msg, flush=True)
        logging.error(error_msg)
        sys.exit(1)
    except Exception as e:
        error_msg = f"Error inesperado: {e}"
        print(error_msg, flush=True)
        logging.error(error_msg)
        traceback.print_exc(file=sys.stdout)
        sys.exit(1)