from app.utils.debug_logger import logger
def folder_selector():
    try:
        import tkinter as tk
        from tkinter import filedialog

        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)  # Garante que a janela fique na frente

        folder_selected = filedialog.askdirectory(title="Selecione a pasta com imagens")
        root.destroy()
        return folder_selected if folder_selected else None

    except Exception as e:
        logger(e)
        return None
