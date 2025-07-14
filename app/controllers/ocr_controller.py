import http.client
import mimetypes
import os
import json
from PIL import Image, ImageFilter, ImageOps
from datetime import datetime
from app.utils.debug_logger import logger

def process_image(dir_img):
    try:
        # Carregar imagem
        img = Image.open(dir_img).convert("RGB")

        # Extrair o canal azul (equivalente ao b = cv2.split(img)[0])
        b_channel = img.getchannel("B")

        # Converter para escala de cinza (usando azul como base)
        gray = b_channel.convert("L")

        # Threshold simples (binário)
        threshold = 140  # ajuste conforme necessidade
        binary = gray.point(lambda x: 255 if x > threshold else 0)

        # Aplicar nitidez (substitui filtro de kernel manual)
        sharpened = binary.filter(ImageFilter.SHARPEN)

        # Aplicar filtro de ruído (opcional, substitui medianBlur)
        final = sharpened.filter(ImageFilter.MedianFilter(size=3))

        # Salvar imagem temporária para envio
        dt = datetime.now().strftime("%d-%m-%Y__%H-%M-%S")
        dir_debug_img = ".\\src\\Temp\\Debug_images\\"
        os.makedirs(dir_debug_img, exist_ok=True)

        # Limpeza de imagens antigas
        try:
            list_debug_img = sorted(f for f in os.listdir(dir_debug_img) if f.lower().endswith('.png'))
            if len(list_debug_img) >= 10:
                for f in list_debug_img[:len(list_debug_img) - 9]:
                    os.remove(os.path.join(dir_debug_img, f))
        except Exception as e:
            logger(e)
            print(f"{type(e)}: {e}")

        temp_file = os.path.join(dir_debug_img, f"{dt}__debug_image.png")
        final.save(temp_file)

        return temp_file
    except Exception as e:
        logger(e)
        print(f"{type(e)}: {e}")
        return None

def get_ocr(dir_img, api_key, language):
    # Processa a imagem para melhor leitura
    temp_file = process_image(dir_img)

    if not temp_file: return None
        
    try:
        # Preparar multipart/form-data
        boundary = '----WebKitFormBoundary7MA4YWxkTrZu0gW'
        with open(temp_file, 'rb') as f:
            file_content = f.read()

        filename = os.path.basename(temp_file)
        body = (
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="filename"; filename="{filename}"\r\n'
            f"Content-Type: {mimetypes.guess_type(temp_file)[0] or 'application/octet-stream'}\r\n\r\n"
        ).encode() + file_content + b"\r\n"

        form_fields = {
            'apikey': api_key,
            'language': language,
            'isOverlayRequired': 'false',
            'OCREngine': '2'
        }

        for key, value in form_fields.items():
            body += (
                f"--{boundary}\r\n"
                f'Content-Disposition: form-data; name="{key}"\r\n\r\n{value}\r\n'
            ).encode()

        body += f"--{boundary}--\r\n".encode()

        # Enviar requisição
        conn = http.client.HTTPSConnection("api.ocr.space")
        headers = {
            "Content-Type": f"multipart/form-data; boundary={boundary}",
            "Content-Length": str(len(body))
        }

        conn.request("POST", "/parse/image", body=body, headers=headers)
        response = conn.getresponse()
        response_data = response.read().decode()
        conn.close()

        # Processar resposta
        result = json.loads(response_data)

        if isinstance(result, dict):
            if result.get("IsErroredOnProcessing"):
                raise ValueError(result.get("ErrorMessage", ["Erro desconhecido no processamento"])[0])

            parsed_results = result.get("ParsedResults", [])
            if parsed_results:
                return {
                    "img_dir": dir_img,
                    "img_text": parsed_results[0].get("ParsedText", "")
                }
            else:
                raise ValueError("A API não retornou resultados.")
        else:
            raise ValueError("Resposta inválida da API.")

    except Exception as e:
        logger(e)
        print(f"{type(e)}: {e}")
        return None