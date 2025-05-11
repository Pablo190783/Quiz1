import os
import subprocess
import shutil
import logging
import traceback
import csv
from pathlib import Path
from datetime import datetime

BASE_DIR = "/Users/pablostiefel/Documents/QuizFutbolYouTube"
VENV_PYTHON = os.path.join(BASE_DIR, "venv/bin/python")
SRC_DIR = os.path.join(BASE_DIR, "src")
IMAGES_DIR = os.path.join(BASE_DIR, "images")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
LOG_FILE = os.path.join(BASE_DIR, "generacion_videos.log")

# Configuración del logging
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def run_script(script_name, args=None):
    script_path = os.path.join(SRC_DIR, script_name)
    cmd = [VENV_PYTHON, script_path]
    if args:
        cmd.extend(args)
    logging.info(f"Ejecutando {script_name} con args {args}")
    print(f"Ejecutando {script_name} con args {args}...")
    try:
        result = subprocess.run(cmd, check=True, text=True, capture_output=True)
        print(result.stdout)
        logging.info(result.stdout)
        if result.stderr:
            print(f"Advertencias en {script_name}: {result.stderr}")
            logging.warning(f"Advertencias en {script_name}: {result.stderr}")
        return result.stdout, True
    except subprocess.CalledProcessError as e:
        error_msg = f"Error ejecutando {script_name}: {e}\nStdout: {e.stdout}\nStderr: {e.stderr}"
        print(error_msg)
        logging.error(error_msg)
        return e.stderr, False

def load_questions_map(file_path):
    question_to_source = {}
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, quoting=csv.QUOTE_ALL)
        next(reader)  # Saltar encabezado
        for row in reader:
            if len(row) == 6:
                question, _, _, _, _, source = row
                if source in ['A', 'B', 'C']:
                    question_to_source[question] = source
    return question_to_source

def move_questions_to_used(quiz_data_path, used_questions_path, questions_all_path, theme):
    question_to_source = load_questions_map(questions_all_path)
    questions = []
    with open(quiz_data_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, quoting=csv.QUOTE_ALL)
        next(reader)  # Saltar encabezado
        for row in reader:
            if len(row) == 5:
                question = row[0]
                source = question_to_source.get(question, 'Unknown')
                questions.append(row + [source, datetime.now().isoformat(), theme, 'válida'])

    with open(used_questions_path, 'a', encoding='utf-8') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        if used_questions_path.stat().st_size == 0:
            writer.writerow(['question', 'option_a', 'option_b', 'option_c', 'answer', 'source', 'timestamp', 'theme', 'status'])
        writer.writerows(questions)
    logging.info(f"Movidas {len(questions)} preguntas a {used_questions_path}")

def clear_quiz_data(quiz_data_path):
    with open(quiz_data_path, 'w', encoding='utf-8') as f:
        f.write('')
    logging.info(f"Vaciado {quiz_data_path}")
    print(f"Vaciado {quiz_data_path}")

def main():
    # Configuración
    base_dir = Path(BASE_DIR)
    quiz_data_path = base_dir / 'movies' / 'Quiz_data.csv'
    used_questions_path = base_dir / 'preguntas_usadas.csv'
    questions_all_path = base_dir / 'movies' / 'Questions_All.csv'
    theme = 'movies'

    # Validación y generación de CSV
    stdout, success = run_script("run_quiz_pipeline.py", ["--theme", "movies"])
    if not success:
        error_msg = f"Fallo en run_quiz_pipeline.py: {stdout}"
        print(error_msg)
        logging.error(error_msg)
        return

    # Limpieza de carpetas
    for directory in [IMAGES_DIR, OUTPUT_DIR, os.path.join(BASE_DIR, "temp")]:
        if os.path.exists(directory):
            print(f"Limpiando {directory}...")
            logging.info(f"Limpiando {directory}")
            shutil.rmtree(directory)
        os.makedirs(directory, exist_ok=True)

    # Generar 10 videos, cada uno con 32 preguntas
    questions_per_video = 32
    total_videos = 10
    successful_videos = 0

    for video_index in range(1, total_videos + 1):
        start_idx = (video_index - 1) * questions_per_video + 1
        end_idx = start_idx + questions_per_video - 1
        print(f"Generando video {video_index} (preguntas {start_idx} a {end_idx})")
        logging.info(f"Generando video {video_index} (preguntas {start_idx} a {end_idx})")

        try:
            scripts = [
                ("generar_diapositivas.py", [str(video_index), str(start_idx), str(end_idx)]),
                ("generar_video.py", [str(video_index)]),
                ("unir_videos.py", [str(video_index)]),
                ("agregar_audio_completo.py", [str(video_index)])
            ]
            all_success = True
            for script_name, args in scripts:
                if not run_script(script_name, args)[1]:
                    all_success = False
                    break
            if all_success:
                successful_videos += 1
                print(f"Video {video_index} generado correctamente")
                logging.info(f"Video {video_index} generado correctamente")
            else:
                print(f"Fallo al generar video {video_index}")
                logging.error(f"Fallo al generar video {video_index}")
        except Exception as e:
            error_msg = f"Error inesperado generando video {video_index}: {e}"
            print(error_msg)
            logging.error(error_msg)
            traceback.print_exc()

    # Mover preguntas a preguntas_usadas.csv y vaciar Quiz_data.csv
    if successful_videos == total_videos:
        move_questions_to_used(quiz_data_path, used_questions_path, questions_all_path, theme)
        clear_quiz_data(quiz_data_path)
    else:
        logging.warning("No se movieron preguntas ni se vació Quiz_data.csv porque no todos los videos se generaron correctamente")
        print("Advertencia: No se movieron preguntas ni se vació Quiz_data.csv porque no todos los videos se generaron correctamente")

    print(f"Proceso completo. {successful_videos}/{total_videos} videos generados correctamente.")
    logging.info(f"Proceso completo. {successful_videos}/{total_videos} videos generados correctamente.")
    print(f"Revisa el log en {LOG_FILE} para detalles.")

if __name__ == "__main__":
    main()