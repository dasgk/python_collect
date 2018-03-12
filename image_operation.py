# -*- coding: utf-8 -*
import random
from PIL import Image,ImageDraw,ImageFont
ttfont = ImageFont.truetype("/C:\Windows\Fonts\STXINWEI.TTF",20)  #这里我之前使用Arial.ttf时不能打出中文，用华文细黑就可以
titles = ["哈哈","嘿嘿","嘚嘚",'呵呵']
im = Image.open("unknown.png")
width=1755
height=861
draw = ImageDraw.Draw(im)
for title in titles:
    x=random.randint(0, 1755)
    y = random.randint(0, 861)
    fillcolor = "#ff0000"
    draw.text((x,y),u'韩寒', fill=fillcolor,font=ttfont)
im.save("out.png","png")