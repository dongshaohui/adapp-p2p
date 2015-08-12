# -*- coding=utf8 -*-
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
import oss
from oss.oss_api import *
from pprint import pformat
from facepp import API

API_KEY = "e650f1c9f43900a5316906c658caa8be"
API_SECRET = "ron72ejcgEA6vR6BfIFD-UBBA8pFQ_QL"

def home(request):
	return render(request, 'content/home.html')
	
def p2pproduct(request):	
	if request.method == 'POST':
		return
	elif request.method == 'GET':
		return render(request, 'content/p2pproduct.html')


# accept image upload post request
def upload_image(request):
	f = None
	image_link = None
	face_features = None
	file_name = None
	if request.method == "POST":
		request_get_obj = request.GET
		if 'name' in request.GET:
			file_name = request.GET['name']
		elif 'name' in request.POST:
			file_name = request.POST['name']
		image_link = handle_uploaded_file(file_name,request.body)
		face_attrs_dict = face_detect(image_link)
		face_features,face_num = face_attrs(face_attrs_dict)
		request.session['imglink'] = image_link
		request.session['imgfeature'] = face_features
		return render(request,'content/uploadsm.html',{'image_link':image_link,'face_features':face_features})
	else:
		if 'imglink' in request.session:
			image_link = request.session['imglink']
		if 'imgfeature' in request.session:
			face_features = request.session['imgfeature']
		return render(request,'content/uploadsm.html',{'image_link':image_link,'face_features':face_features})
	
def info(request):
	return render(request, 'content/info.html')

def facematch(request):
	return render(request, 'content/facematch.html')
	
def debug(request):
	# check form upload method
	if request.method == 'POST':
		file_obj = request.FILES
	return render(request, 'content/debug.html')	

def register(request):
	return render(request,'content/register.html')
	
def uploadsm(request):
	return render(request, 'content/facesm.html', {'file':f})

# Obtain Upload Files	
def handle_uploaded_file(filename,filebody):
	destination = open(filename,'wb+')
	destination.write(filebody)
	destination.close()
	oss_object = obtain_oss_object()
	# submit file into oss
	import time
	oss_file_name = (str)(time.time()) + filename
	res = oss_object.put_object_from_file("dongshaohui-oss",oss_file_name,filename)
	result_url = None
	if res.status == 200:
		result_url = "http://dongshaohui-oss.oss-cn-hangzhou.aliyuncs.com/" + oss_file_name
	return result_url
	
# Obtain Oss Object
def obtain_oss_object():
	oss_object = OssAPI("oss.aliyuncs.com","ER1yMmIH6nhUZzEP","8QO0a5NsD3EALYEg5asDvO8sEmy8ZS")
	return oss_object

# Obtain face detect result
def face_detect(img_url):
	api = API(API_KEY, API_SECRET)
	face_params = api.detection.detect(url = img_url)
	return face_params

# return face attrs
def face_attrs(face_attrs_dict):
	face_features = {}
	face_num = len(face_attrs_dict['face'])
	if face_num != 0:
		face_features['gender'] = (face_attrs_dict['face'][0]['attribute']['gender']['value'] == 'Male') and "男" or "女"
		age_value = face_attrs_dict['face'][0]['attribute']['age']['value']
		age_range = face_attrs_dict['face'][0]['attribute']['age']['range']
		face_features['age'] = (str)(age_value - age_range) + "~" + (str)(age_value + age_range)
		face_features['race'] = face_attrs_dict['face'][0]['attribute']['race']['value']
		face_features['smile'] = face_attrs_dict['face'][0]['attribute']['smiling'] > 50 and True or False
	return face_features,face_num


def print_result(hint, result):
    def encode(obj):
        if type(obj) is unicode:
            return obj.encode('utf-8')
        if type(obj) is dict:
            return {encode(k): encode(v) for (k, v) in obj.iteritems()}
        if type(obj) is list:
            return [encode(i) for i in obj]
        return obj
    print hint
    result = encode(result)
    print '\n'.join(['  ' + i for i in pformat(result, width = 75).split('\n')])	