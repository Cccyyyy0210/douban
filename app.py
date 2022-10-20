import sqlite3

from flask import Flask,render_template
from douban_data import crawler
app = Flask(__name__)


@app.route('/index')
def index():  # put application's code here
	return render_template('index.html')
@app.route('/movie')
def movie():  # put application's code here
	dataList=[]
	connection=sqlite3.connect("movie250.db")
	cursor=connection.cursor()
	sql="select * from movie250"
	data=cursor.execute(sql)
	for item in data:
		dataList.append(item)
	cursor.close()
	connection.close()
	return render_template('movie.html',movies=dataList)
@app.route('/score')
def score():  # put application's code here
	connection = sqlite3.connect("movie250.db")
	cursor = connection.cursor()
	scoreList = []#评分
	numberList=[]#统计评分所对应的电影数量
	sql = "select score,count(score) from movie250 group by score"
	data = cursor.execute(sql)
	for item in data:
		scoreList.append(item[0])
		numberList.append(item[1])
	cursor.close()
	connection.close()
	return render_template('score.html',scoreList=scoreList,numberList=numberList)
@app.route('/word')
def word():  # put application's code here
	return render_template('word.html')

if __name__ == '__main__':
	app.run()
