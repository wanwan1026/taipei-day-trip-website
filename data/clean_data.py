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

# #imgurl長度 
# len(images_list)
# print(images_list[i]][0]) 

# #將圖片存到本地資料夾(暫時用不到)
# header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36'}
# x=0
# for i in range(len(images_list)) :
#     if ".jpg" in images_list[i][0] :
#         response = requests.get(images_list[i][0],headers=header).content
#         file_name = position + "-" + str(x)
#         f = open("./images/%s.jpg" % x,'wb')
#         f.write(response)
#         f.close()
#         x+= 1
#         print("download successful" + str(x-1))
#     if ".JPG" in images_list[i][0] :
#         response = requests.get(images_list[i][0],headers=header).content
#         file_name = position + "-" + str(x)
#         f = open("./images/%s.jpg" % x,'wb')
#         f.write(response)
#         f.close()
#         x+= 1
#         print("download successful" + str(x-1))
#     if ".png" in images_list[i][0] :
#         response = requests.get(images_list[i][0],headers=header).content
#         file_name = position + "-" + str(x)
#         f = open("./images/%s.jpg" % x,'wb')
#         f.write(response)
#         f.close()
#         x+= 1
#         print("download successful" + str(x-1))
#     if ".PNG" in images_list[i][0] :
#         response = requests.get(images_list[i][0],headers=header).content
#         file_name = position + "-" + str(x)
#         f = open("./images/%s.jpg" % x,'wb')
#         f.write(response)
#         f.close()
#         x+= 1
#         print("download successful" + str(x-1))
#     else :
#         continue



# #可以用
# data_dict = dict([
#     ("id",i),
#     ("name",name),
#     ("category",category),
#     ("description",description),
#     ("address",address_cut),
#     ("transport",transport),
#     ("mrt",mrt),
#     ("latitude",latitude),
#     ("longitude",longitude),
#     ("images",[images_list[0][0]])
# ])
# # print(data_dict)    


# #成功
# # 圖片網頁網址
# print(images_list[0][0])

# images = data["result"]["results"][71]["file"]
# position = data["result"]["results"][71]["RowNumber"]
# images_change = images.replace("\/","/")
# images_list = re.findall( r'(http.*?.(.jpg|.JPG|.png|.PNG|.gif|.GIF))', images_change )

# header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36'}
# response = requests.get(images_list[0][0],headers=header).content
# j = 0
# x = position + "-" + str(j)
# f = open("./images/%s.jpg" % x,'wb')
# f.write(response)
# f.close()
# print("download successful")

#失敗
# header = {
#     'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36'
# }
# imgurl = images_list
# def get_img(imgurl):
#     response = requests.get(imgurl,headers=header).content
#     f = open(open(name + ".jpg", 'wb'))
#     f.write(response)
#     f.close

#失敗
# print("正在下載: %s" % images_list[0][0])
# img_save_path = "./images%s.png" % position
# urllib.request.urlretrieve(images_list[0][0],"D:\images")

#失敗
# for j in range(len(images_list)):
#     try :
#         print("正在下載: %s" % images_list[j])
#         img_save_path = "./images%d.png" % i+"-"+x
#         urllib.request.urlretrieve(images_list[j],"D:\images")
#         x+= 1
#     except :
#         continue
# pass

# x=0
# for i in range(len(images_list)) :
#     if "gif" in images_list[i]:
#         continue
#     if "GIF" in images_list[i]:
#         continue
#     if "png" in images_list[i]:
#         print(images_list[i])
#     if "PNG" in images_list[i]:
#         print(images_list[i])
#     if "jpg" in images_list[i] :
#         print(images_list[i])
#     if "JPG" in images_list[i] :
#         print(images_list[i])
#     else :
#         continue

# 迴圈內部還未完成(用不到了)
# for i in range(len(data2)):
#     id = i+1
#     name = data["result"]["results"][i]["stitle"]
#     category = data["result"]["results"][i]["CAT2"]
#     description = data["result"]["results"][i]["xbody"]
#     address = data["result"]["results"][i]["address"]
#     transport = data["result"]["results"][i]["info"]
#     mrt = data["result"]["results"][i]["MRT"]
#     latitude = data["result"]["results"][i]["latitude"]
#     longitude = data["result"]["results"][i]["longitude"]
#     images = data["result"]["results"][i]["file"]
#     position = data["result"]["results"][i]["RowNumber"]
#     data_dict = dict([()])
#     print(data3)

# #測試用
# a = "今天天氣晴，我想要吃蛋餅，為甚麼我想要吃蛋餅?因為有很多字跟蛋餅押韻~" 
# c1 = a.split("，")
# c2 = c1[0] + "，" + c1[1]
# print(c2)

# #測試用
# a = "http:\/\/www.travel.taipei\/d_upload_ttn\/sceneadmin\/image\/A0\/B0\/C1\/D494\/E228\/F635\/62f91bcd-de9c-4873-a34b-13b27c304d61.jpghttp:\/\/www.travel.taipei\/d_upload_ttn\/sceneadmin\/image\/A0\/B0\/C2\/D50\/E48\/F798\/a86af5f8-5f6d-4d37-ab17-f130b786c9c8.jpghttp:\/\/www.travel.taipei\/d_upload_ttn\/sceneadmin\/image\/A0\/B0\/C0\/D31\/E705\/F571\/c0b808c1-2282-4dba-9c4c-866f66d9a611.JPGhttp:\/\/www.travel.taipei\/d_upload_ttn\/sceneadmin\/image\/A0\/B0\/C0\/D0\/E197\/F490\/889da51b-2574-44ff-8193-7540c6faf900.JPGhttp:\/\/www.travel.taipei\/d_upload_ttn\/sceneadmin\/image\/A0\/B0\/C0\/D0\/E197\/F491\/9affe4c4-1d52-488c-a6c4-59635ffd2d2b.JPG"
# a = a.replace("\/","/")
# b = 'http.*?\.jpg' 
# c = 'http.*?\.JPG'
# c1 = re.findall( r'http.*?\.jpg|http.*?\.JPG|http.*?\.png|http.*?\.PNG' , a )
# C2 = re.findall( c , a )
# # print(b)
# print(c1)
# # print(C2)

