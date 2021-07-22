import joblib
from sklearn.svm import LinearSVC
import numpy as np
from hog import HOG
import argparse
import glob
import cv2

def resize(image, width = None, height = None, inter = cv2.INTER_AREA):
	# initialize the dimensions of the image to be resized and
	# grab the image size
	dim = None
	(h, w) = image.shape[:2]

	# if both the width and height are None, then return the
	# original image
	if width is None and height is None:
		return image

	# check to see if the width is None
	if width is None:
		# calculate the ratio of the height and construct the
		# dimensions
		r = height / float(h)
		dim = (int(w * r), height)

	# otherwise, the height is None
	else:
		# calculate the ratio of the width and construct the
		# dimensions
		r = width / float(w)
		dim = (width, int(h * r))

	# resize the image
	resized = cv2.resize(image, dim, interpolation = inter)

	# return the resized image
	return resized

hog = HOG(orientations = 18, pixelsPerCell = (10, 10),
	cellsPerBlock = (1, 1), transform = True)
print('HOG betöltve.')

data = []
target = []
dim = (843,1193)

for image in glob.glob('images\*.jpg'):
	label = image.split('_')[0].split('\\')[-1]
	# print('Label: ', label)
	if label == 'egyeb':
		target.append(int(0))
	else:
		target.append(int(1))
	print('Név: ', image)
	image = cv2.imread(image)
	image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
	print(' shape: ', image.shape)
	hist = hog.describe(image)
	data.append(hist)

# data = np.array(data)

# train the model
print('Modell betöltése:')
model = LinearSVC(random_state = 42)
print('Model betanítása:')
model.fit(data, target)
print('Betanítás kész!')

joblib.dump(model, 'model')