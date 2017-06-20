import sys,os
import DB as db
import matplotlib.pyplot as plt
import numpy as np
from Chart import Chart


researcher = db.get_researcher_copy()
charts_path = '../charts/h_index_over_time'

def h_index_over_time():
	def calculate_h_index(pubs,year):
		pubs = list(filter(lambda pub:pub['year'].isdigit() and pub['citation'].isdigit() and int(pub['year'])<=year,pubs))
		h_index = 0
		for index, pub in enumerate(pubs):
			if int(pub['citation']) >= index:
				h_index = index
			else:
				break
		return h_index

	# researcher.aggregate([
	# 	{'$match':{'gender':{'$exists':1}}},
	# 	{'pubs.year':{'$gt'}}
	# 	])
	# print(len(docs))
	h_index_arr = []
	start = 1980
	end = 2018
	for year in range(start,end):
		docs = researcher.find({'gender':{'$exists':1}})
		h_indexs = [calculate_h_index(doc['pubs'],year) for doc in docs]
		print(sum(h_indexs))
		h_index_arr.append(sum(h_indexs))

	chart = Chart(30,30)
	labels = [str(year) for year in range(start,end)]
	chart.bar(h_index_arr,end-start,labels,'h-index change over time','time','cumulative h_index',True,False)
	chart.save(charts_path+'/h_index_over_time.eps')
	chart.clear()
	chart.close()
	# print(len(h_indexs))
	# d = {}
	# for doc in docs:
	# 	for pub in doc['pubs']:
	# 		int(pub['year'])
	# doc = list(researcher.find({'ID':'5qOogLUAAAAJ'}))



# os.mkdir(charts_path) if not os.path.exists(charts_path) else ''
h_index_over_time()
