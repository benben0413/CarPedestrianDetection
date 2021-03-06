import os
import cv2
import numpy as np
import imutils
import imageProcessor

from imutils.object_detection import non_max_suppression

CV_HOG_DEFAULT_PEOPLE_SVM = 0

class humanDetector:
	def __init__(self):
		# the type of the classifier
		self.classifierType_ = None

		# the pointer point to the classifier
		self.classifier_ = None

		# a function-pointer list which contain some detection functions for
		# some specific classifier. Each classifier will map to ONLY one
		# detection function in this list.
		self.detectFuncPointer_ = [self.__detectHuman4cvDefaultHogSVM]


	# initialize the default SVM human classifier provided by opencv using hog feature
	def setDefaultSVM4Human(self):
		global CV_HOG_DEFAULT_PEOPLE_SVM

		self.classifierType_ = CV_HOG_DEFAULT_PEOPLE_SVM

		self.classifier_ = cv2.HOGDescriptor()
		self.classifier_.setSVMDetector( cv2.HOGDescriptor_getDefaultPeopleDetector() )

	# detect human object in the image
	# parameter:
	# 		img: the image your want to detect
	# return:
	#		img: the modified image file with detected object rectangled
	#		rois: regions of interst, i.e., the rectangle area (x1, y1, x2, y2)
	def detectHuman(self, img):
		return self.detectFuncPointer_[self.classifierType_](img)


	# private function
	# humen detection function for the default SVM human classifier provided by opencv
	# parameter:
	#		img: the image your want to detect
	# return:
	#		img: the modified image file with detected object rectangled
	#		rois: regions of interst, i.e., the rectangle area (x1, y1, x2, y2)
	def __detectHuman4cvDefaultHogSVM(self, img):
		img = imutils.resize(img, height=max(128, img.shape[0]))
		img = imutils.resize(img, width=max(120, img.shape[1]))
		img = imutils.resize(img, width=min(960, img.shape[1]))

		rois, weights = self.classifier_.detectMultiScale(img, winStride=(4, 4),
			padding=(8, 8), scale=1.05)

		# apply non-maxima suppression to the bounding boxes using a
		# fairly large overlap threshold to try to maintain overlapping
		# boxes that are still people
		rois = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rois])
		rois = non_max_suppression(rois, probs=None, overlapThresh=0.65)

		for (x1, y1, x2, y2) in rois:
			cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 2)

		return img, rois



# Tester for human detector
# root: the root directory of the testing files
def tester(root):
	if root is None:
		print "humanDetector-tester(): img is None"

	detector = humanDetector()
	detector.setDefaultSVM4Human()

	images = imageProcessor.loadImages(root)
	if images == []:
		print "humanDetector-tester(): Cannot find any image in path:", root
		return 

	numOfHuman, numOfNonHuman = 0, 0
	for img in images:
		img, rois = detector.detectHuman(img)

		if rois == []:
			numOfNonHuman += 1
		else:
			numOfHuman += 1

	print "number of human:", numOfHuman
	print "number of non-human", numOfNonHuman
	print "ratio of human:", 1.0 * numOfHuman / (numOfHuman + numOfNonHuman)


if __name__ == '__main__':
	tester("")

