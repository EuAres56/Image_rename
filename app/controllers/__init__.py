# app/controllers/__init__.py
from ..utils.debug_logger import logger
from .ocr_controller import get_ocr, process_image
from .rename_controller import imageRename

__all__ = ['logger', 'get_ocr', 'process_image', 'imageRename']
