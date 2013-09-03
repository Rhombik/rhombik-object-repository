#TRISTAN, this will not work. It's only for reference. Be afraid.
class renderstl(basefile, size):
  from selenium import webdriver
  from django.conf import settings

  driver = webdriver.PhantomJS()
  driver.set_window_size(size) # not optional
  driver.get(settings.URL+"/thumbs/stl/"+basefile.url)
  imagedata = driver.get_screenshot_as_base64() # save a screenshot as base64 string, the only format phantom supports that isn't disk.

  import base64
  from io import BytesIO
  #converts the base64 encoded image data into a python file object
  imagedata = Image.open(BytesIO(base64.b64decode(imagedata)))
    return(jsc3d, imagedata)

############### info on using thumbnailer.thumbnailer.thumbnail() #############
#This function takes:
#       URL;             a url (that it can access) to a file to be thumbnailed
#       size;            the dimensions of the thumbnail to be made in an array of two values

#And it returns a thumbobject ID.

