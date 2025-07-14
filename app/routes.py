from flask import Blueprint, render_template, request, jsonify
from app.controllers.rename_controller import imageRename
from app.utils.debug_logger import logger
import os
import json
import threading

main = Blueprint("main", __name__)

# Variável global para controlar progresso
progress = {
    "total": 0,
    "done": 0,
    "status": "idle"
}

def process_images_thread(folder, list_images, settings):
    progress["total"] = len(list_images)
    progress["done"] = 0
    progress["status"] = "processing"

    renamer = imageRename(settings)

    for img in list_images:
        renamer.rename(folder, [img])  # Processa uma imagem por vez
        progress["done"] += 1

    progress["status"] = "done"

@main.route("/")
def index():
    return render_template("index.html")

@main.route("/select_folder")
def select_folder():
    try:
        # Use sua função de seleção de pasta aqui, por ex:
        from app.utils.folder_selector import folder_selector
        folder_selected = folder_selector()
        return jsonify({"folder": folder_selected})
    except Exception as e:
        logger(e)
        return jsonify({"folder": None})

@main.route("/process_folder", methods=["POST"])
def process_folder():
    try:
        data = request.get_json()
        folder = data.get("folderPath")

        if not folder or not os.path.exists(folder):
            return jsonify({"status": "error", "message": "Pasta inválida."})

        list_images = [
            f for f in os.listdir(folder)
            if f.lower().endswith(('.jpg', '.jpeg', '.png'))
        ]

        if not list_images:
            return jsonify({"status": "error", "message": "Nenhuma imagem encontrada na pasta."})

        # Carrega as configurações
        path_settings = os.path.join("src", "config", "settings.json")
        with open(path_settings, 'rb') as f_json:
            settings = json.load(f_json)

        # Inicia o processamento em thread para não travar o servidor
        thread = threading.Thread(target=process_images_thread, args=(folder, list_images, settings))
        thread.start()

        return jsonify({"status": "ok", "message": "Processamento iniciado."})
    except Exception as e:
        logger(e)
        return jsonify({"status": "error", "message": str(e)})

@main.route("/progress")
def get_progress():
    return jsonify(progress)
