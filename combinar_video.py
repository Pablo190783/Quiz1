from moviepy.editor import VideoFileClip, CompositeVideoClip, concatenate_videoclips
import os

# Rutas absolutas
BASE_DIR = "/Users/pablostiefel/Documents/QuizFutbolYouTube"
DIAPOSITIVAS_DIR = os.path.join(BASE_DIR, "images")
BARRA_PATH = os.path.join(BASE_DIR, "output/barra.mp4")
OUTPUT_PATH = os.path.join(BASE_DIR, "output/video_final.mp4")

def combine_videos():
    print("Cargando barra...")
    barra = VideoFileClip(BARRA_PATH)
    
    print("Cargando diapositivas...")
    diapositivas = [VideoFileClip(os.path.join(DIAPOSITIVAS_DIR, f)) for f in sorted(os.listdir(DIAPOSITIVAS_DIR)) if f.endswith(".mp4")]
    
    print("Combinando videos...")
    clips = [CompositeVideoClip([diapo, barra.set_position(("center", "bottom"))]) for diapo in diapositivas]
    final_clip = concatenate_videoclips(clips)
    
    print("Generando video...")
    final_clip.write_videofile(
        OUTPUT_PATH,
        codec="libx264",
        audio_codec="aac",
        ffmpeg_params=["-pix_fmt", "yuv420p"],
        verbose=True
    )
    
    for clip in diapositivas + [barra, final_clip]:
        clip.close()
    print(f"Video generado en {OUTPUT_PATH}")

if __name__ == "__main__":
    combine_videos()