import sys,os
sys.path.append('../../text-based-gender-imputation/script/')
import matplotlib.pyplot as plt
import numpy as np
import math
class Chart():
	def __init__(self,weight=10,height=10):
		self.fig,self.ax = plt.subplots()
		self.fig.set_size_inches(weight, height)
	def save(self,name,format='png'):
		self.fig.savefig(name+'.'+format, format=format, dpi=200)
	def clear(self):
		self.fig.clf()
		plt.clf()
	def close(self):
		plt.close()

	def show(self):
		plt.show()

	def set_fontsize(self,size):
		ax = self.ax
		for item in ([plt.title, plt.xpltis.label, plt.ypltis.label] +plt.get_xticklabels() + plt.get_yticklabels()):
			item.set_fontsize(size)

	def single_histogram(self,data,title,xlabel,ylabel):
		plt.hist(data,histtype='stepfilled',color='c',bins=50)
		plt.title(title)
		plt.xlabel(xlabel)
		plt.ylabel(ylabel)
		plt.legend()

	def single_unnomarlized_CDF(self,data,title,xlabel,ylabel):
		values, base = np.histogram(data, bins=200)
		cumulative = np.cumsum([values[i]*base[i] for i in range(200)])
		plt.plot(base[:-1], cumulative, c='c')
		plt.title(title)
		plt.xlabel(xlabel)
		plt.ylabel(ylabel)
		plt.legend()

	def histogram(self,male,female,title,xlabel,ylabel,fontsize=15):
		ax = self.ax
		plt.tick_params(axis='both', which='major', labelsize=fontsize*1.4)
		plt.hist(male,histtype='stepfilled',color='c',bins=50,label='male')
		plt.hist(female,histtype='stepfilled',color='m',bins=50,label='female')
		plt.title(title,fontsize=fontsize*1.8)
		plt.xlabel(xlabel,fontsize=fontsize*1.5)
		plt.ylabel(ylabel,fontsize=fontsize*1.5)
		plt.legend()

	def unnormalized_CDF(self,male,female,title,xlabel,ylabel,fontsize=15):
		values, base = np.histogram(female, bins=200)
		cumulative = np.cumsum([values[i]*base[i] for i in range(200)])
		plt.tick_params(axis='both', which='major', labelsize=fontsize*1.4)
		plt.plot(base[:-1], cumulative, c='m',label='female')
		values, base = np.histogram(male, bins=200)
		cumulative = np.cumsum([values[i]*base[i] for i in range(200)])
		plt.plot(base[:-1], cumulative, c='c',label='male')
		plt.title(title,fontsize=fontsize*1.8)
		plt.xlabel(xlabel,fontsize=fontsize*1.5)
		plt.ylabel(ylabel,fontsize=fontsize*1.5)
		plt.legend()


	def normalized_CDF(self,male,female,title,xlabel,ylabel,fontsize=15):
		values, base = np.histogram(male, bins=200,normed=True)
		dx = base[1]-base[0]
		cumulative = np.cumsum(values)*dx
		plt.plot(base[:-1], cumulative, c='c',label='male')

		values, base = np.histogram(female, bins=200,normed=True)
		dx = base[1]-base[0]
		cumulative = np.cumsum(values)*dx
		plt.plot(base[:-1], cumulative, c='m',label='female')

		plt.title(title,fontsize=fontsize*1.5)
		plt.xlabel(xlabel,fontsize=fontsize)
		plt.ylabel(ylabel,fontsize=fontsize)
		plt.legend()

	def twin_CDF(self,male,female,title,xlabel,ylabel,fontsize=15):
		ax = self.ax

		values, base = np.histogram(female, bins=200)
		cumulative = np.cumsum([values[i]*base[i] for i in range(200)])
		ax.plot(base[:-1], cumulative, c='m',label='female')

		values, base = np.histogram(male, bins=200)
		cumulative = np.cumsum([values[i]*base[i] for i in range(200)])
		ax.plot(base[:-1], cumulative, c='c',label='male')
		
		ax.set_ylabel('left',color='r',fontsize=fontsize*1.5)
		ax.set_xlabel(xlabel,fontsize=fontsize)
		plt.title(title,fontsize=fontsize*1.5)

		ax2 = self.ax.twinx()


		values, base = np.histogram(male, bins=200,normed=True)
		dx = base[1]-base[0]
		cumulative = np.cumsum(values)*dx
		ax2.plot(base[:-1], cumulative, c='c',label='male')

		values, base = np.histogram(female, bins=200,normed=True)
		dx = base[1]-base[0]
		cumulative = np.cumsum(values)*dx
		ax2.plot(base[:-1], cumulative, c='m',label='female')

		ax2.set_yticklabels([0,0,500000,1000000,1500000,2000000])
		ax2.set_ylabel('right',color='b',fontsize=fontsize*1.5)
		# plt.ylabel(ylabel,fontsize=fontsize)
		# plt.legend()

	def pie(self,arr,title,labels):
		plt.title(title,fontsize=25)
		patches, texts, autotexts = self.ax.pie(arr,explode=(0,0.1),labels=labels,autopct='%1.1f%%',startangle=90)
		autotexts[0].set_fontsize(25)
		autotexts[1].set_fontsize(25)
		texts[0].set_fontsize(20)
		texts[1].set_fontsize(20)
		self.ax.axis('equal')

	def bar(self,ratios,n_ticks,tick_labels,title,xlabel,ylabel,grid=True,log=True,fontsize=30,ylim=None):
		width = 0.4
		ind = np.linspace(1,n_ticks-1,n_ticks) 
		self.ax.tick_params(axis='x', labelsize=fontsize*0.9)
		self.ax.set_xticks(np.arange(n_ticks))
		self.ax.set_xticklabels(tick_labels,rotation=90)
		# self.ax.set_xticklabels(tick_labels)
		self.ax.set_xlabel(xlabel,fontsize=fontsize*1.5)
		
		if log:
			self.ax.set_yscale('log')
		self.ax.tick_params(axis='y', labelsize=fontsize*1.7)
		# self.ax.set_yticks(np.arange(0,max(ratios)+1))
		# self.ax.set_yticklabels([str(ratio) for ratio in np.arange(max(ratios))])
		self.ax.set_ylabel(ylabel,fontsize=fontsize*1.9)

		self.ax.set_title(title, bbox={'facecolor':'0.8', 'pad':5},fontsize=fontsize*2)
		self.ax.bar(ind-width/2,ratios,width,color='c')

		if ylim:
			self.ax.set_ylim(ylim)
		plt.grid(grid)

	def barh(self,ratios,n_ticks,tick_labels,title,xlabel,ylabel,grid=True,log=True,fontsize=30,ylim=None):
		y_pos = np.arange(len(ratios))
		self.ax.tick_params(axis='both', labelsize=fontsize*1.7)
		plt.barh(y_pos, ratios, align='center', alpha=0.4)
		plt.yticks(y_pos, tick_labels)
		plt.xlabel(ylabel,fontsize=fontsize*1.9)
		plt.ylabel(xlabel,fontsize=fontsize*1.5)
		plt.title(title,fontsize=fontsize*2)

	def ROC(self,actual_arr,prediction_arr):
		false_positive_rate, true_positive_rate, thresholds = roc_curve(actual_arr, prediction_arr)
		roc_auc = auc(false_positive_rate, true_positive_rate)
		plt.title('Receiver Operating Characteristic')
		plt.plot(false_positive_rate, true_positive_rate, 'b',
		label='AUC = %0.2f'% roc_auc)
		plt.legend(loc='lower right')
		plt.plot([0,1],[0,1],'r--')
		plt.ylabel('True Positive Rate')
		plt.xlabel('False Positive Rate')
		plt.show()	

