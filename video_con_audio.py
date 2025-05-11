from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip
import os

# Rutas absolutas
BASE_DIR = "/Users/pablostiefel/Documents/QuizFutbolYouTube"
INPUT_VIDEO = os.path.join(BASE_DIR, "output/video_final.mp4")
MUSIC_FILE = os.path.join(BASE_DIR, "musica_fondo.mp3")
OUTPUT_VIDEO = os.path.join(BASE_DIR, "output/video_final_con_audio.mp4")

def add_audio_to_video():
    print("Cargando video y audio...")
    # Cargar video
    video = VideoFileClip(INPUT_VIDEO)
    
    # Cargar música de fondo
    music = AudioFileClip(MUSIC_FILE)
    
    # Ajustar duración de la música al video
    if music.duration > video.duration:
        music = music.subclip(0, video.duration)
    
    # Combinar audio
    final_audio = CompositeAudioClip([music.set_duration(video.duration)])
    video = video.set_audio(final_audio)
    
    # Guardar video con audio
    print("Generando video con audio...")
    video.write_videofile(
        OUTPUT_VIDEO,
        codec="libx264",
        audio_codec="aac",
        ffmpeg_params=["-pix_fmt", "yuv420p"],
        verbose=True
    )
    video.close()
    music.close()
    print(f"Video generado en: {OUTPUT_VIDEO}")

if __name__ == "__main__":
    add_audio_to_video()