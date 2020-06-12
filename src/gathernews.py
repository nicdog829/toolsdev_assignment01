import nltk
import newspaper

keyword = input("Please enter any keyword. Press 'Enter' to continue. ")

cnn_paper = newspaper.build('http://cnn.com', memoize_articles=False)
fox_news = newspaper.build('http://www.foxnews.com', memoize_articles=False)
ign_news = newspaper.build('http://ign.com/news', memoize_articles=False)

nltk.download('punkt')#1 time download of the sentence tokenizer

def goodArticle(keyword , Article): 
	try:
		Article.download()
		Article.parse()
		Article.nlp()
	except:
		return False
	if keyword in Article.keywords: return True
	return False

def articleLooper(keyword, articles, myArticles):
	tempSummaries = ""
	for Article in articles:
		if keyword == "" or goodArticle(keyword,Article):
			try:
				myArticles.append(Article)
				Article.download()
				Article.parse()
			except:
				continue
			tempSummaries += Article.title
			tempSummaries += "-"
			tempSummaries += ",".join(Article.authors)
			Article.nlp()
			tempSummaries += "\n"
			tempSummaries += Article.summary
			tempSummaries += "\n\n"	


	return tempSummaries	
myArticles = []
summaries = ""
summaries += articleLooper(keyword,cnn_paper.articles[:20],myArticles)
summaries += articleLooper(keyword,fox_news.articles[:20],myArticles)
summaries += articleLooper(keyword,ign_news.articles[:20],myArticles)
keys = []
frequencies = {}
for Article in myArticles:
	Article.download()
	Article.parse()
	Article.nlp()
	keywords = Article.keywords
	for word in keywords:
		if word in keys:
			frequencies[word] += 1
		else:
			keys.append(word)
			frequencies[word] = 1
l = [(k, v) for k, v in frequencies.items()]
l.sort(key=lambda x:x[1],reverse=True)
l=l[:10]
labels = [i[0]for i in l ]
occurences = [i[1]for i in l ]

import matplotlib.pyplot as plt
import numpy as np
y_pos = np.arange(len(labels))
plt.bar(y_pos, occurences)
plt.xticks(y_pos, labels)
plt.show()


summaries = summaries.encode("ascii", "ignore").decode()
with open("news_summary.txt","w")as f:
	f.write(summaries)