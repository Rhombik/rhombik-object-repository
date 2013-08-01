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


def jsc3d_render(filepath,size):

        URL=settings.URL
        media_root_path = settings.MEDIA_ROOT+"thumbnails/"+os.path.relpath(filepath,settings.PROJECT_PATH)
        media_url_path = settings.MEDIA_URL+"thumbnails/"+os.path.relpath(filepath,settings.PROJECT_PATH)


        #checks to see ig the thumbnail already exists
        if os.path.exists(media_root_path+str_thumbnail_size+".png"):
                return(media_url_path+str_thumbnail_size+".png","/"+os.path.relpath(filepath,settings.PROJECT_PATH),"jsc3d")
        else:
                builddir(media_root_path)
                #Uses phantomjs to create thumbnails.
                subprocess.call(os.path.realpath(os.path.dirname(__file__)) + "/phantom/bin/phantomjs" +" "+
                        str(os.path.realpath(os.path.dirname(__file__)) + "/phantom/rastersize.js"+" "+
                        "\""+URL+"/thumbs/stl/"+os.path.relpath(filepath,settings.PROJECT_PATH))+"\""+" "+
                        "\""+media_root_path+str_thumbnail_size+".png"+"\""+" "+
                        str(size[0])+ " " + str(size[1])
                        , shell=True
                )
                return(media_url_path+str_thumbnail_size+".png","/"+os.path.relpath(filepath,settings.PROJECT_PATH),"jsc3d")


def browser_render(filepath,size):

        str_thumbnail_size = "-"+str(size[0])+"X"+str(size[1])

        URL=settings.URL
        media_root_path = settings.MEDIA_ROOT+"thumbnails/"+os.path.relpath(filepath,settings.PROJECT_PATH)
        media_url_path = settings.MEDIA_URL+"thumbnails/"+os.path.relpath(filepath,settings.PROJECT_PATH)


        #checks to see ig the thumbnail already exists
        if os.path.exists(media_root_path+str_thumbnail_size+".png"):
                return(media_url_path+str_thumbnail_size+".png","/"+os.path.relpath(filepath,settings.PROJECT_PATH),"browser")
        else:
                img = Image.open(filepath)
                img.thumbnail(size)
                builddir(media_root_path)
                img.save(media_root_path+str_thumbnail_size+".png", "PNG")
                return(media_url_path+str_thumbnail_size+".png","/"+os.path.relpath(filepath,settings.PROJECT_PATH),"browser")


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



def thumbnail(filepath,size):
        
        extension = os.path.splitext(filepath)[1]
        str_thumbnail_size = "-"+str(size[0])+"X"+str(size[1])

        jsc3d_pic=[".stl",".obj",".STL",".OBJ"]
        browser_pic=[ ".png",".jpg",".gif"]

        if extension in jsc3d_pic:
                return(jsc3d_render(filepath,size))


        elif extension in browser_pic:
                return(browser_render(filepath,size))


