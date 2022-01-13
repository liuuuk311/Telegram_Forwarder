import math
import random
import string
from collections import namedtuple
from typing import Optional

import cv2
import requests

DEFAULT_DOWNLOADED_IMAGE = "tmp.jpg"


def download_image(url: str) -> Optional[str]:
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


def create_our_image(image_filename: str, threshold: int, template_name: str = "template.png"):
    img = find_biggest_object(image_filename, threshold)
    template = cv2.imread(template_name)
    x_offset = int(math.floor(template.shape[1] / 2)) - int(math.floor(img.shape[1] / 2))
    y_offset = int(math.floor(template.shape[0] / 2)) - int(math.floor(img.shape[0] / 2))
    template[y_offset:y_offset + img.shape[0], x_offset:x_offset + img.shape[1]] = img
    output_filename = ''.join(random.choices(string.ascii_letters, k=15)) + '.png'
    cv2.imwrite(output_filename, template)
    return output_filename


if __name__ == '__main__':
    # test_img = [
    #     "https://images.zbcdn.ovh/images/1099842631/1641827714699.jpg",
    #     "https://images.zbcdn.ovh/images/1099842631/1641823116937.jpg",
    #     "https://images.zbcdn.ovh/images/1099842631/1641724506467.jpg",
    #     "https://images.zbcdn.ovh/images/1099842631/1641723985825.jpg",
    #     "https://images.zbcdn.ovh/images/1099842631/1641882678308.jpg",
    #     "https://images.zbcdn.ovh/images/1099842631/1641882618896.jpg",
    #     "https://images.zbcdn.ovh/images/1099842631/1641882283051.jpg",
    #     "https://images.zbcdn.ovh/images/1099842631/1641882070306.jpg"
    # ]
    # for url in test_img:
    #     create_our_image(download_image(url), is_debug=True)

    create_our_image("./t1.jpeg", is_debug=True, threshold=150)
