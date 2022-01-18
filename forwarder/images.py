import math
import random
import string
from collections import namedtuple
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


Rectangle = namedtuple("Recangle", ['x', 'y', 'w', 'h'])
BoundingBox = namedtuple("BoundingBox", ['coords', 'area'])


def find_biggest_object(image_filename: str, threshold: int):
    img = cv2.imread(image_filename)
    _, thresh_gray = cv2.threshold(
        cv2.cvtColor(img, cv2.COLOR_BGR2GRAY),
        # thresh=234, # MisterCoupon
        # thresh=150, # SpaceCoupon
        thresh=threshold,
        maxval=255,
        type=cv2.THRESH_BINARY_INV
    )
    contours, _ = cv2.findContours(thresh_gray, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

    biggestBoundingBox = BoundingBox(coords=Rectangle(0, 0, 0, 0), area=0)
    for cont in contours:
        x, y, w, h = cv2.boundingRect(cont)
        area = w * h
        if area > biggestBoundingBox.area:
            biggestBoundingBox = BoundingBox(coords=Rectangle(x, y, w, h), area=area)

    return img[
          biggestBoundingBox.coords.y:biggestBoundingBox.coords.y + biggestBoundingBox.coords.h,
          biggestBoundingBox.coords.x:biggestBoundingBox.coords.x + biggestBoundingBox.coords.w
          ]


def create_our_image(image_filename: str, price: str, old_price: str, template_name: str = "template.png", ):
    img = cv2.imread(image_filename)
    scale_percent = 85
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)

    # resize image
    resized = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)

    template = cv2.imread(template_name)
    x_offset = 500 - int(math.floor(resized.shape[1] / 2))
    y_offset = int(math.floor(template.shape[0] / 2)) - int(math.floor(resized.shape[0] / 2)) + 70
    template[y_offset:y_offset + resized.shape[0], x_offset:x_offset + resized.shape[1]] = resized
    output_filename = ''.join(random.choices(string.ascii_letters, k=15)) + '.png'
    cv2.imwrite(output_filename, template)

    my_image = Image.open(output_filename)
    font = ImageFont.truetype('font/pricedown.otf', 100)
    small_font = ImageFont.truetype('font/pricedown.otf', 40)
    image_editable = ImageDraw.Draw(my_image)
    image_editable.text((1080, 270), f"€ {price}", (255, 255, 255), font=font)
    if old_price:
        image_editable.text((1080, 370), f"al posto di € {old_price}", (255, 255, 255), font=small_font)
    my_image.save(output_filename)

    return output_filename
