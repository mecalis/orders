from __future__ import print_function
import joblib
from hog import HOG
import glob
import cv2

def classify(image):
    dim = (843, 1193)
    # load the model
    model = joblib.load('model')

    # initialize the HOG descriptor
    hog = HOG(orientations=18, pixelsPerCell=(10, 10),
              cellsPerBlock=(1, 1), transform=True, block_norm="L2-Hys")
    print(image)
    image = cv2.imread(image)
    image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
    hist = hog.describe(image)
    pred = model.predict([hist])[0]
    print("Szerintem ez egy: {}".format(pred))

    return pred

for image in glob.glob('images\*.jpg'):
    classify(image)