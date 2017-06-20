import sys,os
sys.path.append('../../text-based-gender-imputation/script/')
import DB as db
import matplotlib.pyplot as plt
import numpy as np
from Chart import Chart

researcher = db.get_researcher_copy()
charts_path = '../charts/distribution'

def basic_info():
	total_profiles = researcher.count({})
	profiles_with_portraits = researcher.count({'portrait_url':{'$ne':''}})

	writeLine('Total profiles:%s'%total_profiles)
	writeLine('Profiles with portrait:%s'%profiles_with_portraits)
	writeLine('Proportion:%s'%(profiles_with_portraits/total_profiles))
	writeLine()

	profiles_with_face = len(os.listdir('../image-based-gender-imputation/data/aligned/all/all'))
	writeLine('Portraits that passed face dectection:%s'%profiles_with_face)
	writeLine('The proportion of portrait with face to all portraits:%s'%(profiles_with_face/profiles_with_portraits))
	writeLine()

def declare_prefrence_distribution(discipline='all researchers'):

	male_declare = researcher.count({'gender':'M','labels.0':{'$exists':1}})
	female_declare = researcher.count({'gender':'F','labels.0':{'$exists':1}})

	female_not_declare = researcher.count({'gender':'F','labels.0':{'$exists':0}})
	male_not_declare = researcher.count({'gender':'M','labels.0':{'$exists':0}})

	chart = Chart()

	chart.pie([female_not_declare,female_declare],'Females\' preference in declaration of research domain',['not declared','declared'])
	chart.save(charts_path+'/{0}/female_declare_preference'.format(discipline))
	chart.clear()

	chart.close()

	chart = Chart()
	chart.pie([male_not_declare,male_declare],'Males\' prefrence in declaration research of domain',['not declared','declared'])
	chart.save(charts_path+'/{0}/male_declare_preference'.format(discipline))
	chart.clear()

	chart.close()

def pubs_distribution(discipline='all researchers'):
	os.mkdir(charts_path+'/'+discipline) if not os.path.exists(charts_path+'/'+discipline) else ''
	male = researcher.aggregate([{'$match':{'gender':'M','labels':discipline}},{'$project':{'_id':'$_id','pubs_count':{'$size':'$pubs'}}},{'$sort':{'pubs_count':1}}])if discipline != 'all researchers' else researcher.aggregate([{'$match':{'gender':'M'}},{'$project':{'_id':'$_id','pubs_count':{'$size':'$pubs'}}},{'$sort':{'pubs_count':1}}])
	female = researcher.aggregate([{'$match':{'gender':'F','labels':discipline}},{'$project':{'_id':'$_id','pubs_count':{'$size':'$pubs'}}},{'$sort':{'pubs_count':1}}]) if discipline !='all researchers' else researcher.aggregate([{'$match':{'gender':'F'}},{'$project':{'_id':'$_id','pubs_count':{'$size':'$pubs'}}},{'$sort':{'pubs_count':1}}])

	male = [doc['pubs_count'] for doc in male]
	female = [doc['pubs_count'] for doc in female]

	chart = Chart()
	# chart.normalized_CDF(male,female,"publication CDF of {0}".format(discipline),"personal publication number","cumulative proportion",15)
	# chart.save(charts_path+'/{0}/publication_cdf'.format(discipline),format='png')
	# chart.clear()

	chart.histogram(male,female,"publication distribution of {0} ".format(discipline),"personal publication number","research count",15)

	chart.save(charts_path+'/{0}/publication_histogram'.format(discipline),format='png')
	chart.clear()

	chart = Chart(15,10)
	chart.unnormalized_CDF(male,female,"cumulative publication number of {0}".format(discipline),"personal publication number","cumulative publication",15)
	chart.save(charts_path+'/{0}/unnormalized_publication_cdf'.format(discipline),format='png')
	chart.clear()

	chart.close()

