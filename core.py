
from PIL import Image
import numpy as np

def load_image(filepath,size):
	img = Image.open(filepath).convert('RGB')
	count = green_pixel_count(img)
	print(count)
	img = img.resize(size)
	img = np.array(img)
	total_pixel = size[0] * size[1]
	per  = count / total_pixel
	if per > .20:
		img = img /255
		return img
	else:
		return False

def green_pixel_count(img):
	#!/usr/local/bin/python3

	# Open image and make RGB and HSV versions
	RGBim = img.convert('RGB')
	HSVim = RGBim.convert('HSV')

	# Make numpy versions
	RGBna = np.array(RGBim)
	HSVna = np.array(HSVim)

	# Extract Hue
	H = HSVna[:,:,0]

	# Find all green pixels, i.e. where 100 < Hue < 140
	lo,hi = 100,140
	# Rescale to 0-255, rather than 0-360 because we are using uint8
	lo = int((lo * 255) / 360)
	hi = int((hi * 255) / 360)
	green = np.where((H>lo) & (H<hi))

	# Make all green pixels black in original image
	RGBna[green] = [0,0,0]

	count = green[0].size
	return count
# k = load_image('static/uploads/078b378c-2aa8-43d9-b674-13ccef760293.jpg',(224,224))

# filename = 'static/uploads/126dee31-ae88-4335-b335-f5bf4c12adee.jpg'
# model = load_model('models/apple.hdf5')
# # filename = "Data/Tomato_Bacterial_spot/00416648-be6e-4bd4-bc8d-82f43f8a7240___GCREC_Bact.Sp 3110.JPG"
# image = load_image(filename,(224,224))
# image = np.expand_dims(image, axis=0)
# result = model.predict(image)
# print(np.max(result))
# print(np.argmax(result))