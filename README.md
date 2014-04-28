rhombik-object-repository
=============


This is all development information. The site isn't up to par yet, but you can see an example at [testing.rhombik.com](http://testing.rhombik.com)

rhombik-object-repository is an AGPL licensed object repository, competing in the same sphere as [thingiverse](http://thingiverse.com), [cubehero](http://cubehero.com), [youMagine](http://www.youmagine.com)
, and [bld3r](http://bld3r.com).

###What makes rhombik different?###

Open source.

If you're one of the independent 3D printer manufacturers like lulzbot, printrbot, or makers tool works; you need to send your users to your competitors website. It was somewhat tolerable before they threw "makerbot" branding all over the site. Now it's not.

So where should they send your users? Most of the alternatives have the potential to go the same way as thingiverse. If you want a platform that isn't going to get baught out by your competitors, you need open source.

We're commited to federation. If rhombik ever goes down or gets baught, you can just take our source and launch a new repo. It will be easy for users to migrate their projects. Don't bet on another horse you don't have control of.

###Developer information###

Rhombik uses:

 * Django web framework
 * pymarkdown
 * Haystack search
 * Celery queueing
 * selenium for generating thumbnails of javascript previewers
 * ...A bunch more that aren't really important enough to list.
 * Coffeescript, and [django-static-precompiler](https://github.com/andreyfedoseev/django-static-precompiler) to make javascript less painful.


Right now the code base is a bit of a mess. We're big believers in "release early, release often, hopefully get around to writing ~~better~~ some test cases". If you're interested in devloping for this, shoot me an [email](mailto://traverse.da@gmail.com) or visit our irc channel #rhombik on freenode. I can help get you up to speed on the code base. Take a look at the bug list for an idea of what needs doing.

---
To set up a development enviroment simply

    git clone https://github.com/Rhombik/rhombik-object-repository.git
    cd rhombik-object-repository
    pip install $(cat requirements.txt)
    python manage.py syncdb
    #follow the prompts to add a new devleoper superuser account to the test DB.
    python manage.py runserver

Unfortunately django-static-precompiler requires the nodejs coffee command, which means we can't just rely on pip for all of our dependencies. Install nodejs and run.

    sudo npm install coffee-script -g

We'll work on cacheing the compiled scripts into git, so you won't need it unless you're editing the javascript.

Then navigate to http://localhost:8000

If you want to use search functinality, you may need to rebuild the search index.

    python manage.py rebuild_index

---

Neither of us are proffesional programmers. If you want to know how we did something, please drop us a line. The code is probably pretty skitty, but we're here to explain anything that doesn't make sense.

We would love to restructure this at some point.

**project**

This app has all our default views. It also has the basic "project" model.

**filemanager**

This app contains the basic structure of our file systems. 

It has a "fileobject" model. That model contains the actual uploaded file. Each fileobject gets attached to a project. It has fields for subfolders, and "rendertype" which tells the front end what to use to display a preview and what to use to create a thumbnail. The rendertype field is filled by "thumbnailer.thumbnailer2".

It also has a "thumbobject" model. Each thumbobject is a png preview of a fileobject. It attaches to a fileobject. It gets the actual image from "thumbnailer.thumbnailer2". It's unique for [project, sizex, sizey]. This allows you to generate thumbnails of different sizes for each project.

**thumbnailer**

At the core of our service is a very robust thumbnailer. It takes screenshots of javascript renderers, so that what the use sees in a thumbnail and what the user see in a live preview are identical. Thumbnailing like that can take a while for more complicated file types, so we have a queueing system and an ajax thumbnail loader. It's overly complicated and poorly documents. But the short story is that in order to get a thumbnail you need to call somefileobject.get\_thumbnail(thumbX, thumbY), and then pass that data in a list[] to the gallery.html template. So something like

```python
#in your view
#Set up a list to store your images in
myimages = []
#get the first fileobject in the database, and append it to our images list.
myimages.append(fileobject.objects.get(pk=1))

render\_to\_string('mytemplate.html', dict(myimages=myimages, testgallery="testgallery")
```
```
#In "mytemplate.html"
{% include "gallery.html" with images=myimages galleryname=testgallery %}
```

**multiuploader**

Multiuploader contains the uploader code.



