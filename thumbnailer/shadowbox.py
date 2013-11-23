"""
This is the amazing script Tristan is writing to get useful variables and use them to make cool shadowbox gallery html script.

Ok, not that amazing.

Edit: It IS that amazing.

Edit: It had cross directory vulnerabilities..

"""
##use this for testing regular expressions.
testtext = """aegfas\nasegf\n[apples, notapples] other [more, list] text\nefaefva"""


from django.template.loader import render_to_string
from markdown.postprocessors import Postprocessor
import re
import os
from django.conf import settings



import filemanager.models
##regular expressions...
findSquareBrackets = re.compile(r'\[([^\[|\]*]+)\]')
findEachImage = re.compile(r'[\[,\s\]]*')
findNewLine = re.compile(r'(\n)')

import posixpath

# ...         Yeah, somethime it would be good to get better security. better security is better.
def goodSecurity(path):
    #path = posixpath.normpath(path)
    newpath = ''
    for part in path.split('/'):
        if not part:
            # strip empty path components
            continue

        drive, part = os.path.splitdrive(part)
        head, part = os.path.split(part)
        if part in (os.curdir, os.pardir):
            # strip '.' and '..' in path
            continue

        newpath = os.path.join(newpath, part).replace('\\', '/')
    return newpath

### this function gets a list of images, a gallery name (numbers generated in order of gallery per page), and the pages pk. and returns an html string formatted to make a gallery
def outputstuff(imagelist, gallerynum, pk):
    images = ""
    for image in imagelist:
        print("shadowimage "+image)
        #ext = os.path.splitext(image)[1]
        #image = "/"+goodSecurity(settings.MEDIA_ROOT+ "uploads/" + pk + image)# I really don't know if this is good... if you could get this to fail youd get "/" .... 3:[
        lst = []
        #print("path: "+image)
        obj = filemanager.models.fileobject.objects.filter(filename = "uploads/"+pk+image)
        #print(obj[0].filename)
        if obj:
            print("this image is fine too")
            #images.append(obj[0])
            images += ("<fileobject id=\""+str(obj[0].id)+"\"galleryname=\""+str(gallerynum)+"\"></fileobject>")
       #else:
       #    for i in os.walk(image , topdown=True, onerror=None, followlinks=False):
       #        for z in i[2]:##If anyone doesn't know, the [2] is because 0 is dir, 1 is folders, and 2 is files.
       #            images.append(thumbnailer.thumbnail(i[0]+"/"+z,(64,64)))

    #c = dict(images=images, galleryname=gallerynum)
    #print("c happens to be "+str(c))
    print("images is " + str(images))
    return images

### main function that searches through html for image/image gallery markdown code and renders it as html
def run(text,pk):
    output = ""
    gallerynum = 0
    for line in findNewLine.split(text):
        m = findSquareBrackets.findall(line)
        print("m is "+str(m))
        ###checks if regular expression found square brackets on this line. (please note, an empty array ([]) is not square brackets...)
        if m != []:
            ###copy line for editing
            linecopy = line
            ###this loop formats the line with shadowbox code into the html
            for gallery in m:
                images = (findEachImage.split(gallery))### regex gets list of galleries on line
                cut = re.compile(r'\[\s*'+gallery+r'\s*\]')### 
                output += cut.split(linecopy)[0]
                print(cut.split(linecopy))
                print("linecopy was "+linecopy)
                if linecopy:
                    linecopy = cut.split(linecopy)[1]
                thestuff = (outputstuff(images, gallerynum, pk))
                for thething in thestuff:
                    output += thething
                gallerynum += 1
            output += linecopy
        ###if theres no gallery to render on this line, just add the line unchanged to the output
        else:
            output += line

    return output
