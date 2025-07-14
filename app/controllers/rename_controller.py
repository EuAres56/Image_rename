import os
import re
import json
from app.controllers.ocr_controller import get_ocr
from app.utils.debug_logger import logger

class imageRename:
    def __init__(self, settings, progress_callback=None):
        """
        settings: dict com 'language' e 'api_key'
        progress_callback: função opcional para reportar progresso (ex: atualizar estado no backend)
        """
        self.settings = settings
        self.progress_callback = progress_callback

    def rename(self, dir_src, list_images):
        if not list_images:
            return
        
        try:
            language = self.settings['language']
            api_key = self.settings['api_key']
        except Exception as e:
            logger(e)
            print(f"{type(e)}: {e}")
            return
        
        count_fail = 0
        total = len(list_images)

        # Para cada imagem, processa OCR e renomeia
        for idx, img_name in enumerate(list_images, start=1):
            try:
                img_path = os.path.join(dir_src, img_name)
                ocr_result = get_ocr(img_path, api_key, language)

                if not ocr_result:
                    count_fail += 1
                    new_name = f"{str(count_fail).zfill(3)}_Falha_no_processamento{os.path.splitext(img_name)[1]}"
                    new_path = os.path.join(dir_src, new_name)
                else:
                    txt_img = ocr_result.get("img_text", "")
                    hour = self.search_pattern(txt_img)
                    base_name, ext = os.path.splitext(img_name)

                    if hour:
                        new_name = f"{hour}{ext}"
                    else:
                        count_fail += 1
                        new_name = f"{str(count_fail).zfill(3)}_Falha_no_processamento{ext}"

                    new_path = os.path.join(dir_src, new_name)

                # Evita sobrescrever arquivos existentes
                i = 1
                final_path = new_path
                while os.path.exists(final_path):
                    base, ext = os.path.splitext(new_path)
                    final_path = f"{base}_({str(i).zfill(2)}){ext}"
                    i += 1

                os.replace(img_path, final_path)

                # Atualiza progresso, se callback definido
                if self.progress_callback:
                    self.progress_callback(current=idx, total=total)

            except Exception as e:
                logger(e)
                print(f"Erro processando {img_name}: {type(e)} - {e}")
                # Continua processando as outras imagens

    def search_pattern(self, txt_img):
        pattern = r'\b\d{2}[:;.\-\s]\d{2}[:;.\-\s]\d{2}\b'
        list_hours = re.findall(pattern, txt_img)
        list_hours = [re.sub(r'[:;.\-\s]', ':', h) for h in list_hours]
        list_hours = list(set(list_hours))
        hour = [h for h in list_hours if self.valid_hour(h)]
        if hour:
            return hour[0].replace(":", ".")
        return None

    def valid_hour(self, hour):
        try:
            h, m, s = map(int, hour.split(':'))
            return 0 <= h < 24 and 0 <= m < 60 and 0 <= s < 60
        except Exception:
            return False
