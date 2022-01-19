import math
import random
import string
from typing import Optional

from PIL import Image, ImageFont, ImageDraw
import cv2

import requests

DEFAULT_DOWNLOADED_IMAGE = "tmp.jpg"


def download_image(url: str) -> Optional[str]:
    if not url:
        return

    response = requests.get(url)
    if response.status_code != 200:
        return

    with open(DEFAULT_DOWNLOADED_IMAGE, 'wb') as f:
        f.write(response.content)
    return DEFAULT_DOWNLOADED_IMAGE



def create_our_image(image_filename: str, price: str, old_price: str, template_name: str = "template.png"):
    img = cv2.imread(image_filename)

    template = cv2.imread(template_name)
    x_offset = 500 - int(math.floor(img.shape[1] / 2))
    y_offset = int(math.floor(template.shape[0] / 2)) - int(math.floor(img.shape[0] / 2)) + 70
    template[y_offset:y_offset + img.shape[0], x_offset:x_offset + img.shape[1]] = img
    output_filename = ''.join(random.choices(string.ascii_letters, k=15)) + '.png'
    cv2.imwrite(output_filename, template)

    my_image = Image.open(output_filename)
    font = ImageFont.truetype('font/Montserrat/static/Montserrat-SemiBold.ttf', 100)
    small_font = ImageFont.truetype('font/Montserrat/static/Montserrat-SemiBold.ttf', 40)
    image_editable = ImageDraw.Draw(my_image)
    image_editable.text((1080, 270), f"€ {price}", (255, 255, 255), font=font)
    if old_price:
        image_editable.text((1080, 370), f"al posto di € {old_price}", (255, 255, 255), font=small_font)
    my_image.save(output_filename)

    return output_filename


if __name__ == '__main__':
    create_our_image("test_images/img1.jpg", template_name="generic_template.jpeg", price="9.99", old_price="1000")
    create_our_image("test_images/img2.jpg", template_name="fashion_template.jpeg", price="99.99", old_price="1000")
    create_our_image("test_images/img3.jpg", template_name="tech_template.jpeg", price="999.99", old_price="1000")
    create_our_image("test_images/img4.jpg", template_name="tech_template.jpeg", price="9999.99", old_price="1000")
