import sys,os
import DB as db
import matplotlib.pyplot as plt
import numpy as np
from Chart import Chart


researcher = db.get_researcher_copy()
charts_path = '../charts/gender_ratio'

def gender_ratio(top_k):
	top_n = researcher.aggregate([
		{'$match':{'gender':{'$exists':1}}},
		{'$unwind':'$labels'},
		{'$group':{
		'_id':{'label':'$labels'},
		'count':{'$sum':1}
		}},
		{'$sort':{'count':-1}}])
	label_ratios = []
	labels = []
	ratios = []
	top_n = [x['_id']['label'] for x in top_n][:top_k]
	for discipline in top_n:
		male_size = researcher.count({'gender':'M','labels':discipline})
		female_size = researcher.count({'gender':'F','labels':discipline})
		# ratio = female_size/male_size
		ratio = male_size/female_size
		label_ratios.append((discipline,ratio))
		labels.append(discipline)
		ratios.append(ratio)

	chart = Chart(top_k/3,top_k/2)
	chart.bar(ratios,top_k,labels,'Gender Ratio in Top %s Disciplines'%top_k,'discipline','ratio',True,log=False,fontsize=top_k/2)
	chart.save(charts_path+'/gender_ratio_top_{0}.eps'.format(top_k))
	chart.clear()
	chart.close()

	label_ratios.sort(key=lambda x:x[1],reverse=True)
	labels = [x[0] for x in label_ratios]
	ratios = [x[1] for x in label_ratios]

	chart = Chart(100,180)
	chart.bar(ratios,top_k,labels,'Ranked Gender Ratio in Top %s Disciplines'%top_k,'discipline','ratio',True,log=False,fontsize=120)
	chart.save(charts_path+'/ranked_gender_ratio_top_{0}'.format(top_k),format='eps')
	chart.clear()
	chart.close()

os.mkdir(charts_path) if not os.path.exists(charts_path) else ''
# gender_ratio(30)
# gender_ratio(30)
# gender_ratio(80)

