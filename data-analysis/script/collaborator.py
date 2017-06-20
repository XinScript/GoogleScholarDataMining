import sys,os
import DB as db
import matplotlib.pyplot as plt
import numpy as np
from Chart import Chart

researcher = db.get_researcher_copy()
charts_path = '../charts/collaborator_distribution'

def collaborator_distribution():
	docs = researcher.aggregate([{'$match':{'gender':{'$exists':1}}},{'$project':{'gender':1,'labels':1,'count':{'$size':'$collaborator'}}}])
	male_arr = []
	female_arr = []
	for doc in docs:
		if doc['gender'] == 'M':
			male_arr.append(doc['count'])
		else:
			female_arr.append(doc['count'])


	# chart = Chart()
	# # chart.single_histogram(docs,'Collaborator Number Distribution','number of collaborators','researcher number')
	# # chart.save(charts_path+'/col_dist.eps')
	# # chart.clear()
	# # chart.single_unnomarlized_CDF(docs,'Unnormalized Collaborator CDF','number of collaborators','cumulative number')
	# chart.histogram(male_arr,female_arr,'collaborator distribution','personal collaborator number','researcher number')	
	# chart.save(charts_path+'/col_distri')
	# chart.clear()
	# chart.unnormalized_CDF(male_arr,female_arr,'cumulative collaborator number','personal collaborator number','researcher number')
	# chart.save(charts_path+'/cumulative_col')
	# chart.clear()
	male_avl = sum(male_arr)/len(male_arr)
	print(len(male_arr))
	female_avl = sum(female_arr)/len(female_arr)
	print(len(female_arr))

	fig,ax=plt.subplots()
	width = 0.5
	ind = np.linspace(0.5,1.5,2) 
	# ax.set_xticklabels()
	# chart = Chart(5,5)
	plt.bar(ind-width/2,height=[male_avl,female_avl],tick_label=['male','female'])
	plt.title('average collaborator quantity',fontsize=20)
	# chart.bar([male_average_index,female_average_index],2,['male','caonima'],'average h-index of researchers','gender','average h-index',log=False,fontsize=5)
	plt.show()

def average_index():
	male_docs = researcher.find({'gender':'M'},{'index':1})
	female_docs = researcher.find({'gender':'F'},{'index':1})
	male_index = [int(x['index']) for x in male_docs]
	female_index = [int(x['index']) for x in female_docs]
	male_average_index = sum(male_index)/len(male_index)
	female_average_index = sum(female_index)/len(female_index)
	print(male_average_index)
	print(female_average_index)

	fig,ax=plt.subplots()
	width = 0.5
	ind = np.linspace(0.5,1.5,2) 
	# ax.set_xticklabels()
	# chart = Chart(5,5)
	plt.bar(ind-width/2,height=[male_average_index,female_average_index],tick_label=['male','female'])
	plt.title('average h-index',fontsize=20)
	# chart.bar([male_average_index,female_average_index],2,['male','caonima'],'average h-index of researchers','gender','average h-index',log=False,fontsize=5)
	plt.show()

collaborator_distribution()


