import sys,os
import DB as db
import matplotlib.pyplot as plt
import numpy as np
from Chart import Chart

copy = db.get_researcher_copy()
chart_path = '../charts/year'

def year_distribution(start,end):
	os.mkdir(chart_path) if not os.path.exists(chart_path) else ''
	pubs_per_year = [0 for x in range(start,end)]
	citation_per_year = [0 for x in range(start,end)]
	# print(pubs_per_year)
	year_labels = [str(x) for x in range(start,end)]
	docs = copy.find({},{'pubs':1})
	for doc in docs:
		for pub in doc['pubs']:
			if pub['year'] == '' :
				continue
			year = int(pub['year'])
			index = year-start
			if 0 > index or index >= end-start:
				continue
			try:
				pubs_per_year[index]+=1
				if pub['citation'].isdigit():
					citation_per_year[index] += int(pub['citation'])
			except Exception as e:
				print(pub['citation'])
				print(len(pub['citation']))
				print(index)
				sys.exit()

	# pubs_per_year = [year/1000 for year in pubs_per_year]
	chart = Chart(50,50)
	chart.bar(citation_per_year,end-start,year_labels,'publication number per year','year','number',log=False,fontsize=10)
	# chart.bar(pubs_per_year,end-start,year_labels,'publication number per year','year','number',log=False,fontsize=10)
	chart.save('pub_per_year',format='png')
	chart.show()
	# fig,ax = plt.subplots()
	# fig.set_size_inches(50, 75)
	# width = 0.4
	# n_ticks = end-start
	# ind = np.linspace(0.5,n_ticks-0.5,n_ticks) 
	# fontsize=50
	# ax.tick_params(axis='x', labelsize=fontsize*0.9)
	# ax.set_xticks(np.arange(end-start))
	# ax.set_xticklabels(year_labels,rotation='vertical')
	# ax.set_xlabel('year',fontsize=fontsize*1.8)
	# ax.tick_params(axis='y', labelsize=fontsize*1.5)
	# ax.set_ylabel('number',fontsize=fontsize*1.8)
	# ax.set_title('publication number per year', bbox={'facecolor':'0.8', 'pad':5},fontsize=fontsize*1.5)
	# ax.bar(ind-width/2,years,width,color='c')
	# plt.grid(False)
	# plt.show()

year_distribution(1970,2018)
