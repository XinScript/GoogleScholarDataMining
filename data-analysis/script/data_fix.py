import sys,os,shutil
from bson.objectid import ObjectId
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27018")	

db = client['GoogleScholar']

copy = db['researcher__copies']

def set_gender_with_cut_off():
	with open('../rf_imputerd.txt','r') as f:
		cut_off = 0.75
		for line in f:
			_id,gender,score = line.rstrip().split(',')
			score = float(score)
			if score > cut_off:
				copy.find_one_and_update({'_id':ObjectId(_id)},{'$set':{'gender':gender}})
				print('Successfully update%s'%_id)


def unset_gender():
	with open('../rf_imputerd.txt','r') as f:
		for line in f:
			_id,gender,score = line.rstrip().split(',')
			copy.find_one_and_update({'_id':ObjectId(_id)},{'$unset':{'gender':''}})
			print('Successfully unset%s'%_id)


def set_gender():
	with open('../rf_50_imputed.txt','r') as f:
		for line in f:
			_id,gender,score = line.rstrip().split(',')
			copy.find_one_and_update({'_id':ObjectId(_id)},{'$set':{'gender':gender}})
			print('Successfully update%s'%_id)	

def generate_gender_imgs():
	os.mkdir('../female_with_cutoff') if not os.path.exists('../female_with_cutoff') else ''
	os.mkdir('../male_with_cutoff') if not os.path.exists('../male_with_cutoff') else ''

	docs = copy.find({'gender':'F'})
	for doc in docs:
		_id = str(doc['_id'])
		shutil.copyfile('../../image-based-gender-imputation/data/aligned/all/all/'+_id+'.jpeg','../female_with_cutoff/'+_id+'.jpeg')

	docs = copy.find({'gender':'M'})
	for doc in docs:
		_id = str(doc['_id'])
		shutil.copyfile('../../image-based-gender-imputation/data/aligned/all/all/'+_id+'.jpeg','../male_with_cutoff/'+_id+'.jpeg')

# unset_gender()
# set_gender()
# generate_gender_imgs()

set_gender()

	# for doc in researcher.find({},{'index':1}):
	# 	try:
	# 		researcher.find_one_and_update({'_id':ObjectId(doc['_id'])},{'$set':{'index':int(doc['index'])}})
	# 		print('Successfully update%s'%doc['_id'])
	# 	except Exception as e:
	# 		print(e)
	# 		sys.exit()

# for doc in researcher.find({},{'collaborator':1}):
# 	copy.find_one_and_update({'_id':ObjectId(doc['_id'])},{'$set':{'collaborator':doc['collaborator']}})
# 	print('Successfully update%s'%doc['_id'])

# for doc in researcher.find({},{'collaborator':1}):
# 	researcher.find_one_and_update({'_id':ObjectId(doc['_id'])},{'$unset':{'collaborator':''}})
# 	print('Successfully update%s'%doc['_id'])
	
# copy.find_one_and_update({'_id':ObjectId("58f136b494662747ea544123")},{'$set':{'collaborator':doc['collaborator']}})
