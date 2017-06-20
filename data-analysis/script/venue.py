import sys,os
import DB as db
import matplotlib.pyplot as plt
from Chart import Chart
import numpy as np
from textwrap import wrap


copy = db.get_researcher_copy()
path = '../charts/venue'

def top_k_venue(top_k):
	os.mkdir(path) if not os.path.exists(path) else ''
	docs = copy.find({'gender':{'$exists':1}},{'pubs':1})
	d = {}

	for doc in docs:
		for pub in doc['pubs']:
			if pub['venue']!='':
				if pub['venue'] in d:
					d[pub['venue']] +=1
				else:
					d[pub['venue']] =1


	arr = [[key,d[key]] for key in d]

	arr.sort(key=lambda x:x[1],reverse=True)

	arr = arr[:top_k]

	labels = [x[0] for x in arr]
	numbers = [x[1] for x in arr]

	# fig,ax=plt.subplots()
	# width = 0.5
	# ind = np.linspace(0.5,top_k-0.5,top_k) 
	# # ax.set_xticklabels()
	# # ax.set_xticklabels(rotation='vertical')
	# fig.set_size_inches(10,10)
	# plt.xticks([x for x in range(10)], labels, rotation='vertical')
	# plt.bar(ind-width/2,height=numbers)
	# plt.title('top 30 most popular venues',fontsize=20)
	# plt.show()

	# chart = Chart(70,70)
	# chart = Chart(100,200)
	a = ''
	for label in labels:
		a+=label+','
	print(labels)
	print(numbers)


	# labels = [ '\n'.join(wrap(l, 12)) for l in labels ]
	# chart.bar(numbers,top_k,labels,'top 30 most popular venues','publication venues','publication number',True,False,100)
	# chart.save(path+'/popular_venues',format='eps')


	# chart.show()


top_k_venue(30)