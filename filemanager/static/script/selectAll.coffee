

# lets do this! Coffee script style!

# (by this, I mean the writing of a script for pretty selection)

        
class window.selectAllTool

    oldbox: null
    selected: null
    targetboxes: []
    newbox: null

    selectBoxes: () ->
        if this.selected
            this.selected=false
            for element in this.targetboxes
                element.checked=true
        else
            this.selected=true
            for element in this.targetboxes
                element.checked=false

    startup: (allbox, targetboxes) ->
        this.selected=true
        this.targetboxes = document.getElementsByClassName(targetboxes)
        div = $ "<input type='checkbox'/>"
        div.addClass "coffee-selectAllBox"
        this.oldbox = $(allbox)
        this.oldbox.hide()
        div.click ->
          allBox.selectBoxes()
          #this.selectBoxes()
        this.newbox = div
        this.oldbox.after(this.newbox)

