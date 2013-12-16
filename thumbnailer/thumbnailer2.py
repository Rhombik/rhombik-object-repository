
#TRISTAN, this will not work. It's only for reference. Be afraid.
#class renderstl(basefile, size):
#  from selenium import webdriver
#  from django.conf import settings

#  driver = webdriver.PhantomJS()
#  driver.set_window_size(size) # not optional
#  driver.get(settings.URL+"/thumbs/stl/"+basefile.url)
#  imagedata = driver.get_screenshot_as_base64() # save a screenshot as base64 string, the only format phantom supports that isn't disk.

#  import base64
#  from io import BytesIO
#  #converts the base64 encoded image data into a python file object
#  imagedata = Image.open(BytesIO(base64.b64decode(imagedata)))
#  return(jsc3d, imagedata)


from io import StringIO, BytesIO

def thumbnailify(filebit, sizebit):
  from PIL import Image
  from os.path import splitext
  from django.http import HttpResponseRedirect, HttpResponse
  from io import BytesIO
  from django.core.files.uploadedfile import UploadedFile
  import sys
 

  browser_kind = [  ".png",".jpg",".gif" ]
  jsc3d_kind = [  ".stl",".obj" ]
  text_kind = [".md",".txt"]
# text_kind = [ ".txt" ]
  ##ext os the file extension, forced into lowercase becouse people are insane.
  ext = str(splitext(str(filebit.filename))[1].lower())
  response = HttpResponse(mimetype="image/png")

  if ext in browser_kind:
    print("filebit.filename"+str(filebit.filename.name))
    img = Image.open(filebit.filename)
    img.thumbnail(sizebit)
    print(img) 
    # Create a file-like object to write thumb data (thumb data previously created
    # using PIL, and stored in variable 'img')
    # using PIL, and stored in variable 'thumb')
#    thumb_io = BytesIO()
    thumb_io = BytesIO()
    img.save( thumb_io, format='png')
  
    # Create a new Django file-like object to be used in models as ImageField using
    # InMemoryUploadedFile.  If you look at the source in Django, a
    # SimpleUploadedFile is essentially instantiated similarly to what is shown here
    thumb_file = UploadedFile(thumb_io)
    thumb_file.name = str(sizebit)+"-"+str(filebit.filename)+".png"

# Once you have a Django file-like object, you may assign it to your ImageField
    # and save.
    return(thumb_file, "browser")

  if ext in jsc3d_kind:
    from selenium import webdriver
    from django.conf import settings

    driver = webdriver.PhantomJS()
    driver.set_window_size(sizebit[0],sizebit[1]) # not optional
    driver.get(settings.URL+"/thumbs/jsc3d/"+str(filebit.pk))
    imagedata = driver.get_screenshot_as_base64() # save a screenshot as base64 string, the only format phantom supports that isn't disk.

    import base64
    from io import BytesIO
    #converts the base64 encoded image data into a python file object
    thumb_io = BytesIO(base64.b64decode(imagedata))
    thumb_file = UploadedFile(thumb_io)
    thumb_file.name = str(sizebit)+"-"+str(filebit.filename)+".png"
#    thumb_file = False

    return(thumb_file, "jsc3d")

  if ext in text_kind:
    return(False, "text")

# if ext in text_kind:
#   print("filebit.filename"+str(filebit.filename.name))

#   from PIL import ImageFont, ImageDraw, Image
#   from django.conf import settings
#   from io import StringIO

#   img = Image.new("RGBA", (100,50), (255,255,255))
#   draw = ImageDraw.Draw(img)
#  #print(settings.URL+"/static/DejaVuSerif-Bold.ttf")
#  #font = ImageFont.truetype(settings.URL+"/media/DejaVuSerif-Bold.ttf", 12)

#   f = filebit.filename.file.read(64)
#   draw.text((10, 0), (f.decode("utf-8")[:16]), (0,0,0) )
#   draw.text((10, 10), (f.decode("utf-8")[16:32]), (0,0,0) )
#   draw.text((10, 20), (f.decode("utf-8")[32:48]), (0,0,0) )
#   draw.text((10, 30), (f.decode("utf-8")[48:64]), (0,0,0) )
#   draw.text((10, 40), ("\t..."), (0,0,0) )
#   img_resized = img.resize((sizebit), Image.ANTIALIAS)

#  #img = Image.open(filebit.filename)
#  #img.thumbnail(sizebit)
#   print(img) 
#   # Create a file-like object to write thumb data (thumb data previously created
#   # using PIL, and stored in variable 'img')
#   # using PIL, and stored in variable 'thumb')
#   thumb_io = BytesIO()
#   img.save( thumb_io, format='png')
# 
#   # Create a new Django file-like object to be used in models as ImageField using
#   # InMemoryUploadedFile.  If you look at the source in Django, a
#   # SimpleUploadedFile is essentially instantiated similarly to what is shown here
#   thumb_file = InMemoryUploadedFile(thumb_io, None, str(sizebit)+"-"+str(filebit.filename)+".png", 'image/jpeg',
#                                   1, None)
#  
#   # Once you have a Django file-like object, you may assign it to your ImageField
#   # and save.
#   return(thumb_file, "browser")


  return(False, "norender") 