def citation_and_index_distribution(discipline='all researchers'):

	docs = researcher.find({'gender':{'$exists':1},'labels':discipline},{'gender':1,'pubs':1,'index':1}) if discipline !='all researchers' else researcher.find({'gender':{'$exists':1}},{'gender':1,'pubs':1,'index':1})
	male_citation = []
	female_citation = []
	male_index = []
	female_index = []

	pub_not_given_ciatation = 0
	profile_not_given_index = 0

	for doc in docs:
		researcher_citation_count = []
		citation_sum = 0
		if doc['gender'] == 'M':
			for pub in doc['pubs']:
				if pub['citation'].isdigit():
					citation_sum+=int(pub['citation'])
					# researcher_citation_count.append(int(pub['citation']))
				else:
					pub_not_given_ciatation+=1
			# researcher_citation_count = researcher_citation_count if researcher_citation_count else [0]
			# male_citation.append(np.mean(researcher_citation_count))
			male_citation.append(citation_sum)
			male_index.append(int(doc['index']))
		else:
			for pub in doc['pubs']:
				if pub['citation'].isdigit():
					citation_sum+=int(pub['citation'])
					# researcher_citation_count.append(int(pub['citation']))
				else:
					pub_not_given_ciatation+=1
			# researcher_citation_count = researcher_citation_count if researcher_citation_count else [0]
			# female_citation.append(np.mean(researcher_citation_count))
			female_citation.append(citation_sum)
			female_index.append(int(doc['index']))

	# chart = Chart()
	# chart.normalized_CDF(male_citation,female_citation,"citation CDF of {0}".format(discipline),"personal citation number","cumulative proportion")
	# chart.save(charts_path+'/{0}/citation_cdf'.format(discipline))
	# chart.clear()

	chart = Chart()
	chart.unnormalized_CDF(male_citation,female_citation,"cumulative citation number of {0}".format(discipline),"personal citation number","cumulative number")
	chart.save(charts_path+'/{0}/unormalized_citation_cdf'.format(discipline))
	chart.clear()

	# chart.normalized_CDF(male_index,female_index,"h-index CDF of {0}".format(discipline),"personal h-index","cumulative proportion")
	# chart.save(charts_path+'/{0}/h-index_cdf'.format(discipline))
	# chart.clear()

	chart = Chart(15,10)
	chart.unnormalized_CDF(male_index,female_index,"cumulative h-index number of {0}".format(discipline),"personal h-index","cumulative number")
	chart.save(charts_path+'/{0}/unnormalized_h-index_cdf'.format(discipline))
	chart.clear()

	chart.histogram(male_citation,female_citation,"citation distribution of {0}".format(discipline),"personal citation number","number of researcher")
	chart.save(charts_path+'/{0}/citation_histogram'.format(discipline))
	chart.clear()

	chart.histogram(male_index,female_index,"h-index distribution of {0}".format(discipline),"personal h-index","number of researcher")
	chart.save(charts_path+'/{0}/h-index_histogram'.format(discipline))
	chart.clear()

	chart.close()

def discipline_analysis(top_k):
	docs = researcher.aggregate([
		{'$match':{'gender':{'$exists':1}}},
		{'$unwind':'$labels'},
		{'$group':{
		'_id':{'label':'$labels'},
		'count':{'$sum':1}
		}},
		{'$sort':{'count':-1}},
		{'$limit':top_k}])

	i = 1
	for doc in docs:
		discipline = doc['_id']['label']
		os.mkdir(charts_path+'/{0}'.format(discipline)) if not os.path.exists(charts_path+'/{0}'.format(discipline)) else ''
		pubs_distribution(discipline)
		citation_and_index_distribution(discipline)
		i+=1




os.mkdir(charts_path) if not os.path.exists(charts_path) else ''
collaborator_distribution()

def writeLine(line=''):
	f.write(line+'\n')

os.mkdir('../charts') if not os.path.exists('../charts/') else ''
os.mkdir(charts_path) if not os.path.exists(charts_path) else ''
# os.mkdir(charts_path+'/all') if not os.path.exists(charts_path+'/all') else ''
# declare_prefrence_distribution()
# pubs_distribution()
citation_and_index_distribution()
# discipline_analysis(30)

