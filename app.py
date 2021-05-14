from flask import *
app=Flask(__name__)
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True

# import mysql.connector
import pymysql.cursors
import pymysql
# from flask import jsonify

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

@app.route("/api/user",methods=['POST'])
def api_user():
	
	if request.values["send"] == "login":
		login_email = request.form["login_email"]
		login_password = request.form["login_password"]
		session["user"] = login_email + "," + login_password
	if request.values["send"] == "register":
		register_name = request.form["register_name"]
		register_email = request.form["register_email"]
		register_password = request.form["register_password"]
		session["user"] = register_name + "," + register_email + "," + register_password
	if request.values["send"] == "check":
		session["user"] = "check"
	if request.values["send"] == "logout":
		session["user"] = "logout"
	
	return "success"
#
@app.route("/api/user")
def api_api():
	# return session["user"]
	if session["user"] == "logout":
		session["log_user"] = "null"
		return "null"
	if session["user"] == "check":
		return session["log_user"]
	
	user = ""
	user = session["user"]
	user = user.split(",")
	if len(user) == 2:
		signup = pymysql.connect(
			host='localhost',
			user='root',
			password='rice1026',
			db='taipei',
			)
		with signup.cursor() as cursor:
			mysqlact = "SELECT `id`,`email`,`password`,`name` FROM `user` WHERE `email`=%s"
			cursor.execute(mysqlact,user[0])
			email_check = cursor.fetchall()
		signup.close()

		if len(email_check) == 1:
			if email_check[0][2] == user[1]:
				log_user = {}
				log_user["data"]={"id":email_check[0][0],"name":email_check[0][3],"email":email_check[0][1]}
				session["log_user"] = log_user
				log = {"ok":True}
				return jsonify(log)
			else:
				log ={"error": True,"message": "輸入錯誤的密碼！"}
				return jsonify(log)
		if len(email_check) == 0 :
			log = {"error":True,"message": "此信箱尚未註冊！"}
			return jsonify(log)
	if len(user) == 3:
		register_name = user[0]
		register_email = user[1]
		register_password = user[2]
		signup = pymysql.connect(
			host='localhost',
			user='root',
			password='rice1026',
			db='taipei',
			)
		with signup.cursor() as cursor:
			mysqlact = "SELECT `id`,`email`,`password` FROM `user` WHERE `email`=%s"
			cursor.execute(mysqlact,register_email)
			email_check = cursor.fetchall()
		signup.close()

		if len(email_check) == 1 :
			log ={"error": True,"message": "此信箱已經註冊！"}
			return jsonify(log)
		if len(email_check) == 0 :
			signup = pymysql.connect(
			host='localhost',
			user='root',
			password='rice1026',
			db='taipei',
			)
			with signup.cursor() as cursor:
					mysqlact = "INSERT INTO user (name,email,password) VALUES (%s,%s,%s)"
					cursor.execute(mysqlact,(register_name,register_email,register_password))
					signup.commit()
			signup.close()
			log = {"ok":True}
			return jsonify(log)
	else :
		log ={"error": True,"message": "伺服器錯誤！"}
		return jsonify(log)

	
# app.run(port=3000)
app.run(host="0.0.0.0",port=3000) 