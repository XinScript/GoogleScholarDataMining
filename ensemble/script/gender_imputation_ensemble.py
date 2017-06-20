import tensorflow as tf, sys,os
sys.path.append('../../text-based-gender-imputation/script/')
from sklearn.metrics import roc_curve, auc
import matplotlib.pyplot as plt
import pymongo
import numpy as np

image_dir = '../../image-based-gender-imputation/data/aligned/all/all/'

image_paths = [x for x in filter(lambda filename:filename.endswith('jpeg'),os.listdir(image_dir))]

my_data = np.genfromtxt(
	'../txt/firstname_and_id.txt',
	delimiter=',',
	dtype=[('name','U20'),('_id','S30')],
	converters={0:lambda x: x.decode().lower()}
	)

import ML

knn_predictions = ML.fit_and_get_proba(my_data)

image_datas = {}

for image_path in image_paths:
	image_datas[image_path.split('.jpeg')[0]] = tf.gfile.FastGFile(image_dir+image_path,'rb').read()
	
root_path = '../../image-based-gender-imputation/tensorflow/tf_files/'

label_lines = [line.rstrip() for line in tf.gfile.GFile(root_path+'retrain_labels.txt')]

with tf.gfile.FastGFile(root_path+'retrain_graph.pb','rb') as f:
	graph_def = tf.GraphDef()
	graph_def.ParseFromString(f.read())
	_ = tf.import_graph_def(graph_def,name="")

with tf.Session() as sess:
	softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
	p_male = 0
	p_female = 0
	threshold = 0.5
	w1,w2 = 0.5,0.5

	with open('imputed.txt','w') as f:
		for _id in image_datas:
			predictions = sess.run(softmax_tensor,{'DecodeJpeg/contents:0':image_datas[_id]})
			score = predictions[0][0]*w1+knn_predictions[_id]*w2

			if score > threshold:
				result = 'M'
				p_male+=1
			else:
				result = 'F'
				score = 1-score
				p_female+=1

			print('_id:{0},prediction:{1},socre:{2}'.format(_id,result,score))
			f.write('{0},{1},{2}\n'.format(_id,result,score))

	print('Predictions of M:%s'%p_male)
	print('Predictions of F:%s'%p_female)

