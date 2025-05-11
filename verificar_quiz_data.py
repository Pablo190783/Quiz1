import csv
import logging
from collections import Counter
from pathlib import Path

# Configuración del logging
logging.basicConfig(
    filename="/Users/pablostiefel/Documents/QuizFutbolYouTube/verificar_quiz_data.log",
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def load_questions_map(file_path):
    question_to_source = {}
    if not file_path.exists():
        logging.error(f"Archivo no encontrado: {file_path}")
        raise FileNotFoundError(f"Archivo no encontrado: {file_path}")
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, quoting=csv.QUOTE_ALL)
        next(reader)  # Saltar encabezado
        for row in reader:
            if len(row) == 6:
                question, _, _, _, _, source = row
                if source in ['A', 'B', 'C']:
                    question_to_source[question] = source
    return question_to_source

def verify_quiz_data():
    logging.info("Iniciando verificación de Quiz_data.csv")
    quiz_data_path = "/Users/pablostiefel/Documents/QuizFutbolYouTube/movies/Quiz_data.csv"
    questions_all_copy = "/Users/pablostiefel/Documents/QuizFutbolYouTube/movies/Questions_All_copy.csv"

    # Cargar mapa de preguntas a fuentes
    question_to_source = load_questions_map(questions_all_copy)

    # Leer Quiz_data.csv
    questions = []
    with open(quiz_data_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, quoting=csv.QUOTE_ALL)
        header = next(reader)
        if header != ['question', 'option_a', 'option_b', 'option_c', 'answer']:
            logging.error(f"Encabezado incorrecto en {quiz_data_path}: {header}")
            raise ValueError("Encabezado incorrecto")
        for row in reader:
            questions.append(row)

    # Verificar número de preguntas
    if len(questions) != 320:
        logging.error(f"Número incorrecto de preguntas: esperado 320, encontrado {len(questions)}")
        raise ValueError(f"Número incorrecto de preguntas: {len(questions)}")

    # Verificar formato de cada pregunta
    for i, row in enumerate(questions, start=2):
        if len(row) != 5:
            logging.error(f"Error en la fila {i}: Formato incorrecto, se esperan 5 campos")
            raise ValueError(f"Formato incorrecto en fila {i}")
        question, opt_a, opt_b, opt_c, answer = row
        if not question.endswith('?'):
            logging.error(f"Error en la fila {i}: Pregunta no termina en '?'")
            raise ValueError(f"Pregunta inválida en fila {i}")
        if answer not in [opt_a, opt_b, opt_c]:
            logging.error(f"Error en la fila {i}: El valor de 'answer' ({answer}) no coincide con ninguna opción")
            raise ValueError(f"Respuesta inválida en fila {i}")

    # Verificar distribución
    source_counts = Counter()
    for question in questions:
        source = question_to_source.get(question[0], 'Unknown')
        source_counts[source] += 1

    logging.info(f"Distribución de preguntas: {dict(source_counts)}")
    print(f"Distribución de preguntas: {dict(source_counts)}")
    expected = {'A': 107, 'B': 107, 'C': 106}
    tolerance = 15
    for source in ['A', 'B', 'C']:
        count = source_counts.get(source, 0)
        if not (expected[source] - tolerance <= count <= expected[source] + tolerance):
            logging.error(f"Distribución incorrecta para {source}: esperado {expected[source]} ± {tolerance}, encontrado {count}")
            raise ValueError(f"Distribución incorrecta para {source}: esperado {expected[source]} ± {tolerance}, encontrado {count}")
    if source_counts.get('Unknown', 0) > 0:
        logging.error(f"Se encontraron {source_counts['Unknown']} preguntas sin fuente conocida")
        raise ValueError(f"Se encontraron {source_counts['Unknown']} preguntas sin fuente conocida")

    logging.info("Verificación completada exitosamente")
    print("Verificación completada exitosamente")

if __name__ == "__main__":
    verify_quiz_data()