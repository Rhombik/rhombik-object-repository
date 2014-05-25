class window.searchDrop

    dropdownlist: []
    formlist: []
    open: false

    #Register a css class to slide down in the event of a click
    registerClass: (id) ->
        document.getElementById(id);       

    #Register some forms. Element will only close if forms are empty.
    registerFormClass: () ->
       pass


    #Slide down any registerd elements.
    open: () ->
        for i in drowdownlist
            i.slideDown()

    #Only close if all the forms in formlist are empy. Attached to the main content.
    close: () ->
        if formlistcontent != empty
            for i in drowdownlist
               i.slideUp()
       
