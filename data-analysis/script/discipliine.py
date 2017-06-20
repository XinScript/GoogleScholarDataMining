import DB as db
import os
from Chart import Chart
import matplotlib.pyplot as plt
import numpy as np
table = db.get_researcher_copy()
chart_path = '../charts/discipline '


def get_discipline_with_more_female():
	docs = table.aggregate([
		{'$match':{'gender':{'$exists':1}}},
		{'$unwind':'$labels'},
		{'$group':{'_id':{'label':'$labels','gender':'$gender'},'count':{'$sum':1}}}
		# {'$group':{'_id':{'label':'$labels'},'male_count':{'$sum':{'$match':{'gender':'M'}}}}}
		])
	d = {}
	for doc in docs:
		if doc['_id']['label'] in d:
			if doc['_id']['gender'] == 'M':
				d[doc['_id']['label']][0] = doc['count']
			else:
				d[doc['_id']['label']][1] = doc['count']
		else:
			d[doc['_id']['label']] = [0,0]
			if doc['_id']['gender'] == 'M':
				d[doc['_id']['label']][0] = doc['count']
			else:
				d[doc['_id']['label']][1] = doc['count']

	count = 0
	for key in d:
		if d[key][0]!=0 and d[key][1] > d[key][0]:
			count+=1
			print('%s:'%key)
			print('male {0},female {1}'.format(d[key][0],d[key][1]))
	print('number of all:%s'%count)



def discipline_proportion(top_k):
	docs = table.aggregate([
		{'$match':{'gender':{'$exists':1}}},
		{'$unwind':'$labels'},
		{'$group':{
		'_id':{'label':'$labels'},
		'count':{'$sum':1}
		}},
		{'$sort':{'count':-1}}])

	docs = [doc for doc in docs]
	# print(docs[:10])
	total = table.count({'gender':{'$exists':1}})
	count_arr = [doc['count'] for doc in docs[:top_k]]
	proportion_arr = [doc['count']/total for doc in docs[:top_k]]

	cumulative_arr = []
	c = 0
	for i in proportion_arr:
		c+=i
		cumulative_arr.append(c)

	labels = [doc['_id']['label'] for doc in docs[:top_k]]

	# chart = Chart()
	# print(len(labels))
	# print(len(arr))
	# chart.pie([arr],'test',labels)
	# chart.show()
	# chart.single_unnomarlized_CDF(arr,'disciplines CDF','disciplines','percentage')
	# chart.save(chart_path+'cdf.eps')

	# s = ''
	# print(np.median())
	# for label in labels:
	# 	s = s+label+', '
	# print(s)

	# os.mkdir(chart_path) if not os.path.exists(chart_path) else ''
	chart = Chart(100,150)
	# chart.bar(count_arr,top_k,labels,'The Top {0} popular disciplines'.format(top_k),'discipline','researcher number',True,log=False,fontsize=100)
	# chart.show()
	# chart.save(chart_path+'/number_{0}'.format(top_k),format='eps')
	# chart.clear()

	chart.bar(cumulative_arr,top_k,labels,'Cumulative propotion of most popular disciplines','discipline','propotion',True,log=False,fontsize=100)
	chart.save(chart_path+'/cumulative_{0}'.format(top_k),format='eps')
	chart.clear()

	# chart = Chart(100,150)
	# chart.bar(proportion_arr,top_k,labels,'The propotion of researchers in top 30 disciplines','discipline','propotion',True,log=False,fontsize=100)
	# chart.save(chart_path+'/proportion_{0}.eps'.format(top_k))
	# chart.clear()
	
def gender_favorite(top_k,sex='M'):
	docs = table.aggregate([
		{'$match':{'gender':sex}},
		{'$unwind':'$labels'},
		{'$group':{
		'_id':{'label':'$labels'},
		'count':{'$sum':1}
		}},
		{'$sort':{'count':-1}}])
	number_arr = []
	count_arr = []
	labels = []
	docs = [doc for doc in docs]
	for doc in docs[:top_k]:
		count_arr.append(doc['count'])
		labels.append(doc['_id']['label'])

	chart = Chart(100,180)
	chart.bar(count_arr,top_k,labels,"The Top {0} females' favorite disciplines".format(top_k),'discipline','researcher number',True,log=False,fontsize=120)
	chart.save(chart_path+'/{1}_favorite_{0}'.format(top_k,sex),format='eps')
	chart.clear()

def average_h_index(top_k):
	all_docs = copy.aggregate([{'$match':{'gender':{'$exists':True}}},{'$project':{'index':1,'labels':1,'gender':1,'count':{'$size':'$pubs'}}}])
	d = {}
	col_d = {}
	for doc in all_docs:
		for label in doc['labels']:
			if label in d:
				if doc['gender'] == 'M':
					d[label][0]+=1
					d[label][1]+=int(doc['index'])
				else:
					d[label][2]+=1
					d[label][3]+=int(doc['index'])
			else:
				if doc['gender'] == 'M':
					d[label] = [1,int(doc['index']),0,0]
				else:
					d[label] = [0,0,1,int(doc['index'])]
					
			if label in d:
				if doc['gender'] == 'M':
					d[label][0]+=1
					d[label][1]+=int(doc['index'])
				else:
					d[label][2]+=1
					d[label][3]+=int(doc['index'])
			else:
				if doc['gender'] == 'M':
					d[label] = [1,int(doc['index']),0,0]
				else:
					d[label] = [0,0,1,int(doc['index'])]	

	labels = []
	arr = []

	for key in d:
		if d[key][0] > 50:
			a = d[key][1]/d[key][0]
			b = d[key][3]/d[key][2]
			if b>a:
				print(key)
				print(a)
				print(b)

def avarage_publication(top_k):
	all_docs = copy.aggregate([{'$match':{'gender':{'$exists':True}}},{'$project':{'labels':1,'gender':1,'count':{'$size':'$pubs'}}}])	
	d = {}
	for doc in docs:
		for label in doc['labels']:
			if label in d:
				d[pub['label']] = d[pub['label']]+1






# 	arr.sort(key=lambda x:x[2],reverse=True)
# 	arr = arr[:top_k]
# 	average_index_arr = []
# 	labels = []
# 	for item in arr:
# 		labels.append(item[0])
# 		average_index_arr.append(item[1])

# 	chart = Chart(100,180)
# 	chart.bar(average_index_arr,top_k,labels,'The Top {0} fields with highest average h-index'.format(top_k),'discipline','researcher number',True,log=False,fontsize=120)
# 	chart.save(chart_path+'/top_{0}_average_disciplines'.format(top_k),format='png')
# 	chart.clear()	


discipline_proportion(30)
# get_discipline_with_more_female()
# gender_favorite(30)
# gender_favorite(30,'F')
