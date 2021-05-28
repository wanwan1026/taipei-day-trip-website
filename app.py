from math import nan
from flask import *
app=Flask(__name__)
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True

# import mysql.connector
import pymysql.cursors
import pymysql
# from flask import jsonify
import json
# import urllib.request as request

import datetime
import random

import requests


app = Flask(__name__,static_folder="static",static_url_path="/")
app.config['SECRET_KEY'] = 'ricetia' 

@app.route("/")
def index():
	return render_template("index.html")
@app.route("/attraction/<id>")
def attraction(id):
	return render_template("attraction.html")
@app.route("/booking")
def booking():
	return render_template("booking.html")
@app.route("/thankyou")
def thankyou():
	return render_template("thankyou.html")

@app.route("/api/attractions")
def attractions():
	page = (request.args.get("page",""))
	keyword = (request.args.get("keyword","",))
	keyword = keyword.replace('\"','')
	
	signup = pymysql.connect(
		host='localhost',
		user='root',
		password='RICETIA', #記得改
		db='taipei',
		cursorclass=pymysql.cursors.DictCursor
		)
	with signup.cursor() as cursor:
		mysqlact = "SELECT * FROM `taipeidata`"
		cursor.execute(mysqlact,)
		result_page = cursor.fetchall()
	signup.close()

	if page != "" :
		if page.isdigit() == False :
			error = {"error": "true" , "message":"查無項目"}
			return error
		if len(result_page) % 12 == 0 :
			if int(page) in range(0,len(result_page) // 12 ) :
				page = int(page)
			else :
				error = {"error": "true" , "message":"查無項目"}
				return error
		if len(result_page) % 12 != 0 :
			if int(page) in range(0,len(result_page) // 12 + 1 ) :
				page = int(page)
			else :
				error = {"error": "true" , "message":"查無項目"}
				return error
		else :
			error = {"error": "true" , "message":"查無項目"}
			return error
			

	if keyword != "" :
		signup = pymysql.connect(
			host='localhost',
			user='root',
			password='RICETIA', #記得改
			db='taipei',
			cursorclass=pymysql.cursors.DictCursor
			)
		with signup.cursor() as cursor:
			mysqlact = "SELECT * FROM `taipeidata` WHERE position(%s in `name`)"
			cursor.execute(mysqlact,keyword)
			result_keyword = cursor.fetchall()
		signup.close()

		if len(result_keyword) == 0 :
			error = {"error": "true" , "message":"查無項目"}
			return error
	
	if page != "" and keyword =="" :
		page_data = {}
		all_page = []

		if len(result_page) % 12 == 0 :
			if page > len(result_page) // 12 :
				error = {"error": "true" , "message":"查無項目"}
				return error
			if page == len(result_page) // 12 :
				page_data["nextPage"] = "null"
				for i in range(page*12,len(result_page)) :
					all_page.append(result_page[i])
				page_data["data"] = all_page
				return page_data
			if page < len(result_page) // 12 :
				page_data["nextPage"] = page + 1
				for i in range(page*12,((page+1)*12)) :
					all_page.append(result_page[i])
				page_data["data"] = all_page
				return page_data
		if len(result_page) % 12 != 0 :
			if page > len(result_page) // 12 :
				error = {"error": "true" , "message":"查無項目"}
				return error
			if page == len(result_page) // 12 :
				page_data["nextPage"] = "null"
				for i in range(page*12,len(result_page)) :
					all_page.append(result_page[i])
				page_data["data"] = all_page
				return page_data
			if page < len(result_page) // 12 :
				page_data["nextPage"] = page + 1
				for i in range(page*12,((page+1)*12)) :
					all_page.append(result_page[i])
				page_data["data"] = all_page
				return page_data
	
	if page == "" and keyword != "" :
		keyword_data = {}
		all_keyword = []
		if len(result_keyword) <= 12 :
			keyword_data["nextPage"] = "null"
			for i in range(len(result_keyword)):
				all_keyword.append(result_keyword[i])
		if len(result_keyword) > 12 :
			keyword_data["nextPage"] = 1
			for i in range(12):
				all_keyword.append(result_keyword[i])
		keyword_data["data"] = all_keyword
		return keyword_data

	if page != "" and keyword != "" :
		keyword_data = {}
		all_keyword = []

		if len(result_keyword) % 12 == 0 :
			if page > len(result_keyword) // 12 - 1 :
				error = {"error": "true" , "message":"查無項目"}
				return error
			if page == len(result_keyword) // 12 - 1 :
				keyword_data["nextPage"] = "null"
				for i in range(page*12,len(result_keyword)) :
					all_keyword.append(result_keyword[i])
				keyword_data["data"] = all_keyword
				return keyword_data
			if page < len(result_keyword) // 12 - 1 :
				keyword_data["nextPage"] = page + 1
				for i in range(page*12,((page+1)*12)) :
					all_keyword.append(result_keyword[i])
				keyword_data["data"] = all_keyword
				return keyword_data
		if len(result_keyword) % 12 != 0 :
			if page > len(result_keyword) // 12 :
				error = {"error": "true" , "message":"查無項目"}
				return error
			if page == len(result_keyword) // 12 :
				keyword_data["nextPage"] = "null"
				for i in range(page*12,len(result_keyword)) :
					all_keyword.append(result_keyword[i])
				keyword_data["data"] = all_keyword
				return keyword_data
			if page < len(result_keyword) // 12 :
				keyword_data["nextPage"] = page + 1
				for i in range(page*12,((page+1)*12)) :
					all_keyword.append(result_keyword[i])
				keyword_data["data"] = all_keyword
				return keyword_data
	
	else :
		error = {"error": "true" , "message":"查無項目"}
		return error

@app.route("/api/attraction/<attractionId>")
def api_attraction(attractionId):
	if attractionId.isdigit() is  False :
		error = {"error": "true" , "message":"查無項目"}
		return error

	signup = pymysql.connect(
		host='localhost',
		user='root',
		password='RICETIA', #記得改
		db='taipei',
		cursorclass=pymysql.cursors.DictCursor
		)
	with signup.cursor() as cursor:
		mysqlact = "SELECT * FROM `taipeidata`"
		cursor.execute(mysqlact,)
		result = cursor.fetchall()
	signup.close()

	if int(attractionId) < len(result) and int(attractionId) > 0:	
		signup = pymysql.connect(
			host='localhost',
			user='root',
			password='RICETIA', #記得改
			db='taipei',
			cursorclass=pymysql.cursors.DictCursor
			)
		with signup.cursor() as cursor:
			mysqlact = "SELECT * FROM `taipeidata` WHERE position(%s in `id`)"
			cursor.execute(mysqlact,attractionId)
			result = cursor.fetchall()
		signup.close()

		return jsonify(result)
	else :
		error = {"error": "true" , "message":"查無項目"}
		return error
@app.route("/api/attraction/" )
def api_error():
	error = {"error": "true" , "message":"查無項目"}
	return jsonify(error)

@app.route("/api/user",methods=['GET'])
def api_get():
	if "logout" not in session:
		error = {"error":True,"message": "　暫時沒有使用者登入資訊！"}
		return error
	if session["logout"] == False:
		success = {"data":{"id":session["login_id"],"name":session["login_name"],"email":session["login_email"]}}
		return success
	else :
		error = {"error":True,"message": "　暫時沒有使用者登入資訊！"}
		return error
@app.route("/api/user",methods=['POST'])
def api_post():
	registerData = request.data.decode('utf-8')
	registerData = json.loads(registerData)
	register_name = registerData["name"]
	register_email = registerData["email"]
	register_password = registerData["password"]
	registerTest1 = False # 檢查參數1
	registerTest2 = False # 檢查參數2
	if register_name != "" and register_email != "" and register_password != "" :
		registerTest1 = True
	else :
		error = {"error":True,"message": "　請填寫所有項目！"}
		return error
	
	signup = pymysql.connect(
		host='localhost',
		user='root',
		password='RICETIA',
		db='taipei',
		)
	with signup.cursor() as cursor:
		mysqlact = "SELECT `id`,`email`,`password`,`name` FROM `user` WHERE `email`=%s"
		cursor.execute(mysqlact,register_email)
		email_check = cursor.fetchall()
	signup.close()

	if len(email_check) >= 1 :
		error = {"error":True,"message": "　此信箱已經註冊！"}
		return error
	if len(email_check) == 0 :
		registerTest2 = True
	
	if registerTest1 == True and registerTest2 == True :
		signup = pymysql.connect(
			host='localhost',
			user='root',
			password='RICETIA',
			db='taipei',
			)
		with signup.cursor() as cursor:
			mysqlact = "INSERT INTO user (name,email,password) VALUES (%s,%s,%s)"
			cursor.execute(mysqlact,(register_name,register_email,register_password))
			signup.commit()
		signup.close()
		success = {"ok":True}
		registerTest1 = False
		registerTest2 = False
		return success

	else :
		error = {"error":True,"message": "　伺服器錯誤！"}
		return error
@app.route("/api/user",methods=['PATCH'])
def api_patch():
	loginData = request.data.decode('utf-8')
	loginData = json.loads(loginData)
	login_email = loginData["email"]
	login_password = loginData["password"]
	loginTest1 = False # 檢查參數1
	loginTest2 = False # 檢查參數2
	if login_email != "" and login_password != "" :
		loginTest1 = True
	else :
		error = {"error":True,"message": "　有項目未填寫！"}
		return error
	
	signup = pymysql.connect(
		host='localhost',
		user='root',
		password='RICETIA',
		db='taipei',
		)
	with signup.cursor() as cursor:
		mysqlact = "SELECT `id`,`name`,`email`,`password` FROM `user` WHERE `email`=%s"
		cursor.execute(mysqlact,login_email)
		email_check = cursor.fetchall()
	signup.close()

	if len(email_check) >= 1 :
		if email_check[0][3] == login_password :
			loginTest2 = True
		else :
			error = {"error":True,"message": "　密碼輸入錯誤！"}
			return error
	if len(email_check) == 0 :
		error = {"error":True,"message": "　此信箱還未註冊！"}
		return error

	if loginTest1 == True and loginTest2 == True :
		session["login_id"] = email_check[0][0]
		session["login_name"] = email_check[0][1]
		session["login_email"] = login_email
		success = {"ok":True}
		loginTest1 = False
		loginTest2 = False
		session["logout"] = False
		return success

	else :
		loginTest1 = False
		loginTest2 = False
		error = {"error":True,"message": "　伺服器錯誤！"}
		return error
@app.route("/api/user",methods=['DELETE'])
def api_delete():
	del session["login_id"]
	del session["login_name"]
	del session["login_email"]
	session["logout"] = True
	success = request.data.decode('utf-8')
	success = json.loads(success)
	return success

@app.route("/api/booking",methods=["GET"])
def booking_get():
	if "booking" not in session:
		error = {"error":True,"message": "　伺服器錯誤！"}
		return error
	if session["booking"] == True :
		success = {"attractionId":session["attractionId"],"date":session["date"],"price":session["price"],"time":session["time"]}
		return success
	if session["booking"] == False :
		error = {"error":True,"message": "　還未挑選任何行程！"}
		return error
	else :
		error = {"error":True,"message": "　伺服器錯誤！"}
		return error
@app.route("/api/booking",methods=["POST"])
def booking_post():
	bookingData = request.data.decode('utf-8')
	bookingData = json.loads(bookingData)
	if bookingData["attractionId"] != "" and bookingData["date"] != "" and bookingData["price"] != "":
		session["attractionId"] = bookingData["attractionId"]
		session["date"] = bookingData["date"]
		session["price"] = bookingData["price"]
		session["time"] = bookingData["time"]
		session["booking"] = True
		success = {"ok": True}
		return success
	if bookingData["attractionId"] == "" or bookingData["date"] == "" or bookingData["price"] == "":
		error = {"error":True,"message": "　部分欄位未點選！"}
		return error
	else :
		error = {"error":True,"message": "　伺服器錯誤！"}
		return error
@app.route("/api/booking",methods=["DELETE"])
def booking_delete():
	del session["attractionId"]
	del session["date"]
	del session["price"]
	del session["time"]
	session["booking"] = False
	success = request.data.decode('utf-8')
	success = json.loads(success)
	return success

@app.route("/api/orders",methods=['GET'])
def order_get():
	order_email = session["login_email"]
	signup = pymysql.connect(
		host='localhost',
		user='root',
		password='RICETIA',
		db='taipei',
		)
	with signup.cursor() as cursor:
		mysqlact = "SELECT `data` FROM `orders` WHERE `name`=%s"
		cursor.execute(mysqlact,order_email)
		orders_email = cursor.fetchall()
	signup.close()

	if len(orders_email) > 0 :		  
		return jsonify(orders_email)
	else:
		error = {"error":"暫無預定資料"}
		return error

@app.route("/api/orders",methods=['POST'])
def order():
	primeData = request.data.decode('utf-8')
	primeData = json.loads(primeData)

	uniqueNum= ""
	for i in range (0,10):
		nowTime=datetime.datetime.now().strftime("%Y%m%d%H%M%S") #生成当前时间
		randomNum=random.randint(0,100) #生成的随机整数n，其中0<=n<=100
		if randomNum <= 10:
			randomNum=str(0)+str(randomNum)
			uniqueNum=str(nowTime)+str(randomNum)

	orders_data = {
		"data":{
			"number": uniqueNum,
			"price":primeData["order"]["price"],
			"trip":{
				"attraction":{
					"id":primeData["order"]["trip"]["attraction"]["id"],
					"name":primeData["order"]["trip"]["attraction"]["name"],
					"address":primeData["order"]["trip"]["attraction"]["address"],
					"image":primeData["order"]["trip"]["attraction"]["image"]
				},
			"date":primeData["order"]["trip"]["date"],
			"time":primeData["order"]["trip"]["time"]
			},
			"contact":{
				"name": primeData["order"]["contact"]["name"],
      			"email": primeData["order"]["contact"]["email"],
      			"phone": primeData["order"]["contact"]["phone"]
			},
			"status":0
		}
	}
	# orders_data["data"]["status"] = 1
	post_data = {
		"prime":primeData["prime"],
		"partner_key": "partner_nhiSaJcc60VQoz0SDIq36kkBIZnugh40CEg0TfRbZKfNSGBEuei1qwWT",
		"merchant_id": "rice1026_ESUN",
		"details":"Tour fee",
		"amount": primeData["order"]["price"],
		"cardholder": {
			"phone_number": primeData["order"]["contact"]["phone"],
			"name": primeData["order"]["contact"]["name"],
			"email": primeData["order"]["contact"]["email"]
		},
		"remember": True
	}

	primeURL = "https://sandbox.tappaysdk.com/tpc/payment/pay-by-prime"
	primeHeaders = {"Content-Type": "application/json","x-api-key":"partner_nhiSaJcc60VQoz0SDIq36kkBIZnugh40CEg0TfRbZKfNSGBEuei1qwWT"}
	
	primeResponse = requests.post(primeURL,json = post_data,headers = primeHeaders)
	primeResponse = primeResponse.json()
	primeStatus = primeResponse["status"]
	
	if primeStatus == 0 :
		orders_data["data"]["status"] = 0
		primenumber = orders_data["data"]["number"]
		primenumber = str(primenumber)
		orders_data = str(orders_data)
		primename = session["login_email"]
		
		signup = pymysql.connect(
			host='localhost',
			user='root',
			password='RICETIA',
			db='taipei',
			)
		with signup.cursor() as cursor:
			mysqlact = "INSERT INTO orders (number,data,name) VALUES (%s,%s,%s)"
			cursor.execute(mysqlact,(primenumber,orders_data,primename))
			signup.commit()
		signup.close()
		success = {
			"data": {
				"number": primenumber,
				"payment": {
					"status": 0,
					"message": "付款成功"
				}
			}
		}
		session["booking"] = False
		return success
	if primeStatus != 0 :
		primenumber = orders_data["data"]["number"]
		signup = pymysql.connect(
		host='localhost',
		user='root',
		password='RICETIA',
		db='taipei',
		)
		with signup.cursor() as cursor:
			mysqlact = "INSERT INTO orders (number,data) VALUES (%s,%s)"
			cursor.execute(mysqlact,(primenumber,orders_data))
			signup.commit()
		signup.close()
		success = {
			"data": {
				"number": primenumber,
				"payment": {
					"status": 1,
					"message": "尚未付款"
				}
			}
		}		
		return success

# app.run(port=3000)
app.run(host="0.0.0.0",port=3000)