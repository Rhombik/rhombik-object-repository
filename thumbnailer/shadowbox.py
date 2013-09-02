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
import thumbnailer.thumbnailer as thumbnailer

##regular expressions...
findSquareBrackets = re.compile(r'[\[](.*?)[\]]')
findEachImage = re.compile(r'[\[,\s\]]*')
findNewLine = re.compile(r'(\n)')

### this function gets a list of images, a gallery name (numbers generated in order of gallery per page), and the pages pk. and returns an html string formatted to make a gallery
def outputstuff(imagelist, gallerynum, pk):
    images = []
    for image in imagelist:
        print("shadowimage "+image)
        print(settings.MEDIA_ROOT+"thumbnails/media/uploads/" + pk + image)
        if os.path.isfile(settings.MEDIA_ROOT+"thumbnails/media/uploads/" + pk + image):
            images.append(thumbnailer.thumbnail(settings.MEDIA_ROOT+"thumbnails/media/uploads/" + pk + image,(64,64)))
        else:
            for i in os.walk(settings.MEDIA_ROOT+"uploads/" + pk +"/"+ image , topdown=True, onerror=None, followlinks=False):
                for z in i[2]:##If anyone doesn't know, the [2] is because 0 is dir, 1 is folders, and 2 is files.
                    images.append(thumbnailer.thumbnail(i[0]+"/"+z,(64,64)))

    c = dict(images=images, galleryname=gallerynum)
    return render_to_string("gallery.html", c)


### main function that searches through html for image/image gallery markdown code and renders it as html
def run(text,pk):
    output = ""
    gallerynum = 0
    for line in findNewLine.split(text):
        m = findSquareBrackets.findall(line)
        ###checks if regular expression found square brackets on this line. (please note, an empty array ([]) is not square brackets...)
        if m != []:
            ###copy line for editing
            linecopy = line
            ###this loop formats the line with shadowbox code into the html
            for gallery in m:
                images = (findEachImage.split(gallery))
                cut = re.compile(r'\[\s*'+gallery+r'\s*\]')
                output += cut.split(linecopy)[0]
                linecopy = cut.split(linecopy)[1]
                output += outputstuff(images, gallerynum, pk)
                gallerynum += 1
            output += linecopy
        ###if theres no gallery to render on this line, just add the line unchanged to the output
        else:
            output += line

    return output
