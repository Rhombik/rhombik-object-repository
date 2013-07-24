"""
This is the amazing script Tristan is writing to get useful variables and use them to make cool shadowbox gallery html script.

Ok, not that amazing.

"""

testtext = """aegfas\nasegf\n[apples, notapples] other [more, list] text\nefaefva"""

from django.template.loader import render_to_string
from markdown.postprocessors import Postprocessor
import re
import os
from django.conf import settings
import thumbnailer

regexp1 = re.compile(r'[\[](.*?)[\]]')
regexp2 = re.compile(r'[\[,\s\]]*')
regexplines = re.compile(r'(\n)')

def outputstuff(imagelist, gallerynum, title):

    images = []
    for image in imagelist:
        if os.path.isfile(settings.MEDIA_ROOT+"uploads/" + title +"/"+ image):
            images.append(thumbnailer.thumbnail(settings.MEDIA_ROOT+"uploads/" + title +"/"+ image,(64,64)))
        else:
            for i in os.walk(settings.MEDIA_ROOT+"uploads/" + title +"/"+ image , topdown=True, onerror=None, followlinks=False):
                for z in i[2]:##If anyone doesn't know, the [2] is because 0 is dir, 1 is folders, and 2 is files.
                    images.append(thumbnailer.thumbnail(i[0]+"/"+z,(64,64)))
        #thestuff += "\n<a href=\"/media/uploads/Distractions/part1/"+image+"\" rel=\"shadowbox[gallery"+str(gallerynum)+"]\"><img src=\"/media/thumbnails/media/uploads/Distractions/part1/"+image+"\" class=\"thumbnail\"></a>\n"

    #request, "gallery.html", c
    c = dict(images=images, galleryname=gallerynum)
    return render_to_string("gallery.html", c)


def run(text,title):
    output = ""
    gallerynum = 0
    for line in regexplines.split(text):
        m = regexp1.findall(line)
        if m != []:
            thisline = line
            for gallery in m:
                images = (regexp2.split(gallery))
                cut = re.compile(r'\[\s*'+gallery+r'\s*\]')
                output += cut.split(thisline)[0]
                thisline = cut.split(thisline)[1]
                output += outputstuff(images, gallerynum, title)
                gallerynum += 1
            output += thisline
        else:
            #output += re.compile(r'[\[\],/s]*').match(m.group()).group() + "#"
            #n = regexp2.match(m[0])
            output += line
        #output += line
    return output
