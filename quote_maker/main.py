#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 10 21:22:20 2017

@author: shajeen ahamed
"""

from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw

import sys
import textwrap
import uuid
import random
import os

# quote font
here = os.path.dirname(os.path.abspath(__file__))
system_font = os.path.join(here,"fonts/Quote.ttf")
# font size
system_font_size = 50

# image type
image_type = "RGBA"

# image size
image_size_x = 1200 # x
image_size_y = 600  # y

# background color
colors = [(255,0,0), (51, 0, 51), (0,0,255), (0,0,0)]

# facebook settings
page_id = 00000000000000    # page id
facebook_token = ""	    # access_token

def alingText(text_size, text):
    wrapper = textwrap.TextWrapper(width = system_font_size) #*3
    text_element = wrapper.wrap(text = text)
    return text_element

def centerPixel(strlen, line_no):
    temp = []
    x = image_size_x / 2
    y = image_size_y / 2
    t = (strlen * system_font_size) / 5 #4
    temp.append(x - t)
    temp.append(y - (system_font_size * line_no))
    return temp

def createImage(text, image_name, logo):
    fonts = ImageFont.truetype(system_font, system_font_size)
    system_color = random.choice(colors)
    img = Image.new(image_type, (image_size_x, image_size_y), (system_color[0], system_color[1], system_color[2]))
    draw = ImageDraw.Draw(img)
    text_element = alingText(fonts.getsize(text), text)
    line = len(text_element)/2
    for element in text_element:
        points = centerPixel(len(element), line)
        draw.text((points[0], points[1]), element, (255, 255, 255), font=fonts)
        draw = ImageDraw.Draw(img)
        line = line - 1.5
    draw.text((10,10), logo, (255,255,255), font=fonts)
    img.save(image_name)

def main():
    #########################################
    print (100 * "*")
    print ("~~~ quote_maker.py ~~~")

    # read quote
    quote_text = str(input("quote: "))
    # create unique name
    image_name = '{name}.png'.format(name = str(uuid.uuid4()))
    logo = "Publish by, " + "-MyPage-"
    
    # create an image
    createImage(quote_text, image_name, logo)
    
    # post on facebook
    command = "curl -F 'access_token={access_token}' -F 'source=@{image_path}' -F 'method=post' -F 'message={message}' 'https://graph.facebook.com/{page_id}/photos'".format(
    access_token = facebook_token,
    image_path = image_name,
    message = logo,
    page_id = page_id)
    print("Generated curl commnad:")
    print(command)
    #os.system(command)
