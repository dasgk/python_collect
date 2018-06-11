# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import jieba
import re
from nltk.book import *
from pylab import *
mpl.rcParams['font.sans-serif'] = ['SimHei']
def stop_words():
    stop_word_list = []
    f = open('stopwords.txt', 'rU',encoding='UTF-8')
    for word in f:
        stop_word_list.append(word.strip())
    return stop_word_list

r = requests.get('https://blog.csdn.net/chszs/article/details/80629056')
soup = BeautifulSoup(r.text, 'lxml')
# 获得主要内容
context = soup.find('article').get_text()
# 进行结巴中文分词，获得字符串数组
word_list = jieba.cut(context)
word_list_str = (",".join(word_list))
word_list = re.split(",", word_list_str)
#去掉长度为1的单词，同时去掉停止词
stop_word_list = stop_words()
word_list = [w for w in word_list if (len(w)>1 and (w not in stop_word_list))]
word_freq_list = FreqDist(word_list)
word_freq_list.plot(30)