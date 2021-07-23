import os

from io import BytesIO

import requests

from PIL import Image, ImageDraw, ImageFont
from cairosvg import svg2png

TEMPLATE_PATH = os.path.abspath('files/ticket_base.png/')
FONT_PATH = os.path.abspath('files/Roboto-Regular.ttf/')
FONT_SIZE = 20

BLACK = (0, 0, 0, 225)
NAME_OFFSET = (270, 125)
EMAIL_OFFSET = (280, 150)

AVATAR_SIZE = 150
AVATAR_OFFSET = (50, 100)


def generate_ticket(name, email):
    with Image.open(TEMPLATE_PATH).convert("RGBA") as base:
        font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
        draw = ImageDraw.Draw(base)
        draw.text(NAME_OFFSET, name, font=font, fill=BLACK)
        draw.text(EMAIL_OFFSET, email, font=font, fill=BLACK)

        response = requests.get(url=f'https://avatars.dicebear.com/api/male/{AVATAR_SIZE}/{email}.svg/')
        if response.status_code == 200:
            avatar_file = BytesIO()
            avatar_file_like = svg2png(bytestring=response.content, write_to=avatar_file)

            avatar = Image.open(avatar_file_like)

            base.paste(avatar, AVATAR_OFFSET)

        temp_file = BytesIO()
        base.save(temp_file, 'png')
        temp_file.seek(0)

        return temp_file
