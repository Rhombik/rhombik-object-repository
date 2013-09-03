from selenium import webdriver

driver = webdriver.PhantomJS()
driver.set_window_size(1024, 768) # optional
driver.get('https://google.com/')
driver.save_screenshot('screen.png') # save a screenshot to disk
sbtn = driver.find_element_by_css_selector('button.gbqfba')
sbtn.click()

############### info on using thumbnailer.thumbnailer.thumbnail() #############
#This function takes:
#       URL;             a url (that it can access) to a file to be thumbnailed
#       size;            the dimensions of the thumbnail to be made in an array of two values

#And it returns a thumbobject ID.

