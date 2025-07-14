from datetime import datetime
import os
import json

# Geração de logs de erro
def logger(error=False):
    try:
        dir_debug_logs = os.path.join("src", "Temp", "Debug_logs")
        os.makedirs(dir_debug_logs, exist_ok=True)
        if error:
            now = datetime.now()
            dt_log = now.strftime("%d/%m/%Y")
            hr_log = now.strftime("%H:%M:%S")
            e_type = type(error).__name__

            log = { "Data": dt_log, "Hora": hr_log,
                    "Tipo": e_type, "Desc": str(error)}
            
            dt_name = now.strftime("%Y-%m-%d")
            name_file_log = os.path.join(dir_debug_logs, f"{dt_name}_{hr_log.replace(':', '-')}-{log['Tipo']}.json")

            with open(name_file_log, 'w', encoding='utf-8') as debug:
                json.dump(log, debug, ensure_ascii=False, indent=4)
    except: pass