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

	if page != "" and keyword =="" :
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

		if int(page) < len(result) // 12 and int(page) >= 0 :
			page_data = {}
			all_page = []
			for i in range(int(page)*12,((int(page)+1)*12)) : 
				all_page.append(result[i])
			page_data["data"] = all_page
			page_data["nextPage"] = int(page) +1
			return page_data
		else :
			error = {"error": "true" , "message":"查無項目"}
			return error
	if page == "" and keyword != "" :
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
			result = cursor.fetchall()
		signup.close()

		if len(result) < 0 :
			error = {"error": "true" , "message":"查無項目"}
			return error
		if len(result) > -1 :
			if len(result) <= 12 :
				keyword_data = {}
				page = 0
				all_keyword = []
				for i in range(len(result)):
					all_keyword.append(result[i])
				keyword_data["data"] = all_keyword
				keyword_data["nextPage"] = page +1
				return keyword_data
			if len(result) > 12 :
				keyword_data = {}
				page = 0
				all_keyword = []
				for i in range(12):
					all_keyword.append(result[i])
				keyword_data["data"] = all_keyword
				keyword_data["nextPage"] = page +1
				return keyword_data
	if page != "" and keyword != "" :
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
			result = cursor.fetchall()
		signup.close()

		if len(result) > -1 and int(page) <= len(result) // 12 and int(page) >= 0 :
			if len(result) <= 12 :
				keyword_data = {}
				page = 0
				all_keyword = []
				for i in range(len(result)):
					all_keyword.append(result[i])
				keyword_data["data"] = all_keyword
				keyword_data["nextPage"] = page +1
				return keyword_data
			if len(result) > 12 :
				keyword_data = {}
				all_keyword = []
				for i in range((int(page)*12,((int(page)+1)*12))) :
					all_keyword.append(result[i])
				keyword_data["data"] = all_keyword
				keyword_data["nextPage"] = page +1
				return keyword_data
		else :
			error = {"error": "true" , "message":"查無項目"}
			return error
	if page == "" and keyword == "" :
		error = {"error": "true" , "message":"查無項目"}
		return error
	
@app.route("/api/attraction/<attractionId>")
def api_attraction(attractionId):
	if "-" in attractionId :
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

app.run(port=3000)