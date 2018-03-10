# url  超品相师专辑的URL  http://www.ximalaya.com/4932085/album/3160816/
# 获得sound_id 然后  album_soundlist中ul的li的sound_id就是每个音频的ID
# 进行拼接URL  http://www.ximalaya.com/tracks/73528737.json  当然数字就是sound_id了
# 然后解析json中的play_path的值，进行下载即可
import requests
from bs4 import BeautifulSoup
ablum_url = "http://www.ximalaya.com/4932085/album/3160816/"
import json

file_index = 1 #文件名称
page_index = 20
header = {
"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
"Accept-Encoding":"gzip, deflate",
"Accept-Language":"zh-CN,zh;q=0.9",
"Cache-Control":"no-cache",
"Connection":"keep-alive",
"Host":"www.ximalaya.com",
"Pragma":"no-cache",
"Upgrade-Insecure-Requests":"1",
"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36"
}

def get_audio_download_url(sound_id, page_index):
    url = "http://www.ximalaya.com/tracks/"+sound_id+".json"
    response = requests.get(url,None,headers = header)
    jsons = json.loads(response.text)
    download_url = jsons['play_path']
    file_name = str(sound_id)+".m4a"
    r = requests.get(download_url)
    with open(file_name, "wb") as code:
        code.write(r.content)
    return

def get_sound_list(url, header,  page_index):
    sound_id_list = []
    response = requests.get(url,None, headers=header)
    soup = BeautifulSoup(response.text, "lxml")
    div = soup.find('div', class_= 'album_soundlist ')
    if not div:
        return
    if not div.ul:
        return
    div = div.ul.find_all('li')
    #获得该专辑下所有的sound_id进行下载
    if not div:
        return
    for item in div:
        sound_id = item['sound_id']
        get_audio_download_url(sound_id, page_index)
    #进行下一页的操作
    print("第"+str(page_index)+"页 下载完成")
    page_index = page_index+1
    current_url = ablum_url +"?page=" + str(page_index)
    get_sound_list(current_url,header,page_index)
current_url = ablum_url +"?page=" + str(page_index)
get_sound_list(current_url,header,  page_index)