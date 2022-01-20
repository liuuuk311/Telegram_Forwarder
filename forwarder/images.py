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


def image_resize(image, width=None, height=None, inter=cv2.INTER_AREA):
    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = image.shape[:2]

    # if both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return image

    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        r = height / float(h)
        dim = (int(w * r), height)

    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # return the resized image
    return cv2.resize(image, dim, interpolation=inter)


def create_our_image(image_filename: str, price: str, old_price: str, template_name: str = "template.png"):
    img = cv2.imread(image_filename, cv2.IMREAD_UNCHANGED)
    if img.shape[0] > img.shape[1]:
        img = image_resize(img, height=700)
    else:
        img = image_resize(img, width=1000)

    template = cv2.imread(template_name, cv2.IMREAD_UNCHANGED)
    x_offset = max(500 - int(math.floor(img.shape[1] / 2)), 0)
    y_offset = max(int(math.floor(template.shape[0] / 2)) - int(math.floor(img.shape[0] / 2)) + 100, 0)
    template[y_offset:y_offset + img.shape[0], x_offset:x_offset + img.shape[1]] = img
    output_filename = ''.join(random.choices(string.ascii_letters, k=15)) + '.png'
    cv2.imwrite(output_filename, template)

    my_image = Image.open(output_filename)
    font = ImageFont.truetype('font/Montserrat/static/Montserrat-SemiBold.ttf', 100)
    small_font = ImageFont.truetype('font/Montserrat/static/Montserrat-SemiBold.ttf', 40)
    image_editable = ImageDraw.Draw(my_image)
    image_editable.text((1090, 270), f"{price}", (255, 255, 255), font=font)
    if old_price:
        image_editable.text((1090, 370), f"al posto di {old_price}", (255, 255, 255), font=small_font)
    my_image.save(output_filename)

    return output_filename


if __name__ == '__main__':
    from utils import get_amazon_image_from_page
    urls = [
        "https://www.amazon.it/dp/B07Z9M6VL6/?tag=jikemaster-21&psc=1",
    ]
    for url in urls:
        img_url = download_image(get_amazon_image_from_page(url))
        create_our_image(img_url, template_name="generic_template.jpeg", price="9.99", old_price="1000")
