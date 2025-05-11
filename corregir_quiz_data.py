import sys
import csv
import logging
import random
from collections import Counter

# Configurar logging
logging.basicConfig(
    filename="/Users/pablostiefel/Documents/QuizFutbolYouTube/corregir_quiz_data.log",
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Rutas absolutas
CSV_PATH = "/Users/pablostiefel/Documents/QuizFutbolYouTube/quiz_data_test.csv"
OUTPUT_CSV_PATH = "/Users/pablostiefel/Documents/QuizFutbolYouTube/quiz_data_test_corrected.csv"

# Secuencia esperada por bloque (32 preguntas)
EXPECTED_SEQUENCE = [
    'B', 'B', 'C', 'B', 'A', 'B', 'A', 'B', 'C', 'A',
    'B', 'A', 'C', 'C', 'B', 'C', 'A', 'C', 'A', 'B',
    'C', 'A', 'A', 'B', 'B', 'C', 'A', 'B', 'A', 'C',
    'C', 'C'
]

def get_correct_option(row):
    """Mapa el valor de 'answer' a A, B, o C."""
    answer = row['answer'].strip()
    options = {
        'A': row['option_a'].strip(),
        'B': row['option_b'].strip(),
        'C': row['option_c'].strip()
    }
    for option, value in options.items():
        if answer == value:
            return option
    raise ValueError(f"El valor de 'answer' ({answer}) no coincide con ninguna opción: A={options['A']}, B={options['B']}, C={options['C']}")

def adjust_distribution(rows, answers):
    """Ajusta la distribución a 100 A, 110 B, 110 C."""
    answer_counts = Counter(answers)
    target_counts = {'A': 100, 'B': 110, 'C': 110}
    adjustments = []

    # Calcular diferencias
    for option in ['A', 'B', 'C']:
        current = answer_counts.get(option, 0)
        target = target_counts[option]
        diff = target - current
        if diff > 0:
            # Necesitamos más de esta opción
            adjustments.append((option, diff))
        elif diff < 0:
            # Tenemos demasiadas, convertir a otra opción
            adjustments.append((option, diff))

    # Realizar ajustes
    adjusted_rows = rows.copy()
    adjusted_answers = answers.copy()
    for option, diff in adjustments:
        if diff > 0:
            # Convertir otras opciones a esta
            candidates = [(i, a) for i, a in enumerate(adjusted_answers) if a != option]
            random.shuffle(candidates)
            for i, _ in candidates[:diff]:
                # Elegir la nueva opción correcta
                adjusted_rows[i]['answer'] = adjusted_rows[i][f'option_{option.lower()}']
                adjusted_answers[i] = option
        elif diff < 0:
            # Convertir esta opción a otra
            candidates = [(i, a) for i, a in enumerate(adjusted_answers) if a == option]
            random.shuffle(candidates)
            for i, _ in candidates[:abs(diff)]:
                # Elegir otra opción aleatoriamente
                other_options = [o for o in ['A', 'B', 'C'] if o != option]
                new_option = random.choice(other_options)
                adjusted_rows[i]['answer'] = adjusted_rows[i][f'option_{new_option.lower()}']
                adjusted_answers[i] = new_option

    return adjusted_rows, adjusted_answers

def corregir_quiz_data():
    print("Corrigiendo quiz_data.csv...", flush=True)
    logging.info("Iniciando corrección de quiz_data.csv")

    # Leer el archivo CSV
    try:
        with open(CSV_PATH, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            if not all(col in reader.fieldnames for col in ['question', 'option_a', 'option_b', 'option_c', 'answer']):
                error_msg = "Faltan columnas requeridas en el CSV"
                print(error_msg, flush=True)
                logging.error(error_msg)
                sys.exit(1)
            rows = []
            answers = []
            for row in reader:
                rows.append(row)
                try:
                    answers.append(get_correct_option(row))
                except ValueError as e:
                    error_msg = f"Error en la fila {reader.line_num}: {e}"
                    print(error_msg, flush=True)
                    logging.error(error_msg)
                    sys.exit(1)
    except FileNotFoundError:
        error_msg = f"Archivo no encontrado: {CSV_PATH}"
        print(error_msg, flush=True)
        logging.error(error_msg)
        sys.exit(1)
    except Exception as e:
        error_msg = f"Error leyendo CSV: {e}"
        print(error_msg, flush=True)
        logging.error(error_msg)
        sys.exit(1)

    # Verificar número total de preguntas
    if len(answers) != 320:
        error_msg = f"Se esperaban 320 preguntas, pero se encontraron {len(answers)}"
        print(error_msg, flush=True)
        logging.error(error_msg)
        sys.exit(1)

    # Ajustar distribución si es necesario
    answer_counts = Counter(answers)
    expected_counts = {'A': 100, 'B': 110, 'C': 110}
    if any(answer_counts.get(opt, 0) != expected_counts[opt] for opt in expected_counts):
        print("Distribución incorrecta detectada, ajustando...", flush=True)
        logging.info("Distribución incorrecta detectada, ajustando")
        rows, answers = adjust_distribution(rows, answers)
        # Verificar distribución ajustada
        answer_counts = Counter(answers)
        for option, expected in expected_counts.items():
            actual = answer_counts.get(option, 0)
            if actual != expected:
                error_msg = f"No se pudo ajustar la distribución para {option}: esperado {expected}, encontrado {actual}"
                print(error_msg, flush=True)
                logging.error(error_msg)
                sys.exit(1)

    # Agrupar preguntas por opción correcta
    questions_by_answer = {'A': [], 'B': [], 'C': []}
    for row, answer in zip(rows, answers):
        questions_by_answer[answer].append(row)

    # Reordenar preguntas según la secuencia
    corrected_rows = []
    for _ in range(10):  # 10 bloques
        for expected_answer in EXPECTED_SEQUENCE:
            if not questions_by_answer[expected_answer]:
                error_msg = f"No hay suficientes preguntas con respuesta {expected_answer}"
                print(error_msg, flush=True)
                logging.error(error_msg)
                sys.exit(1)
            # Tomar la primera pregunta disponible y removerla
            corrected_rows.append(questions_by_answer[expected_answer].pop(0))

    # Escribir el CSV corregido
    try:
        with open(OUTPUT_CSV_PATH, 'w', encoding='utf-8', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=reader.fieldnames)
            writer.writeheader()
            writer.writerows(corrected_rows)
    except Exception as e:
        error_msg = f"Error escribiendo CSV corregido: {e}"
        print(error_msg, flush=True)
        logging.error(error_msg)
        sys.exit(1)

    print(f"CSV corregido generado en: {OUTPUT_CSV_PATH}", flush=True)
    logging.info(f"CSV corregido generado en: {OUTPUT_CSV_PATH}")

if __name__ == "__main__":
    try:
        corregir_quiz_data()
    except Exception as e:
        error_msg = f"Error inesperado: {e}"
        print(error_msg, flush=True)
        logging.error(error_msg)
        sys.exit(1)