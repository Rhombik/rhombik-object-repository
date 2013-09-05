
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
  from django.core.files.uploadedfile import InMemoryUploadedFile
  import sys
 

  browser_kind = [  ".png",".jpg",".gif" ]
  jsc3d_kind = [  ".stl",".obj" ]
  ##ext os the file extension, forced into lowercase becouse people are insane.
  ext = str(splitext(str(filebit.filename))[1].lower())
  response = HttpResponse(mimetype="image/png")
  if ext in browser_kind:
 
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
    thumb_file = InMemoryUploadedFile(thumb_io, None, str(sizebit)+"-"+str(filebit.filename)+".png", 'image/jpeg',
                                    1, None)
   
    # Once you have a Django file-like object, you may assign it to your ImageField
    # and save.
    return(thumb_file, "browser")
  if ext in jsc3d_kind:
    from selenium import webdriver
    from django.conf import settings

    driver = webdriver.PhantomJS()
    driver.set_window_size(sizebit[0],sizebit[1]) # not optional
    driver.get(settings.URL+"/thumbs/stl"+filebit.filename.url)
    print(settings.URL+"/thumbs/stl/"+filebit.filename.url+"   ------------------------------")
    imagedata = driver.get_screenshot_as_base64() # save a screenshot as base64 string, the only format phantom supports that isn't disk.

    import base64
    from io import BytesIO
    #converts the base64 encoded image data into a python file object
    thumb_io = BytesIO(base64.b64decode(imagedata))
    thumb_file = InMemoryUploadedFile(thumb_io, None, str(sizebit)+"-"+str(filebit.filename)+".png", 'image/jpeg',
                                      1, None)
#    thumb_file = False

    return(thumb_file, "jsc3d")
  return(False, "norender") 
  
  
