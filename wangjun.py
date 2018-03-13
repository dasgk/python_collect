# -*- coding: utf-8 -*
import sys
reload(sys)
sys.setdefaultencoding('utf8')
# http://pc-shop.xiaoe-tech.com/appgp6EDV1w6936/video_details?id=v_5a9fb7291b264_wnQueZNO
# 根据id值获得m3u8文件
# 解析m3u8文件获得ts链接数组
# 下载ts文件
# 下载后的ts文件是加密的，需要根据key进行解密
# 使用ffmpeg将所有解密后的文件进行合成mp4文件
# 将mp4文件移动到指定路径
import requests
from bs4 import BeautifulSoup
import json
import random
import time
import os
import codecs

url = "https://pc-shop.xiaoe-tech.com/appgp6EDV1w6936/open/video.detail.get/1.0"

#data = dict(data=dict(resource_id="v_5a98b07dc7dda_ll3Y48cv"))

request_m3u8_url_headers = {
"Accept":"*/*",
"Accept-Encoding":"gzip, deflate",
"Accept-Language":"zh-CN,zh;q=0.9",
"Cache-Control":"no-cache",
"Connection":"keep-alive",
"Content-Length":"46",
"Content-Type":"application/x-www-form-urlencoded",
"Host":"pc-shop.xiaoe-tech.com",
"Origin":"http://pc-shop.xiaoe-tech.com",
"Cookie":"tgw_l7_route=4ed04efd1969357f144e2696012a8c35; laravel_session=eyJpdiI6IlpmR3FJblZpMlU1T0tNelpIRktEUmc9PSIsInZhbHVlIjoiWnBReGZKZ2w0ZkFxbHcxcXlXcFA2N2w3aEJoK2tFYnZDOGo3TVNSVmxRUDZNS1ZTSmdmSGtCVWIyTXgwZTFaM1Z4cDQ1V2FwdE1Xb3V5eEJkYnEreFE9PSIsIm1hYyI6IjdmNDJmOTllMDg2OTIyZTlmZWE5NzgxMWFkM2ZiMjExYjgwYzRhMDFmZGYwOWI2NzRkM2Y4NzhmYjkzODEwOTYifQ%3D%3D",
"Pragma":"no-cache",
"Referer":"http://pc-shop.xiaoe-tech.com/appgp6EDV1w6936/video_details?id=v_5a9fb7291b264_wnQueZNO",
"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36",
"X-Requested-With":"XMLHttpRequest"
}

download_m3u8_url_header={
"Accept":"*/*",
"Accept-Encoding":"gzip, deflate",
"Accept-Language":"zh-CN,zh;q=0.9",
"Cache-Control":"no-cache",
"Connection":"keep-alive",
"Host":"vod2.xiaoe-tech.com",
"Pragma":"no-cache",
"Referer":"http://pc-shop.xiaoe-tech.com/appgp6EDV1w6936/video_details?id=v_5a9fb7291b264_wnQueZNO",
"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36",
"X-Requested-With":"ShockwaveFlash/28.0.0.161"
}

download_ts_header = {
"Accept":"*/*",
"Accept-Encoding":"gzip, deflate",
"Accept-Language":"zh-CN,zh;q=0.9",
"Cache-Control":"no-cache",
"Connection":"keep-alive",
"Host":"vod2.xiaoe-tech.com",
"Pragma":"no-cache",
"Referer":"http://pc-shop.xiaoe-tech.com/appgp6EDV1w6936/video_details?id=v_5a9fb7291b264_wnQueZNO",
"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36",
"X-Requested-With":"ShockwaveFlash/28.0.0.161"
}
# 找到字符串中特定字符最后一次出现的位置
def get_last_char_position(string, str):
    last_position = -1
    while True:
        position = string.find(str, last_position + 1)
        if position == -1:
            return last_position
        last_position = position

#获得hls下载地址的后半部分的数组
def get_ts_url_list(str):
    mm = str.split("\n")
    row_index = 1
    ts_list = []
    for per_row in mm:
        if row_index>=7:
            if (row_index-7)%3==0:
                # 这里是ts文件的地址
                ts_list.append(per_row)
        row_index = row_index+1
    return ts_list

def get_key_list(content, title):
    mm = content.split("\n")
    row_index = 1
    key_list = []
    key_index = 0
    for per_row in mm:
        if row_index >= 5:
            if (row_index - 5) % 3 == 0:
                # 这里是ts文件的地址
                begin_position = per_row.find("URI=\"")
                if begin_position == -1:
                    break;
                begin_position = begin_position+len("URI=\"")
                end_position = per_row.find("\"", begin_position)
                new_url = per_row[begin_position:end_position]
                #不存在key才下载
                if not os.path.exists(title+"/"+str(key_index)+".key"):
                    #也不存在解密后的key文件
                    if not os.path.exists(title+"/media_decryptd_"+str(key_index)+".ts"):
                        r = requests.get(new_url)
                        with open(title+"/"+str(key_index)+".key", "wb") as code:
                            code.write(r.content)
                key_index = key_index+1
        row_index = row_index + 1
    return key_list

