import csv
import logging
from pathlib import Path
from datetime import datetime
import random
import shutil

# Configuración del logging
logging.basicConfig(
    filename='/Users/pablostiefel/Documents/QuizFutbolYouTube/generar_quiz_data.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def load_used_questions(used_questions_path):
    used_questions = set()
    if used_questions_path.exists() and used_questions_path.stat().st_size > 0:
        with open(used_questions_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f, quoting=csv.QUOTE_ALL)
            try:
                next(reader)  # Saltar encabezado
                for row in reader:
                    if len(row) >= 5:
                        used_questions.add(row[0])
            except StopIteration:
                pass
    return used_questions

def load_questions(file_path, theme, used_questions):
    questions_by_source = {'A': [], 'B': [], 'C': []}
    invalid_questions = []
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, quoting=csv.QUOTE_ALL)
        try:
            next(reader)  # Saltar encabezado
        except StopIteration:
            logging.error(f"Archivo vacío o sin encabezado: {file_path}")
            return questions_by_source, invalid_questions
        for row in reader:
            if len(row) != 6:
                logging.warning(f"Pregunta inválida en {file_path}: {row} - Formato incorrecto: se esperan 6 campos")
                invalid_questions.append(row + [datetime.now().isoformat(), theme, 'inválida'])
                continue
            question, opt_a, opt_b, opt_c, answer, source = row
            if source not in ['A', 'B', 'C']:
                logging.warning(f"Pregunta inválida en {file_path}: {row} - Fuente inválida: {source}")
                invalid_questions.append(row + [datetime.now().isoformat(), theme, 'inválida'])
                continue
            if question in used_questions:
                logging.info(f"Pregunta duplicada saltada: {question}")
                invalid_questions.append(row + [datetime.now().isoformat(), theme, 'duplicada'])
                continue
            if not question.endswith('?'):
                logging.warning(f"Pregunta inválida en {file_path}: {row} - Pregunta no termina en ?")
                invalid_questions.append(row + [datetime.now().isoformat(), theme, 'inválida'])
                continue
            if answer not in [opt_a, opt_b, opt_c]:
                logging.warning(f"Pregunta inválida en {file_path}: {row} - Respuesta no coincide con ninguna opción")
                invalid_questions.append(row + [datetime.now().isoformat(), theme, 'inválida'])
                continue
            questions_by_source[source].append([question, opt_a, opt_b, opt_c, answer])
            used_questions.add(question)
    return questions_by_source, invalid_questions

def update_questions_all(file_path, selected_questions, invalid_questions):
    remaining_questions = []
    selected_questions_set = {row[0] for row in selected_questions}
    invalid_questions_set = {row[0] for row in invalid_questions}
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, quoting=csv.QUOTE_ALL)
        header = next(reader)
        for row in reader:
            if len(row) == 6 and row[0] not in selected_questions_set and row[0] not in invalid_questions_set:
                remaining_questions.append(row)
    with open(file_path, 'w', encoding='utf-8') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        writer.writerow(header)
        writer.writerows(remaining_questions)
    logging.info(f"Actualizado {file_path} con {len(remaining_questions)} preguntas restantes")

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--theme', required=True)
    args = parser.parse_args()
    theme = args.theme

    base_dir = Path('/Users/pablostiefel/Documents/QuizFutbolYouTube')
    questions_dir = base_dir / 'movies'
    output_dir = base_dir / 'movies'
    used_questions_path = base_dir / 'preguntas_usadas.csv'
    questions_all_path = questions_dir / 'Questions_All.csv'
    questions_all_copy = questions_dir / 'Questions_All_copy.csv'

    # Crear directorio de salida si no existe
    output_dir.mkdir(exist_ok=True)

    # Hacer copia de Questions_All.csv
    if questions_all_path.exists():
        shutil.copy(questions_all_path, questions_all_copy)
        logging.info(f"Creada copia de {questions_all_path} en {questions_all_copy}")

    # Cargar preguntas usadas
    used_questions = load_used_questions(used_questions_path)

    # Cargar preguntas de Questions_All.csv
    questions_by_source, invalid_questions = load_questions(questions_all_path, theme, used_questions)

    # Verificar número de preguntas válidas
    min_required = 107
    for source, questions in questions_by_source.items():
        available = len(questions)
        logging.info(f"Fuente {source}: {available} preguntas válidas disponibles")
        if available < min_required:
            logging.error(f"No hay suficientes preguntas para fuente {source}: {available} disponibles, se requieren {min_required}")
            print(f"Error: No hay suficientes preguntas para fuente {source}. Disponibles: {available}, requeridas: {min_required}")
            raise ValueError(f"No hay suficientes preguntas para fuente {source}")

    # Seleccionar preguntas con distribución balanceada
    all_questions = []
    target_per_source = {'A': 107, 'B': 107, 'C': 106}  # 107 + 107 + 106 = 320
    for source, questions in questions_by_source.items():
        num_to_take = target_per_source[source]
        random.shuffle(questions)  # Mezclar para evitar sesgo
        selected = questions[:num_to_take]
        all_questions.extend(selected)
        logging.info(f"Tomando {num_to_take} preguntas de fuente {source}")

    # Verificar total de preguntas
    total_questions = len(all_questions)
    if total_questions != 320:
        logging.error(f"No se obtuvieron 320 preguntas: solo {total_questions} disponibles")
        print(f"Error: No se obtuvieron 320 preguntas, solo {total_questions} disponibles")
        raise ValueError(f"No se obtuvieron 320 preguntas")

    # Escribir Quiz_data.csv (sin columna source)
    output_path = output_dir / 'Quiz_data.csv'
    with open(output_path, 'w', encoding='utf-8') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        writer.writerow(['question', 'option_a', 'option_b', 'option_c', 'answer'])
        writer.writerows(all_questions)

    # Actualizar preguntas_usadas.csv
    with open(used_questions_path, 'a', encoding='utf-8') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        if used_questions_path.stat().st_size == 0:
            writer.writerow(['question', 'option_a', 'option_b', 'option_c', 'answer', 'source', 'timestamp', 'theme', 'status'])
        for question in all_questions:
            writer.writerow(question + [source, datetime.now().isoformat(), theme, 'válida'])
        for invalid in invalid_questions:
            writer.writerow(invalid)

    # Actualizar Questions_All.csv
    update_questions_all(questions_all_path, all_questions, invalid_questions)

if __name__ == "__main__":
    main()