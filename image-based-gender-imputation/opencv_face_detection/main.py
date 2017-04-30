import cv2
import os

# img_path = '../dataset/'
img_path = 'male/'

data_path = [
# 'data/haarcascades/haarcascade_frontalface_alt_tree.xml',
# 'data/haarcascades/haarcascade_frontalface_alt.xml',
# 'data/haarcascades/haarcascade_frontalface_alt2.xml',
'data/haarcascades/haarcascade_frontalface_default.xml',
]
img_names = [x for x in filter(lambda filename: filename.endswith('png'),os.listdir(img_path))]
# face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
face_cascades = [cv2.CascadeClassifier(x) for x in data_path]

count = 0
total = len(img_names)

for img_name in img_names:
	img = cv2.imread(img_path+img_name)
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	max_grades = 0
	for face_cascade in face_cascades:
		faces = face_cascade.detectMultiScale(
		    gray,
		    # 1.3,
		    # 5
		    scaleFactor=1.2,
		    minNeighbors=5,
		    minSize=(30, 30),
		    flags = cv2.CASCADE_SCALE_IMAGE
		)
		if len(faces) > max_grades:
			max_grades = len(faces)
	if max_grades > 0:
		count+=1

	# cv2.imshow('img',img)
	# cv2.waitKey(0)
	# cv2.destroyAllWindows()
	# print(img_name)
	# print(len(faces))

print('tatal:{0},faces:{1},percentage:{2}'.format(total,count,count/total))
