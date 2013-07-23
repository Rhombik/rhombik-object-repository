Django3Dtools
=============

Some 3D tools for making previews of 3D objects, or anything else that can be previewed in javascript, such as GCODE or regular images.

Most of the actual code happens in "thumbnailer/". 

"thumbnailer.thumbnail" expects a

 * filepath, relative to http://yoursite.tld/, but not containing the URL string
 * A size in pixels. It just tells the javascript it's running in a browser window of that size, and makes certain the screenshot isn't bigger.

It relies on phantomJS for taking the screenshots, a headless webkit renderer. It gives you an array containing

 * The path to your originol file.
 * The path to the thumbnail.
 * what to render with as a string. "image", "stl", "gcode", or anything else.

The actual rendering is done via "thumbnailer/templates/gallery.html". It will take an array containing the output of thumbnailer.thumbnail (pass it as "images") and turn it into the correct html depending on whether it's a 3D file or an image or whatever. Right now it has renderes using jsc3d and your browsers image parser (just sends the image).

There's also an attempt at a markdown extension in "shadowbox.py". It will look for [lists, of, images, in, brackets] or [/folders] and turn them into galleries using "thumbnailer.py".

The code base is pretty ugly as it stands
