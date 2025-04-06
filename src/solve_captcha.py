import shutil
import cv2
import os
from easyocr import easyocr
import numpy as np

class captcha_resolver:
    def __init__(self, captcha_path: str):
        self.captcha_path = captcha_path

    captcha_folder_path = 'captcha/'
    preprocess_image_name = 'captcha_processed.png'
    
    def extract_value_from_captcha(self):
        self._preprocess_image()

        reader = easyocr.Reader(lang_list=['ru'])
        preprocess_image_path = self.captcha_folder_path + self.preprocess_image_name
        result = reader.readtext(preprocess_image_path, detail=0, allowlist='АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя0123456789')
        
        self.clear_space()

        return "".join(result).replace(" ", "")

    def _preprocess_image(self):
        # WB img
        img = cv2.imread(self.captcha_path, cv2.IMREAD_GRAYSCALE)
        
        # scaling
        scale_factor = 2
        img = cv2.resize(img, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_CUBIC)

        _, img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        
        # morf
        kernel = np.ones((2, 2), np.uint8)
        img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
        
        preprocess_image_path = self.captcha_folder_path + self.preprocess_image_name
        cv2.imwrite(preprocess_image_path, img)

    def clear_space(self):
        if os.path.exists(self.captcha_folder_path):
            shutil.rmtree(self.captcha_folder_path)
