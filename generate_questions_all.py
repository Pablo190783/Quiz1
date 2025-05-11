import csv
import logging
from pathlib import Path
from collections import OrderedDict

# Configuración del logging
logging.basicConfig(
    filename='/Users/pablostiefel/Documents/QuizFutbolYouTube/generate_questions_all.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def is_valid_question(row):
    if len(row) != 5:
        return False, f"Formato incorrecto: se esperan 5 campos, encontrados {len(row)}"
    question, opt_a, opt_b, opt_c, answer = row
    if not question.endswith('?'):
        return False, "Pregunta no termina en ?"
    if answer not in [opt_a, opt_b, opt_c]:
        return False, "Respuesta no coincide con ninguna opción"
    return True, ""

def load_questions(file_path, source, seen_questions):
    questions = []
    invalid_count = 0
    duplicate_count = 0
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, quoting=csv.QUOTE_ALL)
        try:
            next(reader)  # Saltar encabezado
        except StopIteration:
            logging.error(f"Archivo vacío o sin encabezado: {file_path}")
            return questions, invalid_count, duplicate_count
        for row in reader:
            if len(row) != 5:
                logging.warning(f"Pregunta inválida en {file_path}: {row} - Formato incorrecto")
                invalid_count += 1
                continue
            question = row[0]
            is_valid, reason = is_valid_question(row)
            if not is_valid:
                logging.warning(f"Pregunta inválida en {file_path}: {row} - {reason}")
                invalid_count += 1
                continue
            if question in seen_questions:
                logging.info(f"Pregunta duplicada saltada: {question} (fuente {source})")
                duplicate_count += 1
                continue
            questions.append(row + [source])
            seen_questions.add(question)
    return questions, invalid_count, duplicate_count

def main():
    base_dir = Path('/Users/pablostiefel/Documents/QuizFutbolYouTube')
    questions_dir = base_dir / 'movies'
    output_path = questions_dir / 'Questions_All.csv'

    # Inicializar conjunto de preguntas vistas
    seen_questions = set()

    # Cargar preguntas de cada fuente
    sources = [
        ('Questions_A.csv', 'A'),
        ('Questions_B.csv', 'B'),
        ('Questions_C.csv', 'C')
    ]
    all_questions = []
    for file_name, source in sources:
        file_path = questions_dir / file_name
        questions, invalid_count, duplicate_count = load_questions(file_path, source, seen_questions)
        all_questions.extend(questions)
        logging.info(f"Cargadas {len(questions)} preguntas válidas de {file_path} (descartadas: {invalid_count} inválidas, {duplicate_count} duplicadas)")

    # Verificar número de preguntas por fuente
    source_counts = OrderedDict([('A', 0), ('B', 0), ('C', 0)])
    for question in all_questions:
        source_counts[question[-1]] += 1
    for source, count in source_counts.items():
        logging.info(f"Fuente {source}: {count} preguntas válidas")
        if count < 107:
            logging.warning(f"Advertencia: Fuente {source} tiene menos de 107 preguntas válidas. Se recomienda generar más preguntas.")

    # Escribir Questions_All.csv
    with open(output_path, 'w', encoding='utf-8') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        writer.writerow(['question', 'option_a', 'option_b', 'option_c', 'answer', 'source'])
        writer.writerows(all_questions)

    logging.info(f"Generado {output_path} con {len(all_questions)} preguntas totales")

if __name__ == "__main__":
    main()