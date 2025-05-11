import os
import shutil
import glob

# Rutas absolutas
BASE_DIR = "/Users/pablostiefel/Documents/QuizFutbolYouTube"
BACKUP_DIR = os.path.join(BASE_DIR, "backup")
SRC_DIR = os.path.join(BASE_DIR, "src")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
IMAGES_DIR = os.path.join(BASE_DIR, "images")

def create_backup():
    print("Iniciando backup del proyecto...")
    
    # 1. Limpiar la carpeta backup/
    if os.path.exists(BACKUP_DIR):
        print(f"Borrando contenido de {BACKUP_DIR}...")
        shutil.rmtree(BACKUP_DIR)
    os.makedirs(BACKUP_DIR, exist_ok=True)
    
    # 2. Crear estructura de directorios en backup/
    backup_src = os.path.join(BACKUP_DIR, "src")
    backup_output = os.path.join(BACKUP_DIR, "output")
    backup_images = os.path.join(BACKUP_DIR, "images")
    os.makedirs(backup_src, exist_ok=True)
    os.makedirs(backup_output, exist_ok=True)
    os.makedirs(backup_images, exist_ok=True)
    
    # 3. Copiar archivos
    copied_files = []
    
    # Copiar scripts .py desde src/
    for src_file in glob.glob(os.path.join(SRC_DIR, "*.py")):
        dst_file = os.path.join(backup_src, os.path.basename(src_file))
        shutil.copy2(src_file, dst_file)
        copied_files.append(dst_file)
    
    # Copiar videos .mp4 desde output/
    for video_file in glob.glob(os.path.join(OUTPUT_DIR, "*.mp4")):
        dst_file = os.path.join(backup_output, os.path.basename(video_file))
        shutil.copy2(video_file, dst_file)
        copied_files.append(dst_file)
    
    # Copiar diapositivas .png desde images/
    for image_file in glob.glob(os.path.join(IMAGES_DIR, "*.png")):
        dst_file = os.path.join(backup_images, os.path.basename(image_file))
        shutil.copy2(image_file, dst_file)
        copied_files.append(dst_file)
    
    # Copiar musica_fondo.mp3 desde la raíz (o buscar en otras carpetas)
    music_file = os.path.join(BASE_DIR, "musica_fondo.mp3")
    if os.path.exists(music_file):
        dst_file = os.path.join(BACKUP_DIR, "musica_fondo.mp3")
        shutil.copy2(music_file, dst_file)
        copied_files.append(dst_file)
    else:
        print(f"Advertencia: No se encontró musica_fondo.mp3 en {BASE_DIR}")
    
    # Copiar otros archivos potenciales (.csv, .txt) desde la raíz
    for ext in ["*.csv", "*.txt"]:
        for other_file in glob.glob(os.path.join(BASE_DIR, ext)):
            dst_file = os.path.join(BACKUP_DIR, os.path.basename(other_file))
            shutil.copy2(other_file, dst_file)
            copied_files.append(dst_file)
    
    # 4. Listar archivos respaldados
    print("\nArchivos respaldados:")
    for file in sorted(copied_files):
        print(f"- {file}")
    print(f"\nBackup completado en {BACKUP_DIR}")

if __name__ == "__main__":
    create_backup()
