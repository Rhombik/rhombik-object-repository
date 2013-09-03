#!/usr/bin/env python
import os
## logging is not used in this itteration.
import logging
##python image library for rendering new thumbnails
from PIL import Image
##this imports the settings from our webframwork
from django.conf import settings
## subprocess lets us call arbitrary programs, in this case phantom js
import subprocess

###import the url from the django settings
URL=settings.URL
PHANTOMJSPATH=settings.PHANTOMJSPATH

###make directory if it doesn't exist.
def builddir(outpath):
        d = os.path.dirname(outpath)
        if not os.path.exists(d):
                os.makedirs(d)

#This function takes a filepath and size, and returns a:
#Path from /media to a generic thumbnail of the right size.
#Path from /media to the image/file sent.
#File type for render options 
def genericthumb(filepath,size):

        return("null","null","norender")
        logger.warning('not a supported filetype: ' + "\"" + filepath + "\"")

############### info on using thumbnailer.thumbnailer.thumbnail() #############
#This function takes:
#       filepath;        an absolute path to a file to be thumbnailed
#       size;            the dimensions of the thumbnail to be made in an array of two values
#       forceupdate;     (optional) True forces the thumbnail to be regenerated.
#                         Used for when images are changed or whatnot

#And it returns:
#       [0]     Relative path to a thumbnail of the right size. So "/static/thumbnails/something/subdir/thumbnail" instead of "/home/user/djangosite/mysite/thumbnailser/static/thumbnail[...]".
#       [1]     Relative path to whatever I sent you. So fielpath, but relative to the web server. We're going to do this multi-threaded, so I can't gurantee I get data back in the order I put it in.
#       [2]     What to render it with. We don't have all the renderes and what files to use sorted out yet, but for stuff that can just be rendered in the browser, like images, "browser" is the rendered. Other file types will have custom javascript renderers.
def thumbnail(filepath, size, forceupdate=False):
        
        print("thumbnail says:"+filepath)
        filepath = str(filepath)
        extension = os.path.splitext(filepath)[1]
        str_thumbnail_size = "-"+str(size[0])+"X"+str(size[1])

        jsc3d_pic=[".stl",".obj",".STL",".OBJ"]
        browser_pic=[ ".png",".jpg",".gif"]

        str_thumbnail_size = "-"+str(size[0])+"X"+str(size[1])

        media_root_path = settings.MEDIA_ROOT+"thumbnails/"+os.path.relpath(filepath,settings.PROJECT_PATH)
        media_url_path = settings.MEDIA_URL+"thumbnails/"+os.path.relpath(filepath,settings.PROJECT_PATH)
        print("thumbpathteststuff: "+filepath,settings.PROJECT_PATH)

        if extension in jsc3d_pic:
        #checks to see ig the thumbnail already exists
	        print("its a jsc3d pic.")
	        if forceupdate==False and os.path.exists(media_root_path+str_thumbnail_size+".png"):
	                return(media_url_path+str_thumbnail_size+".png","/"+os.path.relpath(filepath,settings.PROJECT_PATH),"jsc3d")
	        else:
	                builddir(media_root_path)
	                #Uses phantomjs to create thumbnails.
	                subprocess.call(

	                        #The path to the phantomjs binary
	                        PHANTOMJSPATH +" "+
	                        #What settings to use. PhantomJS can do a lot of stuff, rastersize lets you specfy a URL, an output path and a size. In reture it gives you a screenshot. If you're changing it you're probably rewriting the whole thing
	                        str(os.path.realpath(os.path.dirname(__file__)) + "/rastersize.js"+" "+
	                        #phantomJS takes a screenshot of a webpage. This is that webpage.
	                        "\""+URL+"/thumbs/stl/"+os.path.relpath(filepath,settings.PROJECT_PATH))+"\""+" "+
	                        #Where to save it to
	                        "\""+media_root_path+str_thumbnail_size+".png"+"\""+" "+
	                        #what size to save it as.
	                        str(size[0])+" "+str(size[1])
	
	                        , shell=True
	                )
	                return(media_url_path+str_thumbnail_size+".png","/"+os.path.relpath(filepath,settings.PROJECT_PATH),"jsc3d")



        elif extension in browser_pic:
	        #checks to see ig the thumbnail already exists.
	        if forceupdate==False and os.path.exists(media_root_path+str_thumbnail_size+".png"):
	                return(media_url_path+str_thumbnail_size+".png","/"+os.path.relpath(filepath,settings.PROJECT_PATH),"browser")
	        else:
	                print("well, it is gettign here."+filepath)
	                try:
	                        img = Image.open("/"+filepath)
	                        img.thumbnail(size)
	                        builddir(media_root_path)
	                        img.save(media_root_path+str_thumbnail_size+".png", "PNG")
	                        return(media_url_path+str_thumbnail_size+".png","/"+os.path.relpath(filepath,settings.PROJECT_PATH),"browser")
	                except:
	                        return(genericthumb(filepath,size))
#        else:
#                return(genericthumb(filepath,size))




