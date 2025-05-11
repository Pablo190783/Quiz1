from PIL import Image, ImageDraw, ImageFont
import csv
import os
import traceback
import sys
import logging

# Configurar logging
logging.basicConfig(
    filename=os.path.join("/Users/pablostiefel/Documents/QuizFutbolYouTube", "diapositivas.log"),
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Rutas absolutas
BASE_DIR = "/Users/pablostiefel/Documents/QuizFutbolYouTube"
TEMPLATE_QUESTION = os.path.join(BASE_DIR, "plantilla_pregunta.png")
TEMPLATE_ANSWER = os.path.join(BASE_DIR, "plantilla_respuesta.png")
CSV_PATH = os.path.join(BASE_DIR, "quiz_data.csv")
OUTPUT_BASE = os.path.join(BASE_DIR, "images")
FONT_PATH = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"

# Validar archivos de entrada
for path in [TEMPLATE_QUESTION, TEMPLATE_ANSWER, CSV_PATH]:
    if not os.path.exists(path):
        error_msg = f"No se encontró el archivo: {path}"
        print(error_msg)
        logging.error(error_msg)
        raise FileNotFoundError(error_msg)

# Cargar fuentes
try:
    font_question = ImageFont.truetype(FONT_PATH, 60)
    font_option = ImageFont.truetype(FONT_PATH, 40)
    font_answer = ImageFont.truetype(FONT_PATH, 60)
except Exception as e:
    error_msg = f"Error cargando fuentes: {e}"
    print(error_msg)
    logging.error(error_msg)
    raise Exception(error_msg)

# Función para ajustar texto largo
def wrap_text(text, font, max_width):
    words = text.split()
    total_words = len(words)
    
    text_bbox = font.getbbox(text)
    text_width = text_bbox[2] - text_bbox[0]
    if text_width <= max_width:
        return [text]
    
    if total_words > 1:
        best_split = None
        min_width_diff = float('inf')
        
        for split_point in range(1, total_words):
            first_part = " ".join(words[:split_point])
            second_part = " ".join(words[split_point:])
            
            first_bbox = font.getbbox(first_part)
            second_bbox = font.getbbox(second_part)
            first_width = first_bbox[2] - first_bbox[0]
            second_width = second_bbox[2] - second_bbox[0]
            
            if first_width <= max_width and second_width <= max_width:
                width_diff = abs(first_width - second_width)
                if width_diff < min_width_diff:
                    min_width_diff = width_diff
                    best_split = (first_part, second_part)
        
        if best_split:
            return list(best_split)
    
    lines = []
    current_line = ""
    for word in words:
        test_line = current_line + word + " "
        text_bbox = font.getbbox(test_line)
        text_width = text_bbox[2] - text_bbox[0]
        if text_width <= max_width:
            current_line = test_line
        else:
            lines.append(current_line.strip())
            current_line = word + " "
    if current_line:
        lines.append(current_line.strip())
    return lines

# Generar diapositivas para un video específico
def generate_slides(video_index, start_idx, end_idx):
    output_folder = os.path.join(OUTPUT_BASE, f"video{video_index}")
    print(f"Creando carpeta para video {video_index}: {output_folder}")
    logging.info(f"Creando carpeta para video {video_index}: {output_folder}")
    try:
        os.makedirs(output_folder, exist_ok=True)
    except Exception as e:
        error_msg = f"Error creando carpeta {output_folder}: {e}"
        print(error_msg)
        logging.error(error_msg)
        raise Exception(error_msg)
    
    slide_number = 1
    current_idx = 0
    processed_questions = 0
    
    # Contar total de filas en el CSV para validación
    with open(CSV_PATH, newline='', encoding='utf-8') as csvfile:
        total_rows = sum(1 for _ in csvfile) - 1  # Restar 1 por la cabecera
    if end_idx > total_rows:
        error_msg = f"end_idx ({end_idx}) excede el número de preguntas en el CSV ({total_rows})"
        print(error_msg)
        logging.error(error_msg)
        raise ValueError(error_msg)
    
    try:
        with open(CSV_PATH, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                current_idx += 1
                if current_idx < start_idx:
                    continue
                if current_idx > end_idx:
                    break
                print(f"Procesando pregunta {current_idx} para video {video_index}")
                logging.info(f"Procesando pregunta {current_idx} para video {video_index}")
                processed_questions += 1
                
                # Verificar plantillas antes de usarlas
                for template in [TEMPLATE_QUESTION, TEMPLATE_ANSWER]:
                    if not os.path.exists(template):
                        error_msg = f"Plantilla no encontrada: {template}"
                        print(error_msg)
                        logging.error(error_msg)
                        raise FileNotFoundError(error_msg)
                
                # Diapositiva de pregunta
                try:
                    img = Image.open(TEMPLATE_QUESTION)
                    draw = ImageDraw.Draw(img)
                    question_lines = wrap_text(row['question'], font_question, 1200)
                    y_text = 150
                    for line in question_lines:
                        draw.text((960, y_text), line, fill="white", font=font_question, anchor="mm", align="center")
                        y_text += 70
                    draw.text((1000, 400), row['option_a'], fill="black", font=font_option, anchor="mm")
                    draw.text((1000, 600), row['option_b'], fill="black", font=font_option, anchor="mm")
                    draw.text((1000, 800), row['option_c'], fill="black", font=font_option, anchor="mm")
                    output_path = os.path.join(output_folder, f"quiz_futbol_video{video_index}_{str(slide_number).zfill(3)}.png")
                    img.save(output_path, "PNG")
                    img.close()
                    print(f"Guardada diapositiva de pregunta: {output_path}")
                    logging.info(f"Guardada diapositiva de pregunta: {output_path}")
                except Exception as e:
                    error_msg = f"Error generando diapositiva de pregunta {current_idx}: {e}"
                    print(error_msg)
                    logging.error(error_msg)
                    traceback.print_exc()
                    raise
                
                slide_number += 1

                # Diapositiva de respuesta
                try:
                    img = Image.open(TEMPLATE_ANSWER)
                    draw = ImageDraw.Draw(img)
                    answer_lines = wrap_text(row['answer'], font_answer, 700)
                    y_text = 540
                    for line in answer_lines:
                        draw.text((960, y_text), line, fill="black", font=font_answer, anchor="mm", align="center")
                        y_text += 70
                    output_path = os.path.join(output_folder, f"quiz_futbol_video{video_index}_{str(slide_number).zfill(3)}.png")
                    img.save(output_path, "PNG")
                    img.close()
                    print(f"Guardada diapositiva de respuesta: {output_path}")
                    logging.info(f"Guardada diapositiva de respuesta: {output_path}")
                except Exception as e:
                    error_msg = f"Error generando diapositiva de respuesta {current_idx}: {e}"
                    print(error_msg)
                    logging.error(error_msg)
                    traceback.print_exc()
                    raise
                
                slide_number += 1

        if processed_questions == 0:
            error_msg = f"No se procesaron preguntas para video {video_index} (start_idx={start_idx}, end_idx={end_idx})"
            print(error_msg)
            logging.error(error_msg)
            raise ValueError(error_msg)
        print(f"Generadas {slide_number-1} diapositivas para video {video_index} en {output_folder} (procesadas {processed_questions} preguntas)")
        logging.info(f"Generadas {slide_number-1} diapositivas para video {video_index} en {output_folder} (procesadas {processed_questions} preguntas)")
    except Exception as e:
        error_msg = f"Error en generate_slides para video {video_index}: {e}"
        print(error_msg)
        logging.error(error_msg)
        traceback.print_exc()
        raise

if __name__ == "__main__":
    if len(sys.argv) != 4:
        error_msg = "Uso: python generar_diapositivas.py <video_index> <start_idx> <end_idx>"
        print(error_msg)
        logging.error(error_msg)
        sys.exit(1)
    try:
        video_index = int(sys.argv[1])
        start_idx = int(sys.argv[2])
        end_idx = int(sys.argv[3])
        print(f"Iniciando generación de diapositivas para video {video_index} (preguntas {start_idx} a {end_idx})")
        logging.info(f"Iniciando generación de diapositivas para video {video_index} (preguntas {start_idx} a {end_idx})")
        generate_slides(video_index, start_idx, end_idx)
    except ValueError as e:
        error_msg = f"Error: Los argumentos deben ser enteros. Recibido: {sys.argv[1:]}"
        print(error_msg)
        logging.error(error_msg)
        sys.exit(1)
    except Exception as e:
        error_msg = f"Error inesperado: {e}"
        print(error_msg)
        logging.error(error_msg)
        traceback.print_exc()
        sys.exit(1)