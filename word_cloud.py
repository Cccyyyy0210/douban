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
def createWordCloud(imgPath, target,limitation=''):  # 词云mask地址,词来源
	conn = sqlite3.connect("movie250.db")
	cursor = conn.cursor()
	sql = f'select {target} from movie250 {limitation}'
	data = cursor.execute(sql)
	text = ""
	for item in data:
		text = text + item[0]
	cursor.close()
	conn.close()
	# 分词
	cut = jieba.cut(text)
	string = ' '.join(cut)
	# 制作词云图片
	img = Image.open(imgPath)  # 遮罩图片
	img_array = numpy.array(img)
	wc = WordCloud(
		background_color='white',
		mask=img_array,
		font_path="STXINWEI.TTF"
	)
	wc.generate_from_text(string)
	# 绘制图片
	pyplot.subplots(figsize=(20, 16))
	pyplot.imshow(wc)
	pyplot.axis("off")
	pyplot.show()


if __name__ == "__main__":
	title_imgPath = r'./static/assets/img/cat.jpg'
	quote_imgPath = r'./static/assets/img/tree.jpg'
	path2=r'static/assets/img/jerry.jpg'
	path3=r'static/assets/img/蜘蛛侠.jpg'
	limitation1='where id between 1 and 125'
	limitation2 = 'where id between 126 and 250'
	# createWordCloud(quote_imgPath,'quote',limitation1)#台词1
	createWordCloud(path3, 'quote', limitation1)#台词2
	# createWordCloud(title_imgPath, 'chineseTitle',limitation1)#片名1
	#createWordCloud(path2, 'chineseTitle', limitation2)#片名2
