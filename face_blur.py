import cv2
import time
import argparse
import numpy as np

def blur_face(image, face_detector):
	"""
	Runs the face detector, extracts face regions and blurs them

	Args:
	  image: Input image or video frame
	  face_detector: Path to the face haarcascade file

	Returns:
	  The processed image with face blurred

	"""

	(h, w) = image.shape[:2]
	k_w = int(w / 7)
	k_h = int(h / 7)

	if k_w % 2 == 0:
		k_w -= 1
	if k_h % 2 == 0:
		k_h -= 1

	# Load the face haarcascade
	face_cascade = cv2.CascadeClassifier(face_detector)

	# Convert image to grayscale for detection
	image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

	# Detect face regions in the image
	detected_faces = face_cascade.detectMultiScale(image_gray, minNeighbors=5, scaleFactor=1.1,)

	# Loop throught face regions and blur them using Gaussian Blur
	for (x, y, w, h) in detected_faces:
		blurred_face_image = image[y:y+h, x:x+w]
		blurred_face_image= cv2.GaussianBlur(blurred_face_image, (k_w, k_h), 0)
		image[y:y+h,x:x+w]=blurred_face_image
	

	return image


if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('-i', '--image', help='path to image')
	parser.add_argument('-v', '--video', help='path to video file')
	parser.add_argument('-f', '--face_cascade', help='path to haarcascade for face', default='haarcascade_frontalface_default.xml')
	args = vars(parser.parse_args())

	# Run the algorithm on an image and save the output
	if args['image']:

		test_image = cv2.imread(args['image'])

		face_blurred_image = blur_face(test_image, args['face_cascade'])

		cv2.imshow('Face Blurred', face_blurred_image)

		cv2.imwrite('output/face_blurred_output.png', face_blurred_image)

		cv2.waitKey(0)

	# Run the algorithm on a video
	elif args['video']:

		video = cv2.VideoCapture(args['video'])
		while True:
			ret, frame = video.read()
			
			if ret == False:
				break

			face_blurred_frame = blur_face(frame, args['face_cascade'])

			face_blurred_frame = cv2.resize(face_blurred_frame, (500,500), cv2.INTER_CUBIC)

			cv2.imshow('Face Blurred', face_blurred_frame)

			if cv2.waitKey(1) & 0xff == ord('q'):
				break

		video.release()

	# Run the algorithm on live web-cam feed
	else:

		video = cv2.VideoCapture(0)
		time.sleep(2)
		while True:
			ret, frame = video.read()

			if ret == False:
				break

			face_blurred_frame = blur_face(frame, args['face_cascade'])


			cv2.imshow('Face Blurred', face_blurred_frame)

			if cv2.waitKey(4) & 0xff == ord('q'):
				break

		video.release()


	cv2.destroyAllWindows()

