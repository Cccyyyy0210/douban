# coding=utf-8
import jieba
from Tools.scripts.objgraph import ignore
from matplotlib import pyplot
import numpy
from wordcloud import WordCloud
from PIL import Image
import sqlite3
# import warnings
# warnings.filterwarnings('ignore')
def test1():
	conn=sqlite3.connect("movie250.db")
	cursor=conn.cursor()
	sql='select chineseTitle from movie250'
	#sql = 'select quote from movie250'
	data=cursor.execute(sql)
	text=""
	for item in data:
		text=text+item[0]
	cursor.close()
	conn.close()
	#分词
	cut=jieba.cut(text)
	string=' '.join(cut)
	print(len(string))
	#制作词云图片
	img=Image.open(r'./static/assets/img/cat.jpg')#遮罩图片
	img_array=numpy.array(img)
	wc=WordCloud(
		background_color='white',
		mask=img_array,
		font_path="STXINWEI.TTF"
	)
	wc.generate_from_text(string)
	#绘制图片
	pyplot.subplots(figsize=(20,16))
	pyplot.imshow(wc)
	pyplot.axis("off")
	pyplot.show()
test1()


