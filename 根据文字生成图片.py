# -*- coding: utf-8 -*
import random
from PIL import Image,ImageDraw,ImageFont
ttfont = ImageFont.truetype("/C:\Windows\Fonts\STXINWEI.TTF",20)  #这里我之前使用Arial.ttf时不能打出中文，用华文细黑就可以
titles = ["哈哈","嘿嘿","乐乐","呵呵","得了吧","神兽"]
weight = [1,1.5,2,2.5,2.7,3]
base_img = Image.open("background.png")  # 778*778
width = 778
height = 778
step = 50
key = 0;
for title in titles:
    #每次使用空白的背景图片，在上边写上字之后进行旋转，然后crop裁剪出包含旋转的字的部分图片
    bk_im = Image.open("background.png")
    draw = ImageDraw.Draw(bk_im)
    fillcolor = "#ff0000"
    rand_num = random.randint(0,360)
    ttfont = ImageFont.truetype("/C:\Windows\Fonts\STXINWEI.TTF", 20*int(weight[key]))  # 这里我之前使用Arial.ttf时不能打出中文，用华文细黑就可以
    draw.text((width/2, height/2), title, fill=fillcolor, font=ttfont)
    rand_rotate = random.randint(0,360)
    bk_im = bk_im.rotate(rand_rotate)
    center_left = width/2
    center_top = height / 2
    current_step = step*(int(weight[key]))
    box = (center_left-current_step,center_top-current_step,center_left+current_step,current_step+center_top)
    # 可以粘贴在目标文件上的图片块
    select_im = bk_im.crop(box)
    rand_left = random.randint(0,width/2)
    rand_top = random.randint(0, height/2)
    #将裁剪出的图片放在目标文件的随机位置上即可
    base_im = base_img.paste(select_im,(rand_left, rand_top,rand_left+2*current_step, rand_top+2*current_step))
    base_img.save("content.png")

    key = key+1
base_img = Image.open("content.png")
base_img.show();
base_img.close()