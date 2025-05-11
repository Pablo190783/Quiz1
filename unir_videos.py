import os
import sys
import logging
from moviepy.editor import VideoFileClip, concatenate_videoclips

# Configurar logging
logging.basicConfig(
    filename="/Users/pablostiefel/Documents/QuizFutbolYouTube/unir_videos.log",
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Rutas absolutas
BASE_DIR = "/Users/pablostiefel/Documents/QuizFutbolYouTube"
OUTPUT_BASE = os.path.join(BASE_DIR, "output")
INTRO_VIDEO = os.path.join(BASE_DIR, "intro_logo.mp4")
OUTRO_VIDEO = os.path.join(BASE_DIR, "suscribite.mp4")

def unir_videos(video_index):
    # Definir rutas
    input_video = os.path.join(OUTPUT_BASE, f"video{video_index}", f"video_final_{video_index}.mp4")
    output_video = os.path.join(OUTPUT_BASE, f"video{video_index}", f"video_completo_sin_audio_{video_index}.mp4")
    output_folder = os.path.join(OUTPUT_BASE, f"video{video_index}")

    # Validar existencia de archivos
    for video_path in [INTRO_VIDEO, input_video, OUTRO_VIDEO]:
        if not os.path.exists(video_path):
            error_msg = f"Archivo no encontrado: {video_path}"
            print(error_msg, flush=True)
            logging.error(error_msg)
            raise FileNotFoundError(error_msg)

    # Validar permisos de escritura
    if not os.path.exists(output_folder):
        os.makedirs(output_folder, exist_ok=True)
    if not os.access(output_folder, os.W_OK):
        error_msg = f"No se puede escribir en {output_folder}"
        print(error_msg, flush=True)
        logging.error(error_msg)
        raise PermissionError(error_msg)

    # Cargar clips
    print(f"Cargando videos para video {video_index}...", flush=True)
    logging.info(f"Cargando videos para video {video_index}")
    try:
        intro_clip = VideoFileClip(INTRO_VIDEO)
        main_clip = VideoFileClip(input_video)
        outro_clip = VideoFileClip(OUTRO_VIDEO)
    except Exception as e:
        error_msg = f"Error cargando videos: {e}"
        print(error_msg, flush=True)
        logging.error(error_msg)
        raise

    # Concatenar clips
    print(f"Concatenando videos para video {video_index}...", flush=True)
    logging.info(f"Concatenando videos para video {video_index}")
    try:
        final_clip = concatenate_videoclips([intro_clip, main_clip, outro_clip], method="compose")
    except Exception as e:
        error_msg = f"Error concatenando videos: {e}"
        print(error_msg, flush=True)
        logging.error(error_msg)
        raise

    # Guardar video
    print(f"Guardando video en {output_video}...", flush=True)
    logging.info(f"Guardando video en {output_video}")
    try:
        final_clip.write_videofile(
            output_video,
            fps=24,
            codec="libx264",
            audio=False,
            ffmpeg_params=["-pix_fmt", "yuv420p"],
            verbose=True,
            logger='bar'
        )
    except Exception as e:
        error_msg = f"Error escribiendo video {output_video}: {e}"
        print(error_msg, flush=True)
        logging.error(error_msg)
        raise
    finally:
        # Cerrar clips
        intro_clip.close()
        main_clip.close()
        outro_clip.close()
        final_clip.close()

    print(f"Video generado en: {output_video}", flush=True)
    logging.info(f"Video generado en: {output_video}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        error_msg = "Uso: python unir_videos.py <video_index>"
        print(error_msg, flush=True)
        logging.error(error_msg)
        sys.exit(1)
    
    try:
        video_index = int(sys.argv[1])
        print(f"Iniciando unión de videos para video {video_index}", flush=True)
        logging.info(f"Iniciando unión de videos para video {video_index}")
        unir_videos(video_index)
    except ValueError as e:
        error_msg = f"Error: video_index debe ser un entero. Recibido: {sys.argv[1]}"
        print(error_msg, flush=True)
        logging.error(error_msg)
        sys.exit(1)
    except Exception as e:
        error_msg = f"Error inesperado: {e}"
        print(error_msg, flush=True)
        logging.error(error_msg)
        sys.exit(1)