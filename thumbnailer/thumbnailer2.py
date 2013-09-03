from PIL import Image
from selenium import webdriver

driver = webdriver.PhantomJS()
driver.set_window_size(1024, 768) # optional
driver.get('https://google.com/')
driver.save_screenshot('screen.png') # save a screenshot to disk



############### info on using thumbnailer.thumbnailer.thumbnail() #############
#This function takes:
#       URL;             a url (that it can access) to a file to be thumbnailed
#       size;            the dimensions of the thumbnail to be made in an array of two values

#And it returns a thumbobject ID.
def thumbnailify(filebit, sizebit):

  browser_kind = [  ".png",".jpg",".gif" ]

  if filebit.filetype in browser_kind:

    img = Image.open(filebit.filename)
    img.thumbnail(sizebit)
    print("it work'd!!!)
