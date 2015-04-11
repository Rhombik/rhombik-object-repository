
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
  from io import BytesIO
  from django.core.files.uploadedfile import UploadedFile
  import sys
  from django.core.files.base import ContentFile 

  browser_kind = [  ".png",".jpg",".gif" ]
  jsc3d_kind = [  ".stl",".obj" ]
  text_kind = [".md",".txt"]
  ##ext os the file extension, forced into lowercase becouse people are insane.
  ext = str(splitext(str(filebit.filename))[1].lower())

  if ext in browser_kind:
    import StringIO
    filebit.filename.open()
    stream = StringIO.StringIO(filebit.filename.read())
    filebit.filename.close()
    img = Image.open(stream)
    img.convert('RGB')
    img.thumbnail(sizebit, Image.ANTIALIAS)
    backround = Image.new('RGBA', sizebit, (255, 255, 255, 0))  #with alpha
    backround.paste(img,((sizebit[0] - img.size[0]) / 2, (sizebit[1] - img.size[1]) / 2))
    thumb_io = BytesIO()
    backround.save( thumb_io, format='png', option='optimize')

    thumb_file = ContentFile(thumb_io.getvalue())
    thumb_file.name = str(sizebit)+"-"+str(filebit.filename)+".png"
    return(thumb_file, "browser")

  if ext in jsc3d_kind:
    from selenium import webdriver
    from django.conf import settings
    #How much to antialias by.
    rendermul = 2
    driver = webdriver.PhantomJS()
    driver.set_window_size(sizebit[0]*rendermul,sizebit[1]*rendermul) # not optional
    driver.get(settings.URL+"/thumbs/jsc3d/"+str(filebit.pk))
    counter = 0
    import time
    while driver.execute_script("return viewer.isLoaded") != True and counter <30:
         counter = counter+1
         time.sleep(1)

    imagedata = driver.get_screenshot_as_base64() # save a screenshot as base64 string, the only format phantom supports that isn't disk.

    import base64
    from io import BytesIO
    img = Image.open(BytesIO(base64.b64decode(imagedata)))
    img = img.convert('RGB')
    img.thumbnail(sizebit, Image.ANTIALIAS)
    thumb_io = BytesIO()
    img.save(thumb_io, format='png', option='optimize')

    thumb_file = ContentFile(thumb_io.getvalue())
    thumb_file.name = str(sizebit)+"-"+str(filebit.filename)+".png"

    return(thumb_file, "jsc3d")

  if ext in text_kind:
    return(None, "text")

  return(None, "norender") 
