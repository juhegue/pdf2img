# -*- coding: utf-8 -*-

"""
por Juhegue
Recorta un pdf al texto que contenga y lo pasa a imagen
Parametros:
  pdf2img origen imagen_destino ampliación(defecto=2)
jue 16 nov 2023 08:17:12 CET
"""

import os
import tempfile
import sys
import fitz             # PyMuPDF
from PIL import Image   # Pillow


AMPLIA = 1


def pdf_to_text_image(pdf_path, output_image_path, amplia):
    image_tmp = os.path.join(tempfile.gettempdir(), next(tempfile._get_candidate_names())) + ".png"

    pdf_document = fitz.open(pdf_path)

    page = pdf_document[0]
    img = page.get_pixmap(dpi=72*amplia)
    img.save(image_tmp)

    image = Image.open(image_tmp)
    # image.show()

    words = page.get_text("words")

    xizq = ysup = xder = yinf = None
    for word in words:
        x_izq, y_sup, x_der, y_inf, texto, a, b, c = word
        yinf = y_inf
        if xizq is None:
            xizq = x_izq
            xder = x_der
            ysup = y_sup
        else:
            if xizq > x_izq:
                xizq = x_izq

            if x_der > xder:
                xder = x_der

    if xizq is None:
        img = Image.new("RGB", (1, 1), (255, 255, 255))
        img.save(output_image_path)
    else:
        img_crop = image.crop((xizq*amplia, ysup*amplia, xder*amplia, yinf*amplia))
        img_crop.save(output_image_path, **image.info)
    # img_crop.show()

    os.remove(image_tmp)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(f'{__doc__}')
    else:
        try:
            amplia = int(sys.argv[3]) if len(sys.argv) > 3 else AMPLIA
            pdf_to_text_image(sys.argv[1], sys.argv[2], amplia)

        except Exception as e:
            print(e)