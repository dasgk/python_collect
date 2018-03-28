import sys
reload(sys)
sys.setdefaultencoding('utf8')
import requests
from bs4 import BeautifulSoup
import re

def get_qiushi_ids(html_str):
    id_list = []
    re1 = re.compile("qiushi_tag_\d*")
    result_list = re1.findall(html_str)
    for result in result_list:
        id_list.append(result)
    return id_list

main_url = "https://www.qiushibaike.com"
def get_content_list(main_url,unchange_url):
    response = requests.get(main_url)
    soup = BeautifulSoup(response.text, "lxml")
    ids = get_qiushi_ids(response.text)
    for id in ids:
        div = soup.find("div", attrs={'id':id})
        like_num = div.find("span", attrs={"class":"stats-vote"})
        if like_num is not None:
            like_num =like_num.find("i").text
        else:
            like_num = 0
        content = div.find("div", attrs={"class":"content"})
        pic_div = div.find("div", attrs={'class':"thumb"})
        img_src = ""
        if pic_div is not None:
            img = pic_div.find("img")
            if img is not None:
                img_src = img.get("src")
            else:
                img_src = ""
        print("id:"+ id+" like_num:"+str(like_num)+"  content:"+content.get_text()+"  img src:"+img_src)
    next_page = soup.find("span", attrs={"class":'next'})
    if next_page is not None:

        get_content_list(unchange_url+next_page.parent.get("href"), unchange_url)

get_content_list(main_url, main_url)
