import json
import re
import os
import requests
import urllib.request
from bs4 import BeautifulSoup
import pymysql.cursors
import pymysql

#讀取json檔案
f = open('./taipei-attractions.json',encoding = 'utf-8')
data = json.load(f)
len(data["result"]["results"]) #數據長度

# images_list_len = []
for i in range(len(data["result"]["results"])) :

    # 處裡圖片
    images = data["result"]["results"][i]["file"]
    images_change = images.replace("\/","/")
    images_list = re.findall( r'(http.*?.(.jpg|.JPG|.png|.PNG|.gif|.GIF))', images_change )
    
    images_list_all = []
    for j in range(len(images_list)) :
        if ".jpg" in images_list[j][0] :
            images_list_all.append(images_list[j][0])
        if ".JPG" in images_list[j][0] :
            images_list_all.append(images_list[j][0])
        if ".png" in images_list[j][0] :
            images_list_all.append(images_list[j][0])
        if ".PNG" in images_list[j][0] :
            images_list_all.append(images_list[j][0])
        else :
            continue
    
    #總結要送到資料庫的資料
    id = data["result"]["results"][i]["RowNumber"]
    name = data["result"]["results"][i]["stitle"]
    category = data["result"]["results"][i]["CAT2"]
    description = data["result"]["results"][i]["xbody"]
    address = data["result"]["results"][i]["address"].replace(" ","") # 處理 address 的空格
    transport = data["result"]["results"][i]["info"]
    mrt = data["result"]["results"][i]["MRT"]
    latitude = data["result"]["results"][i]["latitude"]
    longitude = data["result"]["results"][i]["longitude"]
    images_cut = images_list_all

    #儲存到mysql
    signup = pymysql.connect(
        host='localhost',
        user='root',
        password='rice1026', #記得改
        db='taipei',
        cursorclass=pymysql.cursors.DictCursor #以字典方式儲存
        )
    with signup.cursor() as cursor:
        mysqlact = "INSERT INTO taipeidata (id,name,category,description,address,transport,mrt,latitude,longitude,images) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(mysqlact,(id,name,category,description,address,str(transport),str(mrt),latitude,longitude,str(images_cut)))
        signup.commit() #資料上傳
    signup.close()
