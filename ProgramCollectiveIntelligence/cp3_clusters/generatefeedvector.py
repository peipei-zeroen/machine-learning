#coding:utf-8

import feedparser as fp
import re


def getwords(html):
	#去除html标记
	txt = re.compile(r'<[^>]+>').sub('',html)
	#分词
	words = re.compile(r'[^A-Z^a-z]+').split(txt)
	#转换为小写
	return [w.lower() for w in words if w!='']
	
def getwordscounts(url):
	# 解析订阅源
	d = fp.parse(url)
	#print d
	wc = {}
	
	#
	for e in d.entries:
		if 'summary' in e:
			summary = e.summary
		else:
			summary = e.description
		
		#提取一个单词列表
		words = getwords(e.title + ' ' + summary)
		for w in words:
			wc.setdefault(w, 0)
			wc[w] += 1
	
	return d.feed.title,wc

apcount={}
wordcounts={}
feedlist=[line for line in file('feedlist.txt')]
for u in feedlist:
	try:
		title,wc=getwordscounts(u)
	except:
		continue
	wordcounts[title]=wc
	for word,count in wc.items():
		apcount.setdefault(word,0)
		if count>1:
			apcount[word] += 1

wordlist=[]
for w,bc in apcount.items():
	frac=float(bc)/len(feedlist)
	if frac>0.05 and frac<0.5: wordlist.append(w)

out = file('blogdata.txt','w')
out.write('Blog')
for word in wordlist: out.write('\t%s' % word)
out.write('\n')
for blog,wc in wordcounts.items():
	out.write(blog)
	for word in wordlist:
		if word in wc: out.write('\t%s' % wc[word])
		else: out.write('\t0')
	out.write('\n')
'''
feedlist=[line for line in file('feedlist.txt')]
for u in feedlist:
	try:
		title,wc=getwordscounts(u)
	except:
		continue
'''