#获得m3u8文件下载地址
def get_m3u8_url(resource_id):
    response = requests.post(url, data="data[resource_id]=" + resource_id, headers=request_m3u8_url_headers)
    m3u8_json_data = json.loads(response.text)
    if not m3u8_json_data['data']:
        return
    if not m3u8_json_data['data']['video_hls']:
        return
    hls_url = m3u8_json_data['data']['video_hls']
    return hls_url

def get_m3u8_content(filename):
    fd = codecs.open(filename)
    content = fd.read()
    fd.close()
    return content

#获得ts文件下载地址前缀
def get_ts_prefix_url(hls_url):
    # 获得hls_url 的链接前缀
    prefix_position = get_last_char_position(hls_url, '/')
    ts_url_prefix = hls_url[0:prefix_position + 1]
    return ts_url_prefix

def download_all_files(resource_id, title):
    hls_url = get_m3u8_url(resource_id)
    if not hls_url:
        return
    print("m3u8 link：" + hls_url)
    #创建需要的目录
    if not os.path.exists(title):
        os.makedirs(title)
    file_name = title+"/key.m3u8"
    if not os.path.exists(file_name):
        print("开始下载m3u8文件")
        r = requests.get(hls_url, headers=download_m3u8_url_header)
        with open(file_name, "wb") as code:
            code.write(r.content)
    print("m3u8文件下载成功")
    content = get_m3u8_content(file_name)
    print("开始写入key文件")
    key_list = get_key_list(content, title)
    print("key文件写入成功")
    ts_url_prefix = get_ts_prefix_url(hls_url)
    ts_list = get_ts_url_list(content)
    file_count = len(ts_list)
    print("共需下载"+str(file_count)+"个文件")
    file_index = 0
    for item in ts_list:
        ts_download_url = ts_url_prefix+item
        #不存在加密后的ts文件才进行下载
        if not os.path.exists(title+"/"+str(file_index)+".ts"):
            #也不存在解密后的ts文件才进行下载
            if not os.path.exists(title+"/media_decryptd_"+str(file_index)+".ts"):
                r = requests.get(ts_download_url, headers=download_ts_header)
                print("正在下载第"+str(file_index)+"个文件")
                with open(title+"/"+str(file_index)+".ts", "wb") as code:
                    code.write(r.content)
        #print("第" + str(file_index) + "个文件下载完成")
        file_index = file_index+1
    #将ts文件进行解密，合成mp4文件
    get_new_ts_list(title, len(ts_list))

def get_new_ts_list(title,length):

    title_1 = title.replace(" ","\ ")
    cd_command = "cd " + title_1
    file_name = title.replace(" ", "")
    #删除该目录下所有的mp4文件
    os.popen(cd_command+" && rm -rf *.mp4")
    # 如果文件存在，则不进行操作
        if os.path.exists(file_name + ".mp4"):
            return
    ffmpeg_command = cd_command + " && "
    ffmpeg_command += " ffmpeg -i \"concat:"
    num_list = range(length)
    for index in num_list:
        #如果存在解密后的ts文件则本次不执行
        if not os.path.exists(title+"/media_decryptd_"+str(index)+".ts"):
            str_dump = cd_command+" && "+ "hexdump -v -e  '16/1 \"%02x\"' "
            str_dump = str_dump +str(index)+".key"
            decrpy_data = os.popen(str_dump).readline()
            openss_command = cd_command+" && "+"openssl aes-128-cbc -d -in "+str(index)+".ts -out "+"media_decryptd_"\
                         +str(index)+".ts -nosalt -iv 00000000000000000000000000000000 -K "+str(decrpy_data)
            os.popen(openss_command)
        #说明对应的key文件已经存在,进行删除
        os.popen(cd_command + " && rm -rf " + str(index) + ".key")
        #加密后的ts文件也可以删除
        os.popen(cd_command+" && rm -rf "+str(index)+".ts")
        #调用ffmpeg进行视频的生成
        ffmpeg_command += "media_decryptd_"+str(index)+".ts|"
    ffmpeg_command = ffmpeg_command[0:len(ffmpeg_command)-1]
    ffmpeg_command += "\""

    ffmpeg_command = ffmpeg_command+" -c copy -bsf:a aac_adtstoasc ../"+file_name+".mp4"
    print(ffmpeg_command)
    os.popen(ffmpeg_command)
    #删除解密后的ts文件，还是手动删除吧，部分视频可能第一次合成失败
    '''
    for index in num_list:
        if os.path.exists(title+"/media_decryptd_"+str(index)+".ts"):
            os.remove(title+"/media_decryptd_"+str(index)+".ts")
    '''
