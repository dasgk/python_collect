#获得酷狗top500 的信息
import requests
from bs4 import BeautifulSoup
url = "http://www.kugou.com/yy/rank/home/"
rank = 1
page_list = range(1,23);
for page_index in page_list:
    current_url = url+str(page_index)+"-8888.html?from=rank"
    response = requests.get(current_url)
    soup = BeautifulSoup(response.text,"lxml")
    ranks = soup.select('.pc_temp_num')
    times = soup.select('.pc_temp_time')
    titles = soup.select('.pc_temp_songlist > ul > li > a ')
    for title, rank,time in zip(titles, ranks,times):
        singer = title.get_text().split("-")[0].strip()
        song_title = title.get_text().split("-")[1].strip()
        print("rank: "+rank.text.strip()+"  singer :"+singer+"  title:"+song_title+" time:"+time.text.strip())
