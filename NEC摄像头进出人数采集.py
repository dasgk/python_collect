import requests
from bs4 import  BeautifulSoup
import threading
import time

#需要监听的摄像头的ID
login_url_list = [];
login_url_list.append("http://192.168.0.236/cgi-bin/main.cgi")
##获得登陆的cookie
def get_login_cookie(login_url):
    post_data = {'userpass':'111111'}
    response = requests.post(login_url,data = post_data)
    cookies = response.cookies.get_dict()
    return cookies
##获得用户的进出人数
def get_in_and_out_num(cookie):
    monitor_url = "http://192.168.0.236/cgi-bin/monitor.cgi?body=yes&t=1520479502207"
    response = requests.get(monitor_url ,cookies=cookie)
    if response.text == "Session Error":
        main()
        return
    in_count = BeautifulSoup(response.text,"lxml").find("div",id="incount").text;
    if not  in_count:
        main()
    out_count = BeautifulSoup(response.text, "lxml").find("div", id="outcount").text;
    print("离开人数："+out_count  + "  进入人数：" + in_count+" 统计时间："+time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) )

##主函数
def main():
    for url in login_url_list:
        cookie = get_login_cookie(url)
        get_in_and_out_num(cookie)
    global  timer
    timer = threading.Timer(5, main)
    timer.start();
#定时器开启
timer = threading.Timer(0, main)
timer.start()




