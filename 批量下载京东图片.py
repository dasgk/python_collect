import requests
from bs4 import  BeautifulSoup
import re
url = "https://search.jd.com/Search?keyword=%E6%89%8B%E6%9C%BA&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&suggest=1.def.0.V12&wq=s&cid2=653&cid3=655&s=56&click=0"
def get_imgs(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    select_imgs = soup.find_all("img", attrs={"class":"err-product"})
    imgs_list = []
    for img in select_imgs:
        current_img = img.get('src')
        if not current_img:
            current_img = img.get("data-lazy-img")
        if current_img is not None:
            imgs_list.append(current_img[2:])
    return imgs_list

max_page = 100
page_list = range(1,max_page)
pattern = "\w*.jpg"
pattern = re.compile(pattern)
for page in page_list:
    current_url = url+"&page="+str(page)
    imgs = get_imgs(current_url)
    for img in imgs:
        search = re.search(pattern,img)
        file_name = search.group(0)
        h_file = requests.get("https://"+img)
        with open(file_name, "wb") as f_handle:
            f_handle.write(h_file.content)




