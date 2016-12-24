#coding:utf-8

def readDataFile(filepath):
	lines=[line for line in file(filepath)]
	words=lines[0].strip().split('\t')[1:]
	blognames=[]
	blogdata=[]
	for line in lines[1:]:
		p=line.strip().split('\t')
		blognames.append(p[0])
		blogdata.append([float(count) for count in p[1:]]) #这里是一个二维数组
	
	return blognames,words,blogdata
	
from math import sqrt
def pearsonScore(v1,v2):
	len=len(v1)
	#简单求和
	sum1=sum(v1)
	sum2=sum(v2)
	
	#求平方和
	sum1Sq=sum([pow(v,2) for v in v1])
	sum2Sq=sum([pow(v,2) for v in v2])
	
	#求乘积之和
	multiSum=sum([v1[i]*v2[i] for i in range(len)])
	
	#计算r
	num=multiSum - (sum1*sum2/len)
	den=sqrt((sum1Sq-pow(sum1,2)/len)*(sum2Sq-pow(sum2,2)/len))
	if den==0: return 0
	
	return 1.0 - num/den
	
class cluster:
	def __init__(self,vec,left=None,right=None,distance=0.0,id=None):
		self.left=left
		self,right=right
		self.vec=vec
		self.distance=distance
		self.id=id

def hcluster(rows, dis=pearsonScore):
	pairsOfScore={} #储存两两之间的分值容器，用来缓存，减少距离算法的计算次数
	currentClusterId=-1 #当前聚类的id
	
	#最开始的聚类集合，其中每行数据就是一个聚类
	clust=[cluster(rows[i], id=i) for i in range(len(rows))]
	
	#主键缩减聚类
	while len(clust)>1:
		#以最前面两个行数据开始
		closestPair=(0,1)
		closestScore=9 #dis(rows[0].vec,rows[1].vec)
		
		#遍历每一个配对，找出最小距离
		for i in range(len(clust)):
			for j in range(i+1,len(clust)):
				# 判断此配对是否已经计算过了
				if (clust[i].id,clust[j].id) not in pairsOfScore:
					pairsOfScore[(clust[i].id,clust[j].id)]=dis(rows[i].vec,rows[j].vec)
				
				score=pairsOfScore[(clust[i].id,clust[j].id)]
				
				if score<closestScore
					closestScore=score
					closestPair=(i,j)
		
		#接下来的逻辑时，将上面算出的最接近的两个聚类，求平均数作为新的聚类
		left=clust[closestPair[0]]
		right=clust[closestPair[1]]
		mergevec=[(left.vec[i]+right.vec[i])/2.0 for i in range(len(clust[0].vec))]
		
		#new新的聚类
		newcluster=cluster(mergevec,left=left,right=right,distance=closestScore,id=currentClusterId)
		
		# 不在原始集合中的聚类，其id为负数
		currentClusterId -= 1
		del clust[closestPair[1]]
		del clust[closestPair[0]]
		clust.append(newcluster)
	
	return clust[0]
