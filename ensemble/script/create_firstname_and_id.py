import sys,os,re
sys.path.append('../../text-based-gender-imputation/')
import DB as db
from bson.objectid import ObjectId

def choose_name(fullname):
	name_arr = re.split(r'\s|\-|,',fullname)
	for name in name_arr:
		if re.findall(r'\.|\/',name) or len(name)<2:
			continue
		else:
			return name
	return name_arr[-1]

def createNameTxt(image_paths):
	re_co = db.get_researcher_copy()
	missing_value = 0

	with open('../txt/firstname_and_id.txt','w') as f:
		for image_path in image_paths:
			_id = image_path.split('.jpeg')[0]
			doc = list(re_co.find({'_id':ObjectId(_id)}))[0]
			name = doc['name']
			if name:
				firstname = choose_name(name).lower()
				f.write(firstname+','+_id+'\n')
			else:
				missing_value+=1
	print('successful created:%s'%len(image_paths))
	print('missing name:%s'%(missing_value))


image_dir = '../../image-based-gender-imputation/data/aligned/all/all/'

image_paths = [x for x in filter(lambda filename:filename.endswith('jpeg'),os.listdir(image_dir))]

createNameTxt(image_paths)