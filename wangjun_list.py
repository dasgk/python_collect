# -*- coding: utf-8 -*
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import requests
import json
import wangjun
import time

url ="https://pc-shop.xiaoe-tech.com/appgp6EDV1w6936/open/column.resourcelist.get/2.0"
request_data_list_headers = {
 "Accept":"*/*",
"Accept-Encoding":"gzip, deflate, br",
"Accept-Language":"zh-CN,zh;q=0.8",
"Connection":"keep-alive",
"Content-Length":"277",
"Content-Type":"application/x-www-form-urlencoded",
"Cookie":"tgw_l7_route=4ed04efd1969357f144e2696012a8c35; laravel_session=eyJpdiI6IlpmR3FJblZpMlU1T0tNelpIRktEUmc9PSIsInZhbHVlIjoiWnBReGZKZ2w0ZkFxbHcxcXlXcFA2N2w3aEJoK2tFYnZDOGo3TVNSVmxRUDZNS1ZTSmdmSGtCVWIyTXgwZTFaM1Z4cDQ1V2FwdE1Xb3V5eEJkYnEreFE9PSIsIm1hYyI6IjdmNDJmOTllMDg2OTIyZTlmZWE5NzgxMWFkM2ZiMjExYjgwYzRhMDFmZGYwOWI2NzRkM2Y4NzhmYjkzODEwOTYifQ%3D%3D",
"Host":"pc-shop.xiaoe-tech.com",
"Origin":"https://pc-shop.xiaoe-tech.com",
"Referer":"https://pc-shop.xiaoe-tech.com/appgp6EDV1w6936/columnist_detail?id=p_5a98c01c490cc_NGnnmhAC",
"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36",
    "X-Requested-With":"XMLHttpRequest"
}
data_list_post_data ="data%5Bpage_index%5D=0&data%5Bpage_size%5D=100&data%5Border_by%5D=start_at%3Adesc&data%5Bresource_id%5D=p_5a98c01c490cc_NGnnmhAC&data%5Bstate%5D=0&data%5Bresource_types%5D%5B%5D=1&data%5Bresource_types%5D%5B%5D=2&data%5Bresource_types%5D%5B%5D=3&data%5Bresource_types%5D%5B%5D=4"
response = requests.post(url,data= data_list_post_data, headers=request_data_list_headers)
json_data = json.loads(response.text)
json_data = json_data['data']
for data in json_data:
    print("正在处理"+ data['title'])
    resource_id = data['id']
    title = data['title']
    wangjun.download_all_files(resource_id, title)
    make_new_m3u8(resource_id,title)
    print( title+"处理完成")
    time.sleep(10)


