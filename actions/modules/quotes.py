import numpy as np
from PIL import Image, ImageFont, ImageDraw
import io, base64, os
import random

def get_base64(quote):
    img = write_image(quote)
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    img = base64.b64encode(buf.getvalue()).decode('utf-8')
    return img

def select_background_image():
    path = "assets/images/"
    options = os.listdir(path)
    return path + random.choice(options)

def select_font():
    prefix = "assets/fonts/"
    options = os.listdir(prefix)
    return prefix + random.choice(options)

def recommend_font_size(text):
    size = 50
    l = len(text)
    resize_heuristic = 0.9
    resize_actual = 0.985
    while l > 1:
        l = l * resize_heuristic
        size = size * resize_actual
    return int(size)

def wrap_text(text, w=30):
    new_text = ""
    new_sentence = ""
    for word in text.split(" "):
        delim = " " if new_sentence != "" else ""
        new_sentence = new_sentence + delim + word
        if len(new_sentence) > w:
            new_text += "\n" + new_sentence
            new_sentence = ""
    new_text += "\n" + new_sentence
    return new_text


def write_image(text):
    text = wrap_text(text)
    font_size = recommend_font_size(text)
    image = select_background_image()
    font = select_font()
    img = Image.new("RGBA", (480, 360), (255, 255, 255))
    back = Image.open(image, 'r')
    img.paste(back)
    font = ImageFont.truetype(font, font_size)
    draw = ImageDraw.Draw(img)
    img_w, img_h = img.size
    x = img_w / 2
    y = img_h / 2
    textsize = draw.multiline_textsize(text, font=font, spacing=3)
    text_w, text_h = textsize
    x -= text_w / 2
    y -= text_h / 2
    draw.multiline_text(align="center", xy=(x, y), text=text, fill=(255,255,255), font=font, spacing=3)
    draw = ImageDraw.Draw(img)
    return img

if __name__ == "__main__":
    print(get_base64("heya ......"))


