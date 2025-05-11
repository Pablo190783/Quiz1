import os
import sys
import logging
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip, concatenate_audioclips

# Configurar logging
logging.basicConfig(
    filename="/Users/pablostiefel/Documents/QuizFutbolYouTube/agregar_audio.log",
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Rutas absolutas
BASE_DIR = "/Users/pablostiefel/Documents/QuizFutbolYouTube"
OUTPUT_BASE = os.path.join(BASE_DIR, "output")
MUSIC_PATH = os.path.join(BASE_DIR, "musica_fondo.mp3")
INTRO_AUDIO_PATH = os.path.join(BASE_DIR, "bienvenida.mp3")
OUTRO_AUDIO_PATH = os.path.join(BASE_DIR, "suscribite_audio.mp3")

def agregar_audio_completo(video_index):
    # Definir rutas
    input_video = os.path.join(OUTPUT_BASE, f"video{video_index}", f"video_completo_sin_audio_{video_index}.mp4")
    output_video = os.path.join(OUTPUT_BASE, f"video{video_index}", f"video_completo_{video_index}.mp4")
    output_folder = os.path.join(OUTPUT_BASE, f"video{video_index}")

    # Validar existencia de archivos
    for path in [input_video, MUSIC_PATH, INTRO_AUDIO_PATH, OUTRO_AUDIO_PATH]:
        if not os.path.exists(path):
            error_msg = f"Archivo no encontrado: {path}"
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

    # Cargar video
    print(f"Cargando video: {input_video}", flush=True)
    logging.info(f"Cargando video: {input_video}")
    try:
        video_clip = VideoFileClip(input_video)
        video_duration = video_clip.duration
        print(f"Duración del video {video_index}: {video_duration:.2f} segundos", flush=True)
        logging.info(f"Duración del video {video_index}: {video_duration:.2f} segundos")
    except Exception as e:
        error_msg = f"Error cargando video {input_video}: {e}"
        print(error_msg, flush=True)
        logging.error(error_msg)
        raise

    # Cargar audios
    print(f"Cargando música de fondo: {MUSIC_PATH}", flush=True)
    logging.info(f"Cargando música de fondo: {MUSIC_PATH}")
    try:
        music_clip = AudioFileClip(MUSIC_PATH)
        music_duration = music_clip.duration
        print(f"Duración de musica_fondo.mp3: {music_duration:.2f} segundos", flush=True)
        logging.info(f"Duración de musica_fondo.mp3: {music_duration:.2f} segundos")
        # Reducir el volumen de la música de fondo al 20%
        music_clip = music_clip.volumex(0.07)
    except Exception as e:
        error_msg = f"Error cargando música {MUSIC_PATH}: {e}"
        print(error_msg, flush=True)
        logging.error(error_msg)
        raise

    print(f"Cargando audio de intro: {INTRO_AUDIO_PATH}", flush=True)
    logging.info(f"Cargando audio de intro: {INTRO_AUDIO_PATH}")
    try:
        intro_audio = AudioFileClip(INTRO_AUDIO_PATH)
    except Exception as e:
        error_msg = f"Error cargando audio de intro {INTRO_AUDIO_PATH}: {e}"
        print(error_msg, flush=True)
        logging.error(error_msg)
        raise

    print(f"Cargando audio de suscripción: {OUTRO_AUDIO_PATH}", flush=True)
    logging.info(f"Cargando audio de suscripción: {OUTRO_AUDIO_PATH}")
    try:
        outro_audio = AudioFileClip(OUTRO_AUDIO_PATH)
        outro_duration = outro_audio.duration
        print(f"Duración de suscribite_audio.mp3: {outro_duration:.2f} segundos", flush=True)
        logging.info(f"Duración de suscribite_audio.mp3: {outro_duration:.2f} segundos")
    except Exception as e:
        error_msg = f"Error cargando audio de suscripción {OUTRO_AUDIO_PATH}: {e}"
        print(error_msg, flush=True)
        logging.error(error_msg)
        raise

    # Ajustar música de fondo
    if music_duration < video_duration:
        print(f"Repitiendo música para cubrir {video_duration:.2f} segundos", flush=True)
        logging.info(f"Repitiendo música para cubrir {video_duration:.2f} segundos")
        repetitions = int(video_duration / music_duration) + 1
        music_clip = concatenate_audioclips([music_clip] * repetitions).subclip(0, video_duration)

    # Combinar audios
    print("Combinando audios...", flush=True)
    logging.info("Combinando audios")
    try:
        final_audio = CompositeAudioClip([intro_audio, music_clip, outro_audio.set_start(video_duration - outro_duration)])
    except Exception as e:
        error_msg = f"Error combinando audios: {e}"
        print(error_msg, flush=True)
        logging.error(error_msg)
        raise

    # Asignar audio al video
    print("Asignando audio al video...", flush=True)
    logging.info("Asignando audio al video")
    try:
        final_video = video_clip.set_audio(final_audio)
    except Exception as e:
        error_msg = f"Error asignando audio al video: {e}"
        print(error_msg, flush=True)
        logging.error(error_msg)
        raise

    # Guardar video
    print(f"Guardando video: {output_video}", flush=True)
    logging.info(f"Guardando video: {output_video}")
    try:
        final_video.write_videofile(
            output_video,
            fps=24,
            codec="libx264",
            audio_codec="aac",
            ffmpeg_params=["-pix_fmt", "yuv420p"],
            verbose=True,
            logger='bar'
        )
    except Exception as e:
        error_msg = f"Error escribiendo video {output_video}: {e}"
        print(error_msg, flush=True)
        logging.error(error_msg)
        raise

    # Cerrar clips
    print("Cerrando clips...", flush=True)
    logging.info("Cerrando clips")
    video_clip.close()
    music_clip.close()
    intro_audio.close()
    outro_audio.close()
    final_audio.close()
    final_video.close()

    print(f"Video generado en: {output_video}", flush=True)
    logging.info(f"Video generado en: {output_video}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        error_msg = "Uso: python agregar_audio_completo.py <video_index>"
        print(error_msg, flush=True)
        logging.error(error_msg)
        sys.exit(1)
    
    try:
        video_index = int(sys.argv[1])
        print(f"Iniciando agregar audio para video {video_index}", flush=True)
        logging.info(f"Iniciando agregar audio para video {video_index}")
        agregar_audio_completo(video_index)
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