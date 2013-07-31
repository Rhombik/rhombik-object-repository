#!/usr/bin/env python
import os
import logging
from PIL import Image
from django.conf import settings
import subprocess



#This function needs to take a filepath and a size, and it needs to return a 
#Relative path to a thumbnail of the right size. So "/static/thumbnails/something/subdir/thumbnail" instead of "/home/user/djangosite/mysite/thumbnailser/static/thumbnail[...]".
#Relative path to whatever I sent you. So fielpath, but relative to the web server. We're going to do this multi-threaded, so I can't gurantee I get data back in the order I put it in.
#What to render it with. We don't have all the renderes and what files to use sorted out yet, but for stuff that can just be rendered in the browser, like images, "browser" is the rendered. Other file types will have custom javascript renderers.

def thumbnail(filepath,size):
	print ("Thumbnailer says: "+filepath+" !")
	extension = os.path.splitext(filepath)[1]
	str_thumbnail_size = "-"+str(size[0])+"X"+str(size[1])

	URL="http://testing.monastery0.org"

	if extension == ".stl" or extension == ".obj" or extension ==  ".STL" or extension ==  ".OBJ":
		#checks to see ig the thumbnail already exists
		if os.path.exists(settings.MEDIA_ROOT+"thumbnails/"+os.path.relpath(filepath,settings.PROJECT_PATH)+str_thumbnail_size+".png"):
			return(settings.MEDIA_URL+"thumbnails/"+os.path.relpath(filepath,settings.PROJECT_PATH)+str_thumbnail_size+".png","/"+os.path.relpath(filepath,settings.PROJECT_PATH),"jsc3d")
		else:		
			builddir(settings.MEDIA_ROOT+"thumbnails/"+os.path.relpath(filepath,settings.PROJECT_PATH))
			#Uses phantomjs to create thumbnails.
			subprocess.call(os.path.realpath(os.path.dirname(__file__)) + "/phantom/bin/phantomjs" +" "+
				str(os.path.realpath(os.path.dirname(__file__)) + "/phantom/rastersize.js"+" "+
				"\""+URL+"/thumbs/stl/"+os.path.relpath(filepath,settings.PROJECT_PATH))+"\""+" "+
				"\""+settings.MEDIA_ROOT+"thumbnails/"+os.path.relpath(filepath,settings.PROJECT_PATH)+str_thumbnail_size+".png"+"\""+" "+
				str(size[0])+ " " + str(size[1])
				, shell=True
			)
			return(settings.MEDIA_URL+"thumbnails/"+os.path.relpath(filepath,settings.PROJECT_PATH)+str_thumbnail_size+".png","/"+os.path.relpath(filepath,settings.PROJECT_PATH),"jsc3d")

	elif extension == ".png" or extension == ".jpg" or extension == ".gif":
		 #checks to see ig the thumbnail already exists
		if os.path.exists(settings.MEDIA_ROOT+"thumbnails/"+os.path.relpath(filepath,settings.PROJECT_PATH)+str_thumbnail_size+".png"):
			return(settings.MEDIA_URL+"thumbnails/"+os.path.relpath(filepath,settings.PROJECT_PATH)+str_thumbnail_size+".png","/"+os.path.relpath(filepath,settings.PROJECT_PATH),"browser")
		else:
			img = Image.open(filepath)
			img.thumbnail(size)
			builddir(settings.MEDIA_ROOT+"thumbnails/"+os.path.relpath(filepath,settings.PROJECT_PATH))
			img.save(settings.MEDIA_ROOT+"thumbnails/"+os.path.relpath(filepath,settings.PROJECT_PATH)+str_thumbnail_size+".png", "PNG")
			return(settings.MEDIA_URL+"thumbnails/"+os.path.relpath(filepath,settings.PROJECT_PATH)+str_thumbnail_size+".png","/"+os.path.relpath(filepath,settings.PROJECT_PATH),"browser")


def builddir(outpath):
	d = os.path.dirname(outpath)
	if not os.path.exists(d):
		os.makedirs(d)



def genericthumb(filepath,size):
	str_thumbnail_size = "-"+str(size[0])+"X"+str(size[1])

	img = Image.open(settings.MEDIA_ROOT+"images/genericthumb.png")
	img.thumbnail(size)
	img.save(settings.MEDIA_ROOT+"thumbnails/genericthumb"+str_thumbnail_size+".png")
	return(settings.MEDIA_URL+"thumbnails/genericthumb"+str_thumbnail_size+".png",filepath,"norender")
	logger.warning('not a supported filetype: ' + "\"" + filepath + "\"")


