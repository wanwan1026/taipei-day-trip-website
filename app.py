from flask import *
app=Flask(__name__)
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True

import mysql.connector
import pymysql.cursors
import pymysql
from flask import jsonify



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
		password='rice1026', #記得改
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
			password='rice1026', #記得改
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
		password='rice1026', #記得改
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
			password='rice1026', #記得改
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

app.run(port=3000)
# app.run(host="0.0.0.0",port=3000) 