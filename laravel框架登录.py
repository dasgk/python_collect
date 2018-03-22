# -*- coding: utf-8 -*-
import scrapy
import requests
from bs4 import BeautifulSoup
from PIL import Image,ImageDraw,ImageFont
cookie_str=''
cxrf= ''
def get_csrf(value_list):
    response = requests.get("http://192.168.10.158:8302/admin/login")
    session_headers = response.headers
    for item in session_headers:
        if item == 'Set-Cookie':
            value_list[0] = session_headers[item] + ";"+value_list[0]
    soup = BeautifulSoup(response.text, "lxml")
    value_list[1] =soup.find(attrs={"name": "_token"})['value']
    value_list[0] = value_list[0].replace('hd_session',';hd_session')

def get_capatch(value_list):
    response = requests.get('http://192.168.10.158:8302/cpt/show?r=12332',headers={
           'Cookie':value_list[0]
    })
    session_headers = response.headers
    for item in session_headers:
        if item == 'Set-Cookie':
            value_list[0] = session_headers[item] + ";" + value_list[0]
    with open('captcha.png', 'wb') as f:
        f.write(response.content)
        f.close()
    try:
       im = Image.open('captcha.png')
       im.show()
       im.close()
    except:
       pass
    captcha = input("请输入你的验证>")
    return captcha

def handle(username, password):
    value_list = ['',''];
    value_list[0] = '';
    value_list[1] = '';
    get_csrf(value_list)
    captcha = get_capatch(value_list)
    response = requests.post(url='http://192.168.10.158:8302/admin/login',headers={
              'Cookie':value_list[0]
           },data={
                "_token": value_list[1],
                "username": username,
                'password': password,
                'captcha': captcha
            })
    soup = BeautifulSoup(response.text, 'lxml')
    span = soup.find('span',attrs={'class':'help-block'})
    if span is None:
        print('登录成功')
    else:
        print(span.strong.text)
        if span.strong.text == '用户名或密码错误':
            return
        else:
            handle(username, password)
handle('admin', '111111')