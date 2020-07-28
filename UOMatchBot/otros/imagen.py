from PIL import Image,ImageFilter

def fancysquared(pil_img):
	width,height=pil_img.size
	if width==height:
		return pil_img
	elif width>height:
		result=pil_img.resize((width,width)).filter(ImageFilter.GaussianBlur(100))
		result.paste(pil_img,(0,(width-height)//2))
		return result
	else:
		result=pil_img.resize((height,height)).filter(ImageFilter.GaussianBlur(100))
		result.paste(pil_img,((height-width)//2,0))
		return result

def expand2square(pil_img,background_color):
	width,height=pil_img.size
	if width==height:
		return pil_img
	elif width>height:
		result=Image.new(pil_img.mode,(width,width),background_color)
		result.paste(pil_img,(0,(width-height)//2))
		return result
	else:
		result=Image.new(pil_img.mode,(height,height),background_color)
		result.paste(pil_img,((height-width)//2,0))
		return result

fname="r1.jpg"
img=Image.open(fname)
print(img.format,img.size)

#img_sq=expand2square(img,(0, 0, 0)))
#img_sq.save("squared_%s"%fname,quality=95)

img_perf=fancysquared(Image.open(fname))
img_perf.save("guay_%s"%fname,quality=95)
