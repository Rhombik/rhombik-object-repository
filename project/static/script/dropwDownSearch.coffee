class window.searchDrop

    dropdownlist: []
    formlist: []
    open: false

    #Register a css class to slide down in the event of a click
    registerClass: (argument) ->
        this.dropdownlist = document.getElementsByClassName(argument); 

    #Register some forms. Element will only close if forms are empty.
    registerFormClass: () ->
       pass

    init: () ->
        for i in [0...this.dropdownlist.length]
            if not this.formlistEmpty(i)
                $(this.dropdownlist[i]).toggle(true)


    #Slide down any registerd elements.
    open: () ->
        for i in [0...this.dropdownlist.length]
            $(this.dropdownlist[i]).slideDown()

    #Only close if all the forms in formlist are empy. Attached to the main content.
    close: () ->
        for i in [0...this.dropdownlist.length]
            if this.formlistEmpty(i)
                $(this.dropdownlist[i]).slideUp()

    formlistEmpty: (listId) ->
        eles = this.dropdownlist[listId].getElementsByClassName("tagit-choice");
        return (eles.length==0)


