import os
import subprocess
import shutil
import logging
import argparse

BASE_DIR = "/Users/pablostiefel/Documents/QuizFutbolYouTube"
VENV_PYTHON = os.path.join(BASE_DIR, "venv/bin/python")
SRC_DIR = os.path.join(BASE_DIR, "src")
LOG_FILE = os.path.join(BASE_DIR, "quiz_pipeline.log")

# Configurar logging
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
        return error_msg, False

def main():
    parser = argparse.ArgumentParser(description="Orquesta la generación y validación de Quiz_data.csv")
    parser.add_argument("--theme", default="movies", help="Tema de las preguntas (por ejemplo, movies, sports)")
    args = parser.parse_args()

    theme = args.theme
    theme_dir = os.path.join(BASE_DIR, theme)
    quiz_data_path = os.path.join(theme_dir, "Quiz_data.csv")
    root_quiz_data_path = os.path.join(BASE_DIR, "Quiz_data.csv")

    # Generar Quiz_data.csv
    stdout, success = run_script("generar_quiz_data.py", ["--theme", theme])
    if not success:
        error_msg = f"Fallo en generar_quiz_data.py: {stdout}"
        print(error_msg)
        logging.error(error_msg)
        return

    # Validar Quiz_data.csv
    stdout, success = run_script("verificar_quiz_data.py")
    if not success:
        error_msg = f"Fallo en verificar_quiz_data.py: {stdout}"
        print(error_msg)
        logging.error(error_msg)
        return

    # Copiar Quiz_data.csv a la raíz
    try:
        shutil.copy(quiz_data_path, root_quiz_data_path)
        print(f"Copiado {quiz_data_path} a {root_quiz_data_path}")
        logging.info(f"Copiado {quiz_data_path} a {root_quiz_data_path}")
    except Exception as e:
        error_msg = f"Error copiando Quiz_data.csv: {e}"
        print(error_msg)
        logging.error(error_msg)
        return

    print("Quiz_data.csv generado y copiado correctamente")
    logging.info("Quiz_data.csv generado y copiado correctamente")

if __name__ == "__main__":
    main()