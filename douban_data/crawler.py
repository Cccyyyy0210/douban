# coding=utf-8
from bs4 import BeautifulSoup
import re
import xlwt
import urllib.parse
import urllib.request
import urllib.error
import sqlite3

def askURL(url):#模拟浏览器访问豆瓣服务器
	head = {}  # 模拟浏览器头部信息,向豆瓣服务器发送消息
	# 伪装成浏览器,而不是爬虫
	head["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.34"
	req = urllib.request.Request(url=url, headers=head)
	response = urllib.request.urlopen(req)
	html = response.read().decode('utf-8')
	return html
def getData(baseURL):#获取top250的电影数据
	dataList=[] #存储数据
	for i in range(0,10):
		#获取html原始信息
		url=baseURL+str(i*25)
		html=askURL(url)
		bs = BeautifulSoup(html,"html.parser")
		#筛选所需信息
		for item in bs.find_all('div',class_="item"):
			data=[] #单个电影信息
			item=str(item)
			# 1.排名
			rank=re.findall(findRank,item)[0]
			data.append(rank)
			# 2.片名
			title=re.findall(findTitle,item)
			if (len(title) == 2):
				ctitle = title[0].strip()
				data.append(ctitle)
				otitle = title[1].replace('/', '').strip()
				data.append(otitle)
			else:
				data.append(title[0])
				data.append('')
			#3.佳句
			inq=re.findall(findQuote,item)
			if len(inq)==1:
				quote=inq[0]
				data.append(quote)
			else:
				data.append('')
			# 4.评分
			score=re.findall(findScore,item)[0]
			data.append(score)
			# 5.评价人数
			evaluator=re.findall(findEvaluator,item)[0]
			data.append(evaluator)
			dataList.append(data)
			print(data)
	return dataList
#将爬取的数据存储到数据库
def init_DB(dbPath):
	sql='''
	create table movie250(
    id integer primary key,
    chineseTitle text,
    otherTitle text,
    quote text,
    score real,
    evaluator integer
    )
	'''
	connection=sqlite3.connect(dbPath)
	cursor=connection.cursor()
	cursor.execute(sql)
	connection.commit()
	cursor.close()
	connection.close()
	print("创建成功")
def drop_DB(dbPath):
	sql='''
	drop table movie250
	'''
	connection=sqlite3.connect(dbPath)
	cursor=connection.cursor()
	cursor.execute(sql)
	connection.commit()
	cursor.close()
	connection.close()
	print("删除成功")
def saveData2DB(dbPath,dataList):#保存爬取数据到数据库
	connection = sqlite3.connect(dbPath)
	cursor = connection.cursor()
	for data in dataList:
		for index in range(len(data)):
			data[index] =str('"' + data[index] + '"')
		sql='''
		insert into movie250(id,chineseTitle,otherTitle,quote,score,evaluator)
		values (%s)
		'''%",".join(data)
		cursor.execute(sql)
		connection.commit()
	cursor.close()
	connection.close()
	print("数据存储成功")

if __name__=="__main__":
	#全局变量
	baseURL="https://movie.douban.com/top250?start="
	#爬虫信息筛选正则表达式
	#1.排名
	findRank=re.compile(r'<em class="">(\d*)</em>')
	#2.片名
	findTitle=re.compile(r'<span class="title">(.*)</span>')
	#3.评分
	findScore=re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
	#4.评价人数
	findEvaluator=re.compile(r'<span>(\d*)人评价</span>')
	#5.经典台词
	findQuote=re.compile(r'<span class="inq">(.*)</span>',re.S)
	dbPath=r"D:\pycharm\douban\movie250.db"
	#init_DB(dbPath)
	dataList=getData(baseURL)
	#drop_DB(dbPath)
	saveData2DB(dbPath, dataList)